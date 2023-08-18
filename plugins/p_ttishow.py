from pyrogram import Client, filters, enums
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery
from pyrogram.errors.exceptions.bad_request_400 import MessageTooLong, PeerIdInvalid
from info import ADMINS, LOG_CHANNEL, SUPPORT_CHAT, MELCOW_NEW_USERS, MELCOW_VID, CHNL_LNK, GRP_LNK
from database.users_chats_db import db
from database.ia_filterdb import Media
from utils import get_size, temp, get_settings
from Script import script
from pyrogram.errors import ChatAdminRequired
import asyncio 

"""-----------------------------------------https://t.me/GetTGLink/4179 --------------------------------------"""

@Client.on_message(filters.new_chat_members & filters.group)
async def save_group(bot, message):
    r_j_check = [u.id for u in message.new_chat_members]
    if temp.ME in r_j_check:
        if not await db.get_chat(message.chat.id):
            total=await bot.get_chat_members_count(message.chat.id)
            r_j = message.from_user.mention if message.from_user else "Anonymous" 
            await bot.send_message(LOG_CHANNEL, script.LOG_TEXT_G.format(message.chat.title, message.chat.id, total, r_j))       
            await db.add_chat(message.chat.id, message.chat.title)
        if message.chat.id in temp.BANNED_CHATS:
            # Inspired from a boat of a banana tree
            k = await message.reply(
                text='<b>ᴄʜᴀᴛ ɴᴏᴛ ᴀʟʟᴏᴡᴇᴅ 🐞\n\nᴍʏ ᴀᴅᴍɪɴs ʜᴀs ʀᴇsᴛʀɪᴄᴛᴇᴅ ᴍᴇ ғʀᴏᴍ ᴡᴏʀᴋɪɴɢ ʜᴇʀᴇ ! ɪғ ʏᴏᴜ ᴡᴀɴᴛ ᴛᴏ ᴋɴᴏᴡ ᴍᴏʀᴇ ᴀʙᴏᴜᴛ ɪᴛ ᴄᴏɴᴛᴀᴄᴛ sᴜᴘᴘᴏʀᴛ..</b>',
                reply_markup=reply_markup,
            )

            try:
                await k.pin()
            except:
                pass
            await bot.leave_chat(message.chat.id)
            return
        await message.reply_text(
            text=f"<b>ᴛʜᴀɴᴋʏᴏᴜ ғᴏʀ ᴀᴅᴅɪɴɢ ᴍᴇ ɪɴ {message.chat.title} ❣️\n\nɪғ ʏᴏᴜ ʜᴀᴠᴇ ᴀɴʏ ǫᴜᴇsᴛɪᴏɴs & ᴅᴏᴜʙᴛs ᴀʙᴏᴜᴛ ᴜsɪɴɢ ᴍᴇ ᴄᴏɴᴛᴀᴄᴛ sᴜᴘᴘᴏʀᴛ.</b>",
            reply_markup=reply_markup)
    else:
        settings = await get_settings(message.chat.id)
        if settings["welcome"]:
            for u in message.new_chat_members:
                if (temp.MELCOW).get('welcome') is not None:
                    try:
                        await (temp.MELCOW['welcome']).delete()
                    except:
                        pass
                temp.MELCOW['welcome'] = await message.reply_video(
                                                 video=(MELCOW_VID),
                                                 caption=(script.MELCOW_ENG.format(u.mention, message.chat.title)),
                                                 parse_mode=enums.ParseMode.HTML
                )
                
        if settings["auto_delete"]:
            await asyncio.sleep(600)
            await (temp.MELCOW['welcome']).delete()
                
               



