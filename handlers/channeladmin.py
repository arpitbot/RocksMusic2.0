# Copyright (C) 2021 ๐๐๐๐๐ ๐๐๐๐๐๐๐

from asyncio.queues import QueueEmpty

from pyrogram import Client, filters
from pyrogram.types import Message

from config import que, BOT_USERNAME
from cache.admins import admins
from cache.admins import set
from callsmusic import callsmusic
from callsmusic.queues import queues
from helpers.filters import command, other_filters
from helpers.channelmusic import get_chat_id
from helpers.decorators import authorized_users_only, errors


@Client.on_message(command(["refresh", f"refresh@{BOT_USERNAME}"]) & other_filters)
async def update_admin(client, message):
    global admins
    new_admins = []
    new_ads = await client.get_chat_members(message.chat.id, filter="administrators")
    for u in new_ads:
        new_admins.append(u.user.id)
    admins[message.chat.id] = new_admins
    await message.reply_text(
        "โ Bot **reloaded correctly  By Asad!**\nโ **Admin list** has been **updated !**"
    )


@Client.on_message(command(["cpause", f"cpause@{BOT_USERNAME}"]) & other_filters)
@errors
@authorized_users_only
async def channel_pause(_, message: Message):
    try:
        conchat = await _.get_chat(message.chat.id)
        conid = conchat.linked_chat.id
        chid = conid
    except:
        await message.reply("โ `NOT_LINKED`\n\nโข **The userbot could not play music, due to group not linked to channel yet.**")
        return
    chat_id = chid
    if (chat_id not in callsmusic.pytgcalls.active_calls) or (
        callsmusic.pytgcalls.active_calls[chat_id] == "paused"
    ):
        await message.reply_text("โ **no music is currently playing**")
    else:
        callsmusic.pytgcalls.pause_stream(chat_id)
        await message.reply_text("โถ **Track paused.**\n\nโข **To resume the playback, use the**\nยป `/cresume` command.")


@Client.on_message(command(["cresume", f"cresume@{BOT_USERNAME}"]) & other_filters)
@errors
@authorized_users_only
async def channel_resume(_, message: Message):
    try:
        conchat = await _.get_chat(message.chat.id)
        conid = conchat.linked_chat.id
        chid = conid
    except:
        await message.reply("โ `NOT_LINKED`\n\nโข **The userbot could not play music, due to group not linked to channel yet.**")
        return
    chat_id = chid
    if (chat_id not in callsmusic.pytgcalls.active_calls) or (
        callsmusic.pytgcalls.active_calls[chat_id] == "playing"
    ):
        await message.reply_text("โ **no music is currently playing**")
    else:
        callsmusic.pytgcalls.resume_stream(chat_id)
        await message.reply_text("โธ **Track resumed.**\n\nโข **To pause the playback, use the**\nยป `/cpause` command.")


@Client.on_message(command(["cend", f"cend@{BOT_USERNAME}"]) & other_filters)
@errors
@authorized_users_only
async def channel_stop(_, message: Message):
    try:
        conchat = await _.get_chat(message.chat.id)
        conid = conchat.linked_chat.id
        chid = conid
    except:
        await message.reply("โ `NOT_LINKED`\n\nโข **The userbot could not play music, due to group not linked to channel yet.**")
        return
    chat_id = chid
    if chat_id not in callsmusic.pytgcalls.active_calls:
        await message.reply_text("โ **no music is currently playing**")
    else:
        try:
            callsmusic.queues.clear(chat_id)
        except QueueEmpty:
            pass

        callsmusic.pytgcalls.leave_group_call(chat_id)
        await message.reply_text("โ **music playback has ended**")


@Client.on_message(command(["cskip", f"cskip@{BOT_USERNAME}"]) & other_filters)
@errors
@authorized_users_only
async def skip(_, message: Message):
    global que
    try:
        conchat = await _.get_chat(message.chat.id)
        conid = conchat.linked_chat.id
        chid = conid
    except:
        await message.reply("โ `NOT_LINKED`\n\nโข **The userbot could not play music, due to group not linked to channel yet.**")
        return
    chat_id = chid
    if chat_id not in callsmusic.pytgcalls.active_calls:
        await message.reply_text("โ **no music is currently playing**")
    else:
        callsmusic.queues.task_done(chat_id)

        if callsmusic.queues.is_empty(chat_id):
            callsmusic.pytgcalls.leave_group_call(chat_id)
        else:
            callsmusic.pytgcalls.change_stream(
                chat_id, callsmusic.queues.get(chat_id)["file"]
            )

    qeue = que.get(chat_id)
    if qeue:
        skip = qeue.pop(0)
    if not qeue:
        return
    await message.reply_text("โญ **You've skipped to the next song.**")
