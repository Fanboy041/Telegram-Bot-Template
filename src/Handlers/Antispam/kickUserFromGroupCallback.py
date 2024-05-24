from datetime import datetime, timedelta
from Database.MongoDB import get_admin, get_user, owner_collection
from telebot import types

def kick_user_from_group_callback(bot, call):
    user_id = int(call.data.split('_')[2])
    group_id = call.data.split('_')[3]

    user_first_name = call.message.text.split("'")[1]
    if "[" in call.message.text:
        text = call.message.text.split("[")[1]
        group_name = call.message.text.split("'")[3]
        text = text.split("]")[0]
    else:
        text = None
        
    owner = None
    userIds = []
    administrators = bot.get_chat_administrators(group_id)
    for admin in administrators:
        userIds.append(admin.user.id)
        if admin.status == "creator":
            owner = admin.user.id

    bot.delete_message(call.message.chat.id, call.message.message_id)                   

    if user_id not in userIds:
        bot.send_message(call.message.chat.id, "Done!")

        if get_admin(admin.user.id) is not None or get_user(admin.user.id) is not None or owner_collection.find_one({"chat_id": admin.user.id}) is not None:
            if text is not None:
                bot.send_message(user_id, f"you kicked from this group {group_name} by sending this Link: \n [{text}]")
            else:
                bot.send_message(user_id, "you kicked from this group")
        bot.ban_chat_member(group_id, user_id)

    else:
        if text is not None:
            bot.send_message(owner, f"i want to kick this user {user_first_name} [{user_id}](tg://user?id={user_id}), because of sending this Link {text} in this Group {group_name}", parse_mode = "Markdown")
        else:
            bot.send_message(owner, f"i want to kick this user {user_first_name} [{user_id}](tg://user?id={user_id})", parse_mode = "Markdown")
