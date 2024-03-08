import random
import re

from pyrogram import Client, filters
from pyrogram.types import Message

from utils import get_sender_and_target_from_message

random_list = ["兔兔", "雁雁", "狗狗", "荧", "猫猫", "小企鹅", ]
random_slist = ['只', '条', '件', '个', '枚', '种', '把', '吨']


# random_message_list = ["想要挥刀自宫!", "想要申请全站自ban!", "开付费emby服!",
#                        "想要传禁转资源并改官组后缀!", "想要去盗取他站界面!", "想要去开群友的盒!", "想要唱希望之花",
#                        "想要手冲", "想去M-Team发自己的自制色情片","想要退群","想要被兔纸骂zako!","想要被兔纸暴打!",
#                        "想要爬上兔纸的床!","想要去东京援交","想自觉地撅起屁股","想露出来给群友透","想要被后入"]

@Client.on_message(filters.regex(r"^[+-].+") & filters.group & filters.text, group=100)
async def plus_or_minus(client: Client, message: Message):
    if not message.reply_to_message:
        message.reply_to_message = message

    sender, target_sender = await get_sender_and_target_from_message(message)

    text = message.text[1:]
    match = re.fullmatch(r"(\d+)( .+)?", text)
    if not match:
        return

    num = int(match.group(1))
    what = match.group(2)
    unit = random.choice(random_slist) + random.choice(random_list)

    if what:
        unit = what

    action = "加"
    if message.text.startswith("-"):
        action = "减"

    await message.reply(
        f'{sender.mention} 给 {target_sender.mention} {action}了 {num} {unit}!')
