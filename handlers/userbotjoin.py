import asyncio

from callsmusic.callsmusic import client as USER
from config import BOT_USERNAME, SUDO_USERS
from helpers.decorators import authorized_users_only, errors
from helpers.filters import command
from pyrogram import Client, filters
from pyrogram.errors import UserAlreadyParticipant


@Client.on_message(
    command(["join", f"join@{BOT_USERNAME}"]) & ~filters.private & ~filters.bot
)
@authorized_users_only
@errors
async def addchannel(client, message):
    chid = message.chat.id
    try:
        invitelink = await client.export_chat_invite_link(chid)
    except:
        await message.reply_text(
            "<b> ๐ ๐๐ผ๐ป'๐ ๐๐ฎ๐๐ฒ ๐ฃ๐ฒ๐ฟ๐บ๐ฒ๐๐๐ถ๐ผ๐ป\n\nยป โ __๐๐ฑ๐ฑ ๐จ๐๐ฒ๐ฟ๐__</b>",
        )
        return

    try:
        user = await USER.get_me()
    except:
        user.first_name = "music assistant"

    try:
        await USER.join_chat(invitelink)
        await USER.send_message(
            message.chat.id, "๐ค: ๐ ๐๐ฎ๐๐ฒ ๐๐ผ๐ถ๐ป๐ฑ ๐๐ฒ๐ฟ๐ฒ ๐ง๐ผ ๐ฃ๐น๐ฎ๐ ๐ ๐๐๐ถ๐ฐ ๐ข๐ป ๐ฉ๐ ๐๐ต๐ฎ๐ "
        )
    except UserAlreadyParticipant:
        await message.reply_text(
            f"<b>โ ๐จ๐๐ฒ๐ฟ๐ฏ๐ผ๐ ๐๐น๐ฟ๐ฒ๐ฎ๐ฑ๐ ๐๐ป ๐๐ต๐ฎ๐</b>",
        )
    except Exception as e:
        print(e)
        await message.reply_text(
            f"<b>๐ ๐๐น๐ผ๐ผ๐ฑ ๐๐ฟ๐ฟ๐ผ๐ฟ ๐๐ฎ๐ ๐๐ฎ๐ฟ ๐๐ผ ๐๐ฒ๐ต๐ป๐ฐ๐ต๐ผ ๐ \n\n User {user.first_name} ๐๐ผ๐๐น๐ฑ๐ป'๐ ๐๐ผ๐ถ๐ป ๐ฌ๐ผ๐๐ฟ ๐๐ฟ๐ผ๐๐ฝ ๐๐๐ฒ ๐ง๐ผ ๐๐ฒ๐ฎ๐๐ ๐๐ผ๐ถ๐ป ๐ฅ๐ฒ๐พ๐๐ฒ๐๐ ๐๐ผ๐ฟ ๐จ๐๐ฒ๐ฟ๐ฏ๐ผ๐."
            "\n\n ๐ข๐ฟ ๐ ๐ฎ๐ป๐๐ฎ๐น๐น๐ ๐๐ฑ๐ฑ  @{ASSISTANT_NAME}  ๐ง๐ผ ๐ฌ๐ผ๐๐ฟ ๐๐ฟ๐ผ๐๐ฝ ๐๐ป๐ฑ ๐ง๐ฟ๐ ๐๐ด๐ฎ๐ถ๐ป</b>",
        )
        return
    await message.reply_text(
        f"<b>โ ๐จ๐๐ฒ๐ฟ๐ฏ๐ผ๐ ๐๐ผ๐ถ๐ป ๐ง๐ต๐ฒ ๐๐ต๐ฎ๐t</b>",
    )


