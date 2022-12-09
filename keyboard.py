import json
from main import bot


def data_button(text, color):
    return {
        'action': {
            'type': 'text',
            'payload': "{\"button\": \"" + "1" + "\"}",
            'label': f'{text}'
        },
        'color': f'{color}'
    }


keyboard = {
    "one_time": False,
    "buttons": [
            [data_button('Начать поиск', 'primary')],
            [data_button('Еще', 'secondary')]
        ]
}

keyboard = json.dumps(keyboard, ensure_ascii=False).encode('utf-8')
keyboard = str(keyboard.decode('utf-8'))


def send_buttons(user_id, text):
    bot.vk.method('messages.send', {'user_id': user_id, 'message': text, 'random_id': 0, 'keyboard': keyboard})
