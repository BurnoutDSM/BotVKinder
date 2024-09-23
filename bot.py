from main import *
from keyboard import send_buttons

        # Used at the first launch
create_db()  # ATTENTION this method will delete all registered users if there are any


for event in bot.longpoll.listen():
    if event.type == VkEventType.MESSAGE_NEW and event.to_me:
        user_id = str(event.user_id)
        msg = event.text.lower()
        send_buttons(user_id, "Принял, действую.")
        tuple_users = select_users()
        list_users = []
        for i in tuple_users:
            list_users.append(i[0])
        if user_id not in list_users:
            insert_users(user_id)
            if msg == 'начать поиск':
                bot.send_msg(user_id, f'Привет, {bot.find_name(user_id)}')
                bot.find_people(user_id)
                bot.send_msg(event.user_id, 'Вот что я нашел, если не подходит жми "Еще".')
                bot.unseen_people(user_id)

            elif msg == 'еще' or msg == 'ещё':
                bot.send_msg(event.user_id, 'Я еще никого не искал. Жми "Начать поиск".')

            else:
                bot.send_msg(event.user_id, 'Я тебя не понял. Вот что я умею: \n'
                                            '"Начать поиск" - Ищю подходящих людей, показываю первого. \n'
                                            '"Еще" - Показываю следующего. \n'
                                            '"Обнулить" - Удаляю базу просмотренных людей, что бы снова их показать.')

        else:
            if msg == 'начать поиск':
                bot.send_msg(user_id, f'Привет, {bot.find_name(user_id)}')
                delete_from_persons(user_id)
                bot.find_persons(user_id)  # contains the function insert_people()
                bot.send_msg(event.user_id, 'Вот что я нашел, если не подходит жми "Еще".')
                bot.unseen_persons(user_id)

            elif msg == 'еще' or msg == 'ещё':
                try:
                    bot.unseen_people(user_id)
                except TypeError:
                    bot.send_msg(event.user_id, 'Нет анкет, попробуй "Начать поиск" или "Обнулить"')

            elif msg == 'обнулить':
                delete_from_seen_persons(user_id)
                bot.send_msg(event.user_id, 'Иноформация о просмотренных людях удалена.')

            else:
                bot.send_msg(event.user_id, 'Я тебя не понял. Вот что я умею: \n '
                                            '"Начать поиск" - Ищю подходящих людей, показываю первого. \n'
                                            '"Еще" - Показываю следующего. \n'
                                            '"Обнулить" - Удаляю базу просмотренных людей, что бы снова их показать.')
