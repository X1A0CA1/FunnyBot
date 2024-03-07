import pyrogram.utils as utils
import pyrogram.enums as enums
from pyrogram.types.messages_and_media.message import Message


def link(self) -> str:
    if self.chat.type in (enums.ChatType.GROUP, enums.ChatType.SUPERGROUP, enums.ChatType.CHANNEL):
        return f"https://t.me/c/{utils.get_channel_id(self.chat.id)}/{self.id}"


setattr(Message, "link", property(link))
