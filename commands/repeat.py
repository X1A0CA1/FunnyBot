from pyrogram import Client, filters
from pyrogram.types import Message

from typing import List


def _compare(msg1: Message, msg2: Message) -> bool:
    if msg1.text and msg2.text:
        return msg1.text == msg2.text
    elif msg1.sticker and msg2.sticker:
        return msg1.sticker.file_unique_id == msg2.sticker.file_unique_id
    return False


def compare_messages(messages: List[Message]) -> bool:
    for i in range(len(messages) - 1):
        if not _compare(messages[i], messages[i + 1]):
            return False
    return True


class MessageList(list):
    def __init__(self, max_size=20, *args, **kwargs) -> None:
        self.max_size = max_size
        self.repeated = Message(id=0)
        super(MessageList, self).__init__(*args, **kwargs)

    def append(self, item: Message) -> None:
        """
        将一个消息插入队列的开头
        :param item:
        :return:
        """
        super(MessageList, self).insert(0, item)
        self._trim_list()

    def remove(self, item: Message) -> None:
        super(MessageList, self).remove(item)

    def update(self, item: Message) -> None:
        if not isinstance(item, Message):
            raise ValueError("item must be a Message")
        for index, message in enumerate(self):
            if message.id == item.id:
                self[index] = item
                return

    def _trim_list(self) -> None:
        if len(self) > self.max_size:
            del self[:len(self) - self.max_size]

    def need_repeat(self) -> bool:
        # 至少需要三条消息
        if len(self) < 3:
            return False
        # 如果和自己上次复读过的消息一样就不复读，直到出现不一样的消息
        if _compare(self[0], self.repeated):
            return False
        else:
            self.repeated = Message(id=0)
        # 如果连续三条消息都一样，就需要复读
        return compare_messages(self[:3])

    async def try_repeat(self) -> None:
        if self.need_repeat():
            message = self[0]
            repeat_message = await message.forward(message.chat.id)
            self.repeated = repeat_message
            self.append(repeat_message)


GROUP_LIST = {}


@Client.on_message((filters.text | filters.sticker) & filters.group, group=10)
async def message_handler(_: Client, message: Message):
    chat_messages: MessageList = GROUP_LIST.get(message.chat.id, None)
    if chat_messages:
        chat_messages.append(message)
    else:
        GROUP_LIST[message.chat.id] = MessageList()
        GROUP_LIST[message.chat.id].append(message)
        return

    await chat_messages.try_repeat()


@Client.on_edited_message((filters.text | filters.sticker) & filters.group, group=11)
async def edit_handler(_: Client, message: Message):
    chat_messages: MessageList = GROUP_LIST.get(message.chat.id, None)
    if message in chat_messages:
        chat_messages.update(message)
        await chat_messages.try_repeat()