@Client.on_message(
    command(["leave", f"leave@{BOT_USERNAME}"]) & filters.group & ~filters.edited
)
@authorized_users_only
async def rem(client, message):
    try:
        await USER.send_message(message.chat.id, "โ ๐๐ฎ ๐ฅ๐ฎ๐ต๐ฎ ๐๐ผ๐ป ๐ ๐ฎ๐ถ๐ป ๐๐ฟ๐ผ๐๐ฝ ๐๐ต๐ต๐ผ๐ฑ ๐๐ฒ๐")
        await USER.leave_chat(message.chat.id)
    except:
        await message.reply_text(
            "<b>๐จ๐๐ฒ๐ฟ ๐๐ผ๐๐น๐ฑ๐ป'๐ ๐๐ฒ๐ฎ๐๐ฒ ๐ฌ๐ผ๐๐ฟ ๐๐ฟ๐ผ๐๐ฝ, ๐ ๐ฎ๐ ๐๐น๐ผ๐ผ๐ฑ๐๐ฎ๐ถ๐ ๐๐ฟ๐ฟ๐ผ๐ฟ.\n\n ๐๐ถ๐ฐ๐ธ ๐ ๐ฒ ๐ ๐ฎ๐ป๐๐ฎ๐น๐น๐</b>"
        )

        return


@Client.on_message(command(["leaveall", f"leaveall@{BOT_USERNAME}"]))
async def bye(client, message):
    if message.from_user.id not in SUDO_USERS:
        return

    left = 0
    failed = 0
    lol = await message.reply("๐ **userbot** leaving all chats !")
    async for dialog in USER.iter_dialogs():
        try:
            await USER.leave_chat(dialog.chat.id)
            left += 1
            await lol.edit(
                f"Userbot leaving all group...\n\nLeft: {left} chats.\nFailed: {failed} chats."
            )
        except:
            failed += 1
            await lol.edit(
                f"Userbot leaving...\n\nLeft: {left} chats.\nFailed: {failed} chats."
            )
        await asyncio.sleep(0.7)
    await client.send_message(
        message.chat.id, f"Left {left} chats.\nFailed {failed} chats."
    )


@Client.on_message(
    command(["joinchannel", "ubjoinc"]) & ~filters.private & ~filters.bot
)
@authorized_users_only
@errors
async def addcchannel(client, message):
    try:
        conchat = await client.get_chat(message.chat.id)
        conid = conchat.linked_chat.id
        chid = conid
    except:
        await message.reply(
            "โ `NOT_LINKED`\n\nโข **The userbot could not play music, due to group not linked to channel yet.**"
        )
        return
    try:
        invitelink = await client.export_chat_invite_link(chid)
    except:
        await message.reply_text(
            "<b>โข ๐ ๐๐ผ๐ป'๐ ๐๐ฎ๐๐ฒ ๐ฃ๐ฒ๐ฟ๐บ๐ฒ๐๐๐ถ๐ผ๐ป\n\nยป โ __๐๐ฑ๐ฑ ๐จ๐๐ฒ๐ฟ๐__</b>",
        )
        return

    try:
        user = await USER.get_me()
    except:
        user.first_name = "helper"

    try:
        await USER.join_chat(invitelink)
        await USER.send_message(
            message.chat.id, "๐ค: ๐ ๐๐ฎ๐๐ฒ ๐๐ผ๐ถ๐ป๐ฑ ๐๐ฒ๐ฟ๐ฒ ๐ง๐ผ ๐ฃ๐น๐ฎ๐ ๐ ๐๐๐ถ๐ฐ ๐ข๐ป ๐ฉ๐"
        )
    except UserAlreadyParticipant:
        await message.reply_text(
            "<b>โ ๐จ๐๐ฒ๐ฟ๐ฏ๐ผ๐ ๐๐น๐ฟ๐ฒ๐ฎ๐ฑ๐ ๐๐ป ๐๐ต๐ฎ๐ป๐ป๐ฒ๐น</b>",
        )
        return
    except Exception as e:
        print(e)
        await message.reply_text(
            f"<b>๐ Flood Wait Error ๐\n\n**userbot couldn't join to channel** due to heavy join requests for userbot, make sure userbot is not banned in channel."
            f"\n\nor manually add @{ASSISTANT_NAME} to your channel and try again</b>",
        )
        return
    await message.reply_text(
        "<b>โ ๐ ๐ฎ๐ถ๐ป ๐๐ฎ ๐๐ฎ๐๐ฎ ๐๐ฝ๐ธ๐ฒ๐ ๐๐ต๐ฎ๐ป๐ป๐ฒ๐น ๐ ๐ฎ๐ถ๐ป</b>",
    )
