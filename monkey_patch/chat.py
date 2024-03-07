from pyrogram.types.user_and_chats.chat import Chat
from pyrogram.types.user_and_chats.user import Link

from utils import contains_only_special_whitespace


def full_name(self) -> str:
    if contains_only_special_whitespace(self.title):
        fullname = "潇洒的互联网高隐私皮套行者"
    else:
        fullname = self.title
    return fullname


def mention(self) -> Link:
    if self.username:
        return Link(
            f"https://t.me/{self.username}",
            self.full_name,
            self._client.parse_mode
        )
    else:
        chat_id = self.id
        if str(chat_id).startswith("-100"):
            chat_id = chat_id.lstrip("-100")

        return Link(
            f"tg://privatepost?channel={chat_id}&post=-1",
            self.full_name,
            self._client.parse_mode
        )


# noinspection DuplicatedCode
def __eq__(self, other) -> bool:
    if isinstance(other, Chat):
        return self.id == other.id
    else:
        return False


setattr(Chat, "full_name", property(full_name))
setattr(Chat, "mention", property(mention))
setattr(Chat, "__eq__", __eq__)
