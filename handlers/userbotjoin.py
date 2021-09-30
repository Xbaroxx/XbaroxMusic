import asyncio

from pyrogram import Client, filters
from pyrogram.errors import UserAlreadyParticipant

from callsmusic.callsmusic import client as USER
from config import BOT_USERNAME, SUDO_USERS
from helpers.decorators import authorized_users_only, errors
from helpers.filters import command


@Client.on_message(
    command(["userbotjoin", f"userbotjoin@{BOT_USERNAME}"])
    & ~filters.private
    & ~filters.bot
)
@authorized_users_only
@errors
async def addchannel(client, message):
    chid = message.chat.id
    try:
        invitelink = await client.export_chat_invite_link(chid)
    except:
        await message.reply_text(
            "<b>promote me as admin first !</b>",
        )
        return

    try:
        user = await USER.get_me()
    except:
        user.first_name = "music assistant"

    try:
        await USER.join_chat(invitelink)
        await USER.send_message(
            message.chat.id, "🤖: i'm joined here for playing music on voice chat"
        )
    except UserAlreadyParticipant:
        await message.reply_text(
            f"<b>✅ userbot already joined this group.</b>",
        )
    except Exception as e:
        print(e)
        await message.reply_text(
            f"<b>🛑 Flood Wait Error 🛑 \n\n User {user.first_name} couldn't join your group due to heavy join requests for userbot."
            "\n\nor manually add assistant to your Group and try again</b>",
        )
        return
    await message.reply_text(
        f"<b>✅ userbot successfully joined this group.</b>",
    )


@Client.on_message(
    command(["userbotleave", f"userbotleave@{BOT_USERNAME}"])
    & filters.group
    & ~filters.edited
)
@authorized_users_only
async def rem(client, message):
    try:
        await USER.send_message(message.chat.id, "✅ userbot successfully left group")
        await USER.leave_chat(message.chat.id)
    except:
        await message.reply_text(
            "<b>user couldn't leave your group, may be floodwaits.\n\nor manually kick me from your group</b>"
        )

        return


@Client.on_message(command(["userbotleaveall", f"userbotleaveall@{BOT_USERNAME}"]))
async def bye(client, message):
    if message.from_user.id not in SUDO_USERS:
        return

    left = 0
    failed = 0
    lol = await message.reply("Assistant Leaving all chats")
    async for dialog in USER.iter_dialogs():
        try:
            await USER.leave_chat(dialog.chat.id)
            left += 1
            await lol.edit(
                f"Assistant leaving all group... \n\nLeft: {left} chats. Failed: {failed} chats."
            )
        except:
            failed += 1
            await lol.edit(
                f"Assistant leaving... Left: {left} chats. Failed: {failed} chats."
            )
        await asyncio.sleep(0.7)
    await client.send_message(
        message.chat.id, f"Left {left} chats. Failed {failed} chats."
    )


@Client.on_message(
    command(["userbotjoinchannel", "ubjoinc"]) & ~filters.private & ~filters.bot
)
@authorized_users_only
@errors
async def addcchannel(client, message):
    try:
        conchat = await client.get_chat(message.chat.id)
        conid = conchat.linked_chat.id
        chid = conid
    except:
        await message.reply("is the chat even linked ?")
        return
    try:
        invitelink = await client.export_chat_invite_link(chid)
    except:
        await message.reply_text(
            "<b>promote me as group admin first !</b>",
        )
        return

    try:
        user = await USER.get_me()
    except:
        user.first_name = "helper"

    try:
        await USER.join_chat(invitelink)
        await USER.send_message(message.chat.id, "🤖: i joined here as you requested")
    except UserAlreadyParticipant:
        await message.reply_text(
            "<b>helper already in your channel</b>",
        )
        return
    except Exception as e:
        print(e)
        await message.reply_text(
            f"<b>🛑 Flood Wait Error 🛑 \n\n User {user.first_name} couldn't join your channel due to heavy join requests for userbot! Make sure user is not banned in channel."
            f"\n\nOr manually add @{ASSISTANT_NAME} to your Group and try again</b>",
        )
        return
    await message.reply_text(
        "<b>helper userbot joined your channel</b>",
    )