@Client.on_message(filters.command('leave') & filters.user(ADMINS))
async def leave_a_chat(bot, message):
    if len(message.command) == 1:
        return await message.reply('ɢɪᴠᴇ ᴍᴇ ᴀ ᴄʜᴀᴛ ɪᴅ')
    chat = message.command[1]
    try:
        chat = int(chat)
    except:
        chat = chat
    try:
        await bot.send_message(
            chat_id=chat,
            text='<b>ʜᴇʟʟᴏ ғʀɪᴇɴᴅs, \nᴍʏ ᴀᴅᴍɪɴ ʜᴀs ᴛᴏʟᴅ ᴍᴇ ᴛᴏ ʟᴇᴀᴠᴇ ғʀᴏᴍ ɢʀᴏᴜᴘ, sᴏ ɪ ɢᴏ! ɪғ ʏᴏᴜ ᴡᴀɴɴᴀ ᴀᴅᴅ ᴍᴇ ᴀɢᴀɪɴ ᴄᴏɴᴛᴀᴄᴛ ᴍʏ sᴜᴘᴘᴏʀᴛ ɢʀᴏᴜᴘ ᴏʀ ᴍʏ ᴏᴡɴᴇʀ</b>',
            reply_markup=reply_markup,
        )

        await bot.leave_chat(chat)
        await message.reply(f"ʟᴇғᴛ ᴛʜᴇ ᴄʜᴀᴛ `{chat}`")
    except Exception as e:
        await message.reply(f'Error - {e}')

@Client.on_message(filters.command('disable') & filters.user(ADMINS))
async def disable_chat(bot, message):
    if len(message.command) == 1:
        return await message.reply('ɢɪᴠᴇ ᴍᴇ ᴀ ᴄʜᴀᴛ ɪᴅ')
    r = message.text.split(None)
    if len(r) > 2:
        reason = message.text.split(None, 2)[2]
        chat = message.text.split(None, 2)[1]
    else:
        chat = message.command[1]
        reason = "No reason Provided"
    try:
        chat_ = int(chat)
    except:
        return await message.reply('ɢɪᴠᴇ ᴍᴇ ᴀ ᴠᴀʟɪᴅ ᴄʜᴀᴛ ɪᴅ')
    cha_t = await db.get_chat(int(chat_))
    if not cha_t:
        return await message.reply("ᴄʜᴀᴛ ɴᴏᴛ ғᴏᴜɴᴅ ɪɴ ᴅʙ")
    if cha_t['is_disabled']:
        return await message.reply(f"ᴛʜɪs ᴄʜᴀᴛ ɪs ᴀʟʀᴇᴀᴅʏ ᴅɪsᴀʙʟᴇᴅ:\nʀᴇᴀsᴏɴ-<code> {cha_t['reason']} </code>")
    await db.disable_chat(int(chat_), reason)
    temp.BANNED_CHATS.append(int(chat_))
    await message.reply('ᴄʜᴀᴛ sᴜᴄᴄᴇssғᴜʟʟʏ ᴅɪsᴀʙʟᴇᴅ')
    try:
        await bot.send_message(
            chat_id=chat_, 
            text=f'<b>ʜᴇʟʟᴏ ғʀɪᴇɴᴅs, \nᴍʏ ᴀᴅᴍɪɴ ʜᴀs ᴛᴏʟᴅ ᴍᴇ ᴛᴏ ʟᴇᴀᴠᴇ ғʀᴏᴍ ɢʀᴏᴜᴘ sᴏ ɪ ɢᴏ! ɪғ ʏᴏᴜ ᴡᴀɴɴᴀ ᴀᴅᴅ ᴍᴇ ᴀɢᴀɪɴ ᴄᴏɴᴛᴀᴄᴛ ᴍʏ sᴜᴘᴘᴏʀᴛ ɢʀᴏᴜᴘ.</b> \nʀᴇᴀsᴏɴ : <code>{reason}</code>',
            reply_markup=reply_markup)
        await bot.leave_chat(chat_)
    except Exception as e:
        await message.reply(f"Error - {e}")


