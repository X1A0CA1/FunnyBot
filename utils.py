from copy import deepcopy
from typing import Tuple

from pyrogram.types import Message, User, Chat

from bot import bot


def contains_only_special_whitespace(string: str) -> bool:
    chars = (
        "\u000A\u0020\u200B\u200C\u200D\u200E\u200F\u2060\u2061\u2062\u2063\u2064\u2065\u2066"
        "\u2068\u2069\u206A\u206B\u206C\u206D\u206E\u206F\u3164\uFE0F"
    )
    return all(char in chars for char in string)


async def get_sender_and_target_from_message(message: Message) -> tuple[User | None | Chat, User | None | Chat]:
    sender = message.from_user or message.sender_chat
    target_sender = deepcopy(message.reply_to_message.from_user) or deepcopy(message.reply_to_message.sender_chat)
    target_sender._client = bot

    if sender.id == target_sender.id:
        target_sender.first_name = '自己'
        target_sender.last_name = ''

    return sender, target_sender
