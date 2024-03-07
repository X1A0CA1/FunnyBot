from pyrogram.types.messages_and_media.message import Message
from pyrogram.types.user_and_chats.chat import Chat
from pyrogram.types.user_and_chats.user import User
import pyrogram.utils as utils
import pyrogram.enums as enums


def link(self) -> str:
    if self.chat.type in (enums.ChatType.GROUP, enums.ChatType.SUPERGROUP, enums.ChatType.CHANNEL):
        return f"https://t.me/c/{utils.get_channel_id(self.chat.id)}/{self.id}"


setattr(Message, "link", property(link))
