from pyrogram import Client
from pyrogram.types import Message, User, Chat
from pyrogram.enums import ChatType, ChatMembersFilter
from pyrogram.errors import FloodWait, SlowmodeWait, PeerIdInvalid, UserIsBlocked

from bot import bot


def contains_only_special_whitespace(string: str) -> bool:
    chars = (
        "\u000A\u0020\u200B\u200C\u200D\u200E\u200F\u2060\u2061\u2062\u2063\u2064\u2065\u2066"
        "\u2068\u2069\u206A\u206B\u206C\u206D\u206E\u206F\u3164\uFE0F"
    )
    return all(char in chars for char in string)


# 从消息， chat_id, Chat 获取， 群组的名字，适用于频道皮套、群组皮套
async def get_sender_chat_fullname(chat: Message | int | Chat) -> str:
    full_name = ""
    if isinstance(chat, Message):
        full_name = chat.sender_chat.title
        if chat.author_signature:
            if contains_only_special_whitespace(chat.author_signature):
                full_name += "(空白字符皮套人)"
            else:
                full_name += f"({chat.author_signature})"
        else:
            full_name += ("(频道皮套)" if chat.sender_chat.type is ChatType.CHANNEL else "(无头衔群组皮套)")

    elif isinstance(chat, int):
        chat = await bot.get_chat(chat)
        full_name = chat.title
        full_name += ("(频道皮套)" if chat.type is ChatType.CHANNEL else "(群组皮套)")

    elif isinstance(chat, Chat):
        full_name = chat.title
        full_name += ("(频道皮套)" if chat.type is ChatType.CHANNEL else "(群组皮套)")

    else:
        raise ValueError("chat must be a Message, int or Chat object")

    return full_name


async def get_user_fullname(obj: User | int | Message) -> str:
    if isinstance(obj, Message):
        obj = obj.from_user
    elif isinstance(obj, int):
        obj = await bot.get_users(obj)

    if isinstance(obj, User):
        user = obj
        full_name = user.first_name
        if user.last_name:
            full_name += f" {user.last_name}"
        if contains_only_special_whitespace(full_name):
            full_name = "潇洒的互联网高隐私行者"
    else:
        raise ValueError("param must be a User, int or Message object")
    return full_name


async def get_sender_info_from_msg(message: Message) -> tuple[str, int] | tuple[None, None]:
    full_name = user_id = None
    if not isinstance(message, Message):
        raise ValueError("message must be a Message object")

    if message.from_user:
        full_name = await get_user_fullname(message)
        user_id = message.from_user.id
    elif message.sender_chat:
        full_name = await get_sender_chat_fullname(message)
        user_id = message.sender_chat.id

    return full_name, user_id
