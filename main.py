from config import user_token, comm_token, offset
import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
from random import randrange
import requests
import datetime
from database import *
import time


class BotVK:
    def __init__(self, access_token, version='5.131'):
        self.token = access_token
        self.vk = vk_api.VkApi(token=comm_token)
        self.longpoll = VkLongPoll(self.vk)
        self.version = version
        self.params = {'access_token': self.token, 'v': self.version}

    def send_msg(self, user_id, message):
        self.vk.method('messages.send', {'user_id': user_id, 'message': message,
                       'random_id': randrange(10 ** 7), 'v': self.version})

    def find_age_low(self, user_id):
        url = 'https://api.vk.com/method/users.get'
        params = {'user_id': user_id, 'fields': 'bdate'}
        response = requests.get(url, params={**self.params, **params})
        user_data = response.json()
        if 'response' in user_data:
            user_bday = user_data['response'][0]['bdate']
            bday_list = user_bday.split('.')
            if len(bday_list) == 3:
                year = int(bday_list[2])
                year_now = int(datetime.date.today().year)
                return year_now - year - 1
            elif len(bday_list) == 2 or user_bday not in user_data['response'][0]:
                self.send_msg(user_id, 'Укажите возраст для поиска от (от 16)')
                for event in self.longpoll.listen():
                    if event.type == VkEventType.MESSAGE_NEW and event.to_me:
                        msg = event.text
                        return msg
        else:
            self.send_msg(user_id, f'{response.status_code} - '
                                   f'Не понимаю мин. возраст, '
                                   f'попробуй еще раз и/или обратись к администратору')
            print(response.status_code)

    def find_age_high(self, user_id):
        url = 'https://api.vk.com/method/users.get'
        params = {'user_id': user_id, 'fields': 'bdate'}
        response = requests.get(url, params={**self.params, **params})
        user_data = response.json()
        if 'response' in user_data:
            user_bday = user_data['response'][0]['bdate']
            bday_list = user_bday.split('.')
            if len(bday_list) == 3:
                year = int(bday_list[2])
                year_now = int(datetime.date.today().year)
                return year_now - year + 1
            elif len(bday_list) == 2 or user_bday not in user_data['response'][0]:
                self.send_msg(user_id, 'Укажи возраст для поиска до ')
                for event in self.longpoll.listen():
                    if event.type == VkEventType.MESSAGE_NEW and event.to_me:
                        msg = event.text
                        return msg
        else:
            self.send_msg(user_id, f'{response.status_code} - '
                                   f'Не понимаю макс. возраст, '
                                   f'попробуй еще раз и/или обратись к администратору')
            print(response.status_code)

    def find_gender(self, user_id):
        url = 'https://api.vk.com/method/users.get'
        params = {'user_ids': user_id, 'fields': 'sex'}
        response = requests.get(url, params={**self.params, **params})
        user_data = response.json()
        if 'response' in user_data:
            gender = user_data['response'][0]['sex']
            if gender == 1:
                return 2
            elif gender == 2:
                return 1
            elif gender == 0:
                self.send_msg(user_id, 'Укажи пол для поиска("м" или "ж")')
                for event in self.longpoll.listen():
                    if event.type == VkEventType.MESSAGE_NEW and event.to_me:
                        msg = event.text
                        if msg.lowwer() == 'м':
                            return 2
                        elif msg.lowwer() == 'ж':
                            return 1
                        else:
                            return 3
        else:
            self.send_msg(user_id, f'{response.status_code} - '
                                   f'Не понимаю пол, '
                                   f'попробу еще раз и/или обратись к администратору')
            print(response.status_code)

    def find_city(self, user_id):
        url = 'https://api.vk.com/method/users.get'
        params = {'user_ids': user_id, 'fields': 'city'}
        response = requests.get(url, params={**self.params, **params})
        user_data = response.json()
        if 'response' in user_data:
            if 'city' in user_data['response'][0]:
                return user_data['response'][0]['city']['title']
            else:
                self.send_msg(user_id, 'Введи город (полное название) проживания для поиска ')
                for event in self.longpoll.listen():
                    if event == VkEventType.MESSAGE_NEW and event.to_me:
                        msg = event.text
                        return msg
        else:
            self.send_msg(user_id, f'{response.status_code} - '
                                   f'Не понимаю город, '
                                   f'попробуй еще раз и/или обратись к администратору')
            print(response.status_code)

    def find_relation(self, user_id):
        url = 'https://api.vk.com/method/users.get'
        params = {'user_ids': user_id, 'fields': 'relation'}
        response = requests.get(url, params={**self.params, **params})
        user_data = response.json()
        if 'response' in user_data:
            if user_data['response'][0]['relation'] == 0:
                return 6
            else:
                return user_data['response'][0]['relation']
        else:
            self.send_msg(user_id, f'{response.status_code} - '
                                   f'Не понимаю семейное положение, '
                                   f'попробуй еще раз и/или обратись к администратору')
            print(response.status_code)

    def find_name(self, user_id):
        url = 'https://api.vk.com/method/users.get'
        params = {'user_ids': user_id}
        response = requests.get(url, params={**self.params, **params})
        user_data = response.json()
        if 'response' in user_data:
            return user_data['response'][0]['first_name']
        else:
            self.send_msg(user_id, f'{response.status_code} - '
                                   f'Не могу узнать имя, '
                                   f'попробуй еще раз и/или обратись к администратору')
            print(response.status_code)

    def find_people(self, user_id):
        url = 'https://api.vk.com/method/users.search'
        params = {'age_from': self.find_age_low(user_id), 'age_to': self.find_age_high(user_id),
                  'sex': self.find_gender(user_id), 'hometown': self.find_city(user_id),
                  'status': self.find_relation(user_id), 'fields': 'is_closed', 'count': 600}
        response = requests.get(url, params={**self.params, **params})
        users_data = response.json()
        if 'response' in users_data:
            for item in users_data['response']['items']:
                if item.get('is_closed') == False:
                    f_name = item.get('first_name')
                    l_name = item.get('last_name')
                    vk_id = str(item.get('id'))
                    vk_link = 'vk.com/id' + str(item.get('id'))
                    insert_people(user_id, f_name, l_name, vk_id, vk_link)
                else:
                    continue
            return 'Поиск завершен'
        else:
            self.send_msg(user_id, f'{response.status_code} - '
                                   f'Не смог найти людей, '
                                   f'попробуй еще раз и/или обратись к администратору')
            print(response.status_code)

    def extract_id_photo(self, user_id):
        url = 'https://api.vk.com/method/photos.get'
        params = {'owner_id': user_id, 'album_id': 'profile', 'extended': 1}
        response = requests.get(url, params={**self.params, **params})
        photos = response.json()
        try:
            if 'response' in photos:
                links = {}
                for items in photos['response']['items']:
                    photo_id = items['id']
                    comments1 = str(items['reposts']['count'])
                    comments = ''
                    if len(comments1) == 1:
                        comments = '000' + comments1
                    elif len(comments1) == 2:
                        comments = '00' + comments1
                    elif len(comments1) == 3:
                        comments = '0' + comments1
                    else:
                        comments = comments1
                    like1 = str(items['likes']['count'])
                    like = ''
                    if len(like1) == 1:
                        like = '000' + like1
                    elif len(like1) == 2:
                        like = '00' + like1
                    elif len(like1) == 3:
                        like = '0' + like1
                    else:
                        like = like1
                    date = [like, comments]
                    links[photo_id] = date
                sort_links = sorted(links.items(), reverse=True, key=lambda val: val[1])[0:3]
                return [lnk[0] for lnk in sort_links]
            else:
                print(response.status_code)
                self.send_msg(user_id, f'{response.status_code} - '
                                       f'Ошибка получения фото, '
                                       f'попробуй еще раз и/или обратись к администратору')
        except Exception:
            return ''

    def send_photo_1(self, user_id, offset):
        photo = self.extract_id_photo(self.person_id(user_id, offset))
        try:
            if len(photo) > 0:
                self.vk.method('messages.send', {'user_id': user_id, 'message': 'Лучшее фото', 'access_token': user_token,
                                                 'attachment': f'photo{self.person_id(user_id, offset)}_{photo[0]}',
                                                 'random_id': 0})
            else:
                self.send_msg(user_id, 'Нет фото')
        except TypeError:
            self.send_msg(user_id, 'Ошибка получения фото')

    def send_photo_2(self, user_id, offset):
        photo = self.extract_id_photo(self.person_id(user_id, offset))
        try:
            if len(photo) > 1:
                self.vk.method('messages.send', {'user_id': user_id, 'message': '2-е фото', 'access_token': user_token,
                                                 'attachment': f'photo{self.person_id(user_id, offset)}_{photo[1]}',
                                                 'random_id': 0})
            else:
                self.send_msg(user_id, 'Нет фото')
        except TypeError:
            self.send_msg(user_id, 'Ошибка получения фото')

    def send_photo_3(self, user_id, offset):
        photo = self.extract_id_photo(self.person_id(user_id, offset))
        try:
            if len(photo) > 2:
                self.vk.method('messages.send', {'user_id': user_id, 'message': '3-e фото', 'access_token': user_token,
                                                 'attachment': f'photo{self.person_id(user_id, offset)}_{photo[2]}',
                                                 'random_id': 0})
            else:
                self.send_msg(user_id, 'Нет фото')
        except TypeError:
            self.send_msg(user_id, 'Ошибка получения фото')

    def unseen_people(self, user_id, offset):
        self.send_photo_1(user_id, offset)
        time.sleep(0.4)
        self.send_photo_2(user_id, offset)
        time.sleep(0.4)
        self.send_photo_3(user_id, offset)
        self.send_msg(user_id, self.person_info(user_id, offset))
        insert_seen_people(user_id, self.person_id(user_id, offset))

    def person_info(self, user_id, offset):
        tuple_persons = select(user_id, offset)
        list_persons = []
        for person in tuple_persons:
            list_persons.append(person)
        return f'{list_persons[0]} {list_persons[1]}, страница - {list_persons[3]}'

    def person_id(self, user_id, offset):
        tuple_persons = select(user_id, offset)
        list_persons = []
        for person in tuple_persons:
            list_persons.append(person)
        return str(list_persons[2])


bot = BotVK(user_token)