@Client.on_message(filters.command('enable') & filters.user(ADMINS))
async def re_enable_chat(bot, message):
    if len(message.command) == 1:
        return await message.reply('ɢɪᴠᴇ ᴍᴇ ᴀ ᴄʜᴀᴛ ɪᴅ')
    chat = message.command[1]
    try:
        chat_ = int(chat)
    except:
        return await message.reply('ɢɪᴠᴇ ᴍᴇ ᴀ ᴠᴀʟɪᴅ ᴄʜᴀᴛ ɪᴅ')
    sts = await db.get_chat(int(chat))
    if not sts:
        return await message.reply("ᴄʜᴀᴛ ɴᴏᴛ ғᴏᴜɴᴅ ɪɴ ᴅʙ !")
    if not sts.get('is_disabled'):
        return await message.reply('ᴛʜɪs ᴄʜᴀᴛ ɪs ɴᴏᴛ ʏᴇᴛ ᴅɪsᴀʙʟᴇᴅ.')
    await db.re_enable_chat(int(chat_))
    temp.BANNED_CHATS.remove(int(chat_))
    await message.reply("ᴄʜᴀᴛ sᴜᴄᴄᴇssғᴜʟʟʏ ʀᴇ-ᴇɴᴀʙʟᴇᴅ")


@Client.on_message(filters.command('stats') & filters.incoming)
async def get_ststs(bot, message):
    rju = await message.reply('ғᴇᴛᴄʜɪɴɢ sᴛᴀᴛs..')
    total_users = await db.total_users_count()
    totl_chats = await db.total_chat_count()
    files = await Media.count_documents()
    size = await db.get_db_size()
    free = 536870912 - size
    size = get_size(size)
    free = get_size(free)
    await rju.edit(script.STATUS_TXT.format(files, total_users, totl_chats, size, free))


@Client.on_message(filters.command('invite') & filters.user(ADMINS))
async def gen_invite(bot, message):
    if len(message.command) == 1:
        return await message.reply('ɢɪᴠᴇ ᴍᴇ ᴀ ᴄʜᴀᴛ ɪᴅ')
    chat = message.command[1]
    try:
        chat = int(chat)
    except:
        return await message.reply('ɢɪᴠᴇ ᴍᴇ ᴀ ᴠᴀʟɪᴅ ᴄʜᴀᴛ ɪᴅ')
    try:
        link = await bot.create_chat_invite_link(chat)
    except ChatAdminRequired:
        return await message.reply("ɪɴᴠɪᴛᴇ ʟɪɴᴋ ɢᴇɴᴇʀᴀᴛɪᴏɴ ғᴀɪʟᴇᴅ, ɪᴀᴍ ɴᴏᴛ ʜᴀᴠɪɴɢ sᴜғғɪᴄɪᴇɴᴛ ʀɪɢʜᴛs")
    except Exception as e:
        return await message.reply(f'Error {e}')
    await message.reply(f'ʜᴇʀᴇ ɪs ʏᴏᴜʀ ɪɴᴠɪᴛᴇ ʟɪɴᴋ {link.invite_link}')

@Client.on_message(filters.command('ban') & filters.user(ADMINS))
async def ban_a_user(bot, message):
    # https://t.me/GetTGLink/4185
    if len(message.command) == 1:
        return await message.reply('ɢɪᴠᴇ ᴍᴇ ᴀ ᴜsᴇʀ ɪᴅ / ᴜsᴇʀɴᴀᴍᴇ')
    r = message.text.split(None)
    if len(r) > 2:
        reason = message.text.split(None, 2)[2]
        chat = message.text.split(None, 2)[1]
    else:
        chat = message.command[1]
        reason = "No reason Provided"
    try:
        chat = int(chat)
    except:
        pass
    try:
        k = await bot.get_users(chat)
    except PeerIdInvalid:
        return await message.reply("ᴛʜɪs ɪs ᴀɴ ɪɴᴠᴀʟɪᴅ ᴜsᴇʀ, ᴍᴀᴋᴇ sᴜʀᴇ ɪ ʜᴀᴠᴇ ᴍᴇᴛ ʜɪᴍ ʙᴇғᴏʀᴇ.")
    except IndexError:
        return await message.reply("ᴛʜɪs ᴍɪɢʜᴛ ʙᴇ ᴀ ᴄʜᴀɴɴᴇʟ, ᴍᴀᴋᴇ sᴜʀᴇ ɪᴛs ᴀ ᴜsᴇʀ.")
    except Exception as e:
        return await message.reply(f'Error - {e}')
    else:
        jar = await db.get_ban_status(k.id)
        if jar['is_banned']:
            return await message.reply(f"{k.mention} ɪs ᴀʟʀᴇᴀᴅʏ ʙᴀɴɴᴇᴅ\nʀᴇᴀsᴏɴ: {jar['ban_reason']}")
        await db.ban_user(k.id, reason)
        temp.BANNED_USERS.append(k.id)
        await message.reply(f"sᴜᴄᴄᴇssғᴜʟʟʏ ʙᴀɴɴᴇᴅ {k.mention}")


    
