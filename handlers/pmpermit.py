from callsmusic.callsmusic import client as USER
from pyrogram import filters
from pyrogram.types import Chat, Message, User
from config import BOT_USERNAME

@USER.on_message(filters.text & filters.private & ~filters.me & ~filters.bot)
async def pmPermit(client: USER, message: Message):
  await USER.send_message(message.chat.id,"πHi there, This is a music assistant service\n**βοΈ Rules:**\nπ..No chatting allowed.\nπ..No spam allowed.\nβ¨π§π΅πΆπ ππΌπ ππ²ππ²πΉπΌπ½π²π± ππ @Dr_Asad_Aliπ")
  return                       