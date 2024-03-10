from pyrogram import Client, filters
from pyrogram.types import Message
import random
import cn2an

score_randoms_list = ['喵~', '捏~', '哼!', '**的', 'baka!', 'mks', 'asu']
admin_list = [1992000380, 6660179114]

MSG_COUNTS = {}


class UserMsg:
    def __init__(self, UserEntity, MsgCount):
        self.user = UserEntity
        self.count = MsgCount

    def addone(self):
        self.count = self.count + 1


@Client.on_message(filters.group & (filters.text | filters.sticker), group=120)
async def msg_count(client: Client, message: Message):
    msg_count_chat = MSG_COUNTS.get(message.chat.id)
    if msg_count_chat is None:
        MSG_COUNTS.update({message.chat.id: {
        }})
        return
    sender = message.from_user or message.sender_chat
    sender_entity = msg_count_chat.get(sender.id)
    if sender_entity is None:
        msg_count_chat.update({sender.id:
                                   UserMsg(sender, 0)
                               })
        return
    sender_entity.addone()


@Client.on_message(filters.group & filters.command("water_scores_list"), group=12)
async def waterlist(client, message):
    msg_count = MSG_COUNTS.get(message.chat.id)
    if msg_count is None:
        header = ["今日还没有水王上榜~(水满十条才能上哦)"]
    else:
        header = ["本群今日水王排行榜~(水满十条才能上哦)"]
        listsorted = []
        for i in list(msg_count.values()):
            listsorted.append([i.user, i.count])
        top_players = sorted(listsorted, key=lambda s: s[1], reverse=True)[:14]
        count = 0
        for idx, (key, value) in enumerate(top_players, start=1):
            if value > 9:
                position = cn2an.an2cn(idx, "up")
                header.append(f'第 {position} 名 {get_sender_name(key)} 水了 {value} 条信息')
                count += 1
        if len(top_players) > count and count > 0:
            header.append(f'还有几个水逼我就不列举了，{random.choice(score_randoms_list)}')
        if count == 0:
            header = ["今日还没有水王上榜~"]
    await message.reply('\n'.join(header))


@Client.on_message(filters.private & filters.command("reset_water_scores_list"), group=13)
async def resetwaterlistgrp(client, message):
    if message.from_user.id in admin_list:
        MSG_COUNTS = {}
        await message.reply("(所有)重置水王排行榜成功！")


@Client.on_message(filters.group & filters.command("reset_water_scores_list"), group=14)
async def resetwaterlistgrp(client, message):
    if message.from_user is not None:
        if message.from_user.id in admin_list:
            MSG_COUNTS[message.chat.id] = {}
            await message.reply("(本群)重置水王排行榜成功！")
        else:
            await message.reply("你没有权限执行此命令")
    else:
        await message.reply("皮套/匿名状态时 不可使用此命令")


def get_sender_name(User) -> str:
    if User.first_name is not None:
        user_name = User.first_name
        if User.last_name is not None:
            user_name = user_name + " " + User.last_name
        return user_name
    elif User.title is not None:
        return User.title
