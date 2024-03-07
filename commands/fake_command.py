import re
from copy import deepcopy

from pyrogram import Client, filters
from pyrogram.types import Message


ACTIONS = {
    "kiss": '{from_user_name} 亲了一口 {target_user_name}!',
    "mua": '{from_user_name} 冲过去抱住 {target_user_name}!',
    "rua": '{from_user_name} 揉揉 {target_user_name} 的头!',
    "bia": '{from_user_name} 敲打 {target_user_name} 的脸蛋!',
    "bite": '{from_user_name} 咬了一口 {target_user_name}!',
    "stick": '{from_user_name} 贴贴了 {target_user_name}!',
    "ban": '{target_user_name} 已被管理员永久封禁！',
    "unban": '{target_user_name} 已解封！',
    "kick": '{target_user_name} 已被管理员永久踢出！',
    "csn": '{from_user_name} 抓住 {target_user_name} 一顿输出！',
    "apple": '{from_user_name} 送给 {target_user_name} 一个苹果！',
    "hug": '{from_user_name} 紧紧拥抱 {target_user_name} ！',
    "nakadashi": '{from_user_name} 注入了 {target_user_name} ！',
    "yue": '{from_user_name} 吐了 {target_user_name} 一身！',

}


@Client.on_message(filters.group & filters.text & filters.regex(r"^[!！].+"))
async def fake_command(client: Client, message: Message):
    if not message.reply_to_message:
        message.reply_to_message = message

    sender = message.from_user or message.sender_chat
    target_sender = deepcopy(message.reply_to_message.from_user) or deepcopy(message.reply_to_message.sender_chat)
    target_sender._client = client
    if sender.id == target_sender.id:
        target_sender.first_name = '自己'
        target_sender.last_name = ''

    action = message.text[1:]
    if action in ACTIONS:
        text = ACTIONS[action].format(**{
            'from_user_name': sender.mention,
            'target_user_name': target_sender.mention
        })
        await client.send_message(
            chat_id=message.chat.id,
            reply_to_message_id=message.id,
            text=text
        )
    else:
        match = re.fullmatch(r"(.+) (.+)", message.text)
        if match:
            action = match.group(1)
            what = match.group(2)
            await client.send_message(
                chat_id=message.chat.id,
                reply_to_message_id=message.id,
                text=f'{sender.mention} {action} {target_sender.mention} {what}!')
        else:
            await client.send_message(
                chat_id=message.chat.id,
                reply_to_message_id=message.id,
                text=f'{sender.mention} {action} {target_sender.mention}!'
            )
