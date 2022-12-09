from main import *
from keyboard import send_buttons

        # Used at the first launch
# drop_table_users()          # ATTENTION This function will delete all registered users
# create_table_users()


for event in bot.longpoll.listen():
    if event.type == VkEventType.MESSAGE_NEW and event.to_me:
        user_id = str(event.user_id)
        msg = event.text.lower()
        send_buttons(user_id, "Принял, действую")
        tuple_users = select_users()
        list_users = []
        for i in tuple_users:
            list_users.append(i[0])
        if user_id in list_users:
            if msg == 'начать поиск':
                bot.send_msg(user_id, f'Привет, {bot.find_name(user_id)}')
                bot.send_msg(event.user_id, 'Вот что я нашел, если не подходит жми "Еще"')
                bot.unseen_people(user_id, offset)

            elif msg == 'еще' or msg == 'ещё':
                for i in range(0, 1000):
                    offset += 1
                    bot.unseen_people(user_id, offset)
                    break

            else:
                bot.send_msg(event.user_id, 'Твоё сообщение непонятно')
        else:
            if msg == 'начать поиск':
                insert_user(user_id)
                create_db(user_id)
                bot.send_msg(user_id, f'Привет, {bot.find_name(user_id)}')
                bot.find_people(user_id)
                bot.send_msg(event.user_id, 'Вот что я нашел, если не подходит жми "Еще"')
                bot.unseen_people(user_id, offset)

            elif msg == 'еще' or msg == 'ещё':
                for i in range(0, 1000):
                    offset += 1
                    bot.unseen_people(user_id, offset)
                    break

            else:
                bot.send_msg(event.user_id, 'Твоё сообщение непонятно')