@Client.on_message(filters.command('unban') & filters.user(ADMINS))
async def unban_a_user(bot, message):
    if len(message.command) == 1:
        return await message.reply('ɢɪᴠᴇ ᴍᴇ ᴀ ᴜsᴇʀ ɪᴅ / ᴜsᴇʀɴᴀᴍᴇ')
    r = message.text.split(None)
    if len(r) > 2:
        reason = message.text.split(None, 2)[2]
        chat = message.text.split(None, 2)[1]
    else:
        chat = message.command[1]
        reason = "No reason Provided"
    try:
        chat = int(chat)
    except:
        pass
    try:
        k = await bot.get_users(chat)
    except PeerIdInvalid:
        return await message.reply("ᴛʜɪs ɪs ᴀɴ ɪɴᴠᴀʟɪᴅ ᴜsᴇʀ, ᴍᴀᴋᴇ sᴜʀᴇ ɪ ʜᴀᴠᴇ ᴍᴇᴛ ʜɪᴍ ʙᴇғᴏʀᴇ.")
    except IndexError:
        return await message.reply("ᴛʜɪs ᴍɪɢʜᴛ ʙᴇ ᴀ ᴄʜᴀɴɴᴇʟ, ᴍᴀᴋᴇ sᴜʀᴇ ɪᴛs ᴀ ᴜsᴇʀ.")
    except Exception as e:
        return await message.reply(f'Error - {e}')
    else:
        jar = await db.get_ban_status(k.id)
        if not jar['is_banned']:
            return await message.reply(f"{k.mention} ɪs ɴᴏᴛ ʏᴇᴛ ʙᴀɴɴᴇᴅ.")
        await db.remove_ban(k.id)
        temp.BANNED_USERS.remove(k.id)
        await message.reply(f"sᴜᴄᴄᴇssғᴜʟʟʏ ᴜɴʙᴀɴɴᴇᴅ {k.mention}")


    
@Client.on_message(filters.command('users') & filters.user(ADMINS))
async def list_users(bot, message):
    # https://t.me/GetTGLink/4184
    raju = await message.reply('ɢᴇᴛᴛɪɴɢ ʟɪsᴛ ᴏғ ᴜsᴇʀs')
    users = await db.get_all_users()
    out = "ᴜsᴇʀs sᴀᴠᴇᴅ ɪɴ ᴅʙ ᴀʀᴇ:\n\n"
    async for user in users:
        out += f"<a href=tg://user?id={user['id']}>{user['name']}</a>"
        if user['ban_status']['is_banned']:
            out += '( Banned User )'
        out += '\n'
    try:
        await raju.edit_text(out)
    except MessageTooLong:
        with open('users.txt', 'w+') as outfile:
            outfile.write(out)
        await message.reply_document('users.txt', caption="List Of Users")

@Client.on_message(filters.command('chats') & filters.user(ADMINS))
async def list_chats(bot, message):
    raju = await message.reply('ɢᴇᴛᴛɪɴɢ ʟɪsᴛ ᴏғ ᴄʜᴀᴛs')
    chats = await db.get_all_chats()
    out = "ᴄʜᴀᴛs sᴀᴠᴇᴅ ɪɴ ᴅʙ ᴀʀᴇ:\n\n"
    async for chat in chats:
        out += f"**Title:** `{chat['title']}`\n**- ID:** `{chat['id']}`"
        if chat['chat_status']['is_disabled']:
            out += '( Disabled Chat )'
        out += '\n'
    try:
        await raju.edit_text(out)
    except MessageTooLong:
        with open('chats.txt', 'w+') as outfile:
            outfile.write(out)
        await message.reply_document('chats.txt', caption="List Of Chats")
