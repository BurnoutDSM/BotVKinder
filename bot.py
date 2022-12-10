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
        if user_id not in list_users:
            insert_users(user_id)  # Table with all users
            create_db(user_id)  # Tables for a single user
            if msg == 'начать поиск':
                bot.send_msg(user_id, f'Привет, {bot.find_name(user_id)}')
                bot.find_people(user_id)
                bot.send_msg(event.user_id, 'Вот что я нашел, если не подходит жми "Еще"')
                bot.unseen_people(user_id, offset)

            elif msg == 'еще' or msg == 'ещё':
                bot.send_msg(event.user_id, 'Я еще никого не искал. Жми "Начать поиск"')

            else:
                bot.send_msg(event.user_id, 'Я тебя не понял. Вот что я умею:'
                                            'Начать поиск - Ищю подходящих людей, показываю первого.'
                                            'Еще - Показываю следующего.'
                                            'Обнулить - Удаляю базу просмотренных людей, что бы снова их показать')

        else:
            if msg == 'начать поиск':
                bot.send_msg(user_id, f'Привет, {bot.find_name(user_id)}')
                drop_people(user_id)
                create_table_people(user_id)
                bot.find_people(user_id)  # contains the function insert_people()
                bot.send_msg(event.user_id, 'Вот что я нашел, если не подходит жми "Еще"')
                bot.unseen_people(user_id, offset)

            elif msg == 'еще' or msg == 'ещё':
                try:
                    for i in range(0, 1000):
                        # offset += 1
                        bot.unseen_people(user_id, offset)
                        break
                except TypeError:
                    bot.send_msg(event.user_id, 'Что-то пошло не так, попробуй "Начать поиск"')

            elif msg == 'обнулить':
                drop_seen_people(user_id)
                create_table_seen_people(user_id)
                bot.send_msg(event.user_id, 'Иноформация о просмотренных людях удалена')

            else:
                bot.send_msg(event.user_id, 'Я тебя не понял. Вот что я умею:'
                                            'Начать поиск - Ищю подходящих людей, показываю первого.'
                                            'Еще - Показываю следующего.'
                                            'Обнулить - Удаляю базу просмотренных людей, что бы снова их показать')
