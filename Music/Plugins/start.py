import yt_dlp
from Music import (
    ASSID,
    BOT_ID,
    BOT_NAME,
    BOT_USERNAME,
    OWNER,
    SUDOERS,
    app,
)
from Music.MusicUtilities.database.chats import is_served_chat
from Music.MusicUtilities.database.queue import remove_active_chat
from Music.MusicUtilities.database.sudo import get_sudoers
from Music.MusicUtilities.helpers.inline import personal_markup
from Music.MusicUtilities.helpers.thumbnails import down_thumb
from Music.MusicUtilities.helpers.ytdl import ytdl_opts
from Music.config import GROUP, CHANNEL
from pyrogram import Client, filters
from pyrogram.types import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    Message,
)


def start_pannel():
    buttons = [
        [
            InlineKeyboardButton(text="sᴜᴘᴘᴏʀᴛ​", url=f"https://t.me/{GROUP}"),
            InlineKeyboardButton(text="ᴜᴘᴅᴀᴛᴇs", url=f"https://t.me/{CHANNEL}"),
        ],
        [
            InlineKeyboardButton("ᴄᴏᴍᴍᴀɴᴅ​", url="https://telegra.ph/DEXDECRYPT-MUSICBOT-01-11-2"),
        ],
    ]
    return (
        "🎛 **{BOT_NAME} Is one of the telegram bots that can play music on the group**",
        buttons,
    )


pstart_markup = InlineKeyboardMarkup(
    [
        [
            InlineKeyboardButton(
                "Add Me To Your Group", url=f"https://t.me/{BOT_USERNAME}?startgroup=true"),
        ],
        [
            InlineKeyboardButton("Support", url=f"https://t.me/{GROUP}"),
            InlineKeyboardButton("Updates", url=f"https://t.me/{CHANNEL}"),
        ],
        [
            InlineKeyboardButton("Cmd Music", url="https://telegra.ph/DEXDECRYPT-MUSICBOT-01-11-2"),
            InlineKeyboardButton("Cmd Stream", url="https://telegra.ph/DEXDECRYPT-MUSICBOT-01-11"),
        ],
    ]
)
welcome_captcha_group = 2


@app.on_message(filters.new_chat_members, group=welcome_captcha_group)
async def welcome(_, message: Message):
    chat_id = message.chat.id
    for member in message.new_chat_members:
        try:
            if member.id in OWNER:
                return await message.reply_text(
                    f"🦸🏻‍♂️ **Bot owner [{member.mention}] just joined this group.**"
                )
            if member.id in SUDOERS:
                return await message.reply_text(
                    f"**🤖 Admin Bot [{member.mention}] just joined this group.**"
                )
            if member.id == ASSID:
                await remove_active_chat(chat_id)
            if member.id == BOT_ID:
                out = start_pannel()
                await message.reply_text(
                    f"""
👋 ** Hello, it's nice to be able to join this group**

**Don't forget to make me an admin in this group**
""",
                    reply_markup=InlineKeyboardMarkup(out[1]),
                    disable_web_page_preview=True
                )
                return
        except BaseException:
            return


@Client.on_message(
    filters.group
    & filters.command(
        ["start", "help", f"start@{BOT_USERNAME}", f"help@{BOT_USERNAME}"]
    )
)
async def start(_, message: Message):
    chat_id = message.chat.id
    out = start_pannel()
    await message.reply_text(
        f"""
Thanks for including me on {message.chat.title}.
Music is alive.

For help please click the button below.
""",
        reply_markup=InlineKeyboardMarkup(out[1]),
        disable_web_page_preview=True
    )
    return


@Client.on_message(filters.private & filters.incoming & filters.command("start"))
async def play(_, message: Message):
    if len(message.command) == 1:
        user_id = message.from_user.id
        user_name = message.from_user.first_name
        rpk = "[" + user_name + "](tg://user?id=" + str(user_id) + ")"
        await app.send_message(
            message.chat.id,
            text=f"""
**✨ Hello {rpk}!  How Are You?

🤖 [{BOT_NAME}](tg://user?id=2129034376) is a bot that can be used to listen to songs in voice chat and can play videos in voice chat!

🧰 To find out all the available command bots, you can press the two buttons below, namely Cmd Music and Cmd Stream**

""",
            parse_mode="markdown",
            reply_markup=pstart_markup,
            reply_to_message_id=message.message_id,
        )
    elif len(message.command) == 2:
        query = message.text.split(None, 1)[1]
        f1 = query[0]
        f2 = query[1]
        f3 = query[2]
        finxx = f"{f1}{f2}{f3}"
        if str(finxx) == "inf":
            query = (str(query)).replace("info_", "", 1)
            query = f"https://www.youtube.com/watch?v={query}"
            with yt_dlp.YoutubeDL(ytdl_opts) as ytdl:
                x = ytdl.extract_info(query, download=False)
            thumbnail = x["thumbnail"]
            searched_text = f"""
🔍 **Video Track Information**

❇️**Title:** {x["title"]}

⏳ **Duration:** {round(x["duration"] / 60)} Mins
👀 **Watched:** `{x["view_count"]}`
👍 **Like:** `{x["like_count"]}`
👎 **Do not like:** `{x["dislike_count"]}`
⭐️ **Average Rating:** {x["average_rating"]}
🎥 **Name channel:** {x["uploader"]}
📎 **Channel Link:** [Kunjungi Dari Sini]({x["channel_url"]})
🔗 **Link:** [Link]({x["webpage_url"]})
"""
            link = x["webpage_url"]
            buttons = personal_markup(link)
            userid = message.from_user.id
            thumb = await down_thumb(thumbnail, userid)
            await app.send_photo(
                message.chat.id,
                photo=thumb,
                caption=searched_text,
                parse_mode="markdown",
                reply_markup=InlineKeyboardMarkup(buttons),
            )
        if str(finxx) == "sud":
            sudoers = await get_sudoers()
            text = "**💻 SUDO USER LIST**\n\n"
            for count, user_id in enumerate(sudoers, 1):
                try:
                    user = await app.get_users(user_id)
                    user = user.first_name if not user.mention else user.mention
                except Exception:
                    continue
                text += f"- {user}\n"
            if not text:
                await message.reply_text("No Sudo User")
            else:
                await message.reply_text(text)
