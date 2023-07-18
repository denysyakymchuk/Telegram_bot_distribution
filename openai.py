import requests
import json

OPENAI_API_KEY = 'ваш токен'


def open_ai(group: str):
    url = 'https://api.openai.com/v1/chat/completions'
    headers = {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer ' + OPENAI_API_KEY
    }
    message = f"chatgpt пожалуйста поздоровайся со всеми учасниками группы от имени {group}, группа не group - мы просто здороваемся от этого имени, не спрашивай как дела просто поздоровайся, можешь пожелать всем продуктивного дня и добавь пару смайликов"
    data = {
        'model': 'gpt-3.5-turbo',
        'messages': [
            {'role': 'user', 'content': message}
        ],
        'temperature': 0.7
    }

    response = requests.post(url, headers=headers, json=data)
    response_data = response.json()

    if 'choices' in response_data:
        gen_text = response_data['choices'][0]['message']['content']
        # print(gen_text.encode('utf-8').decode('utf-8'))
    else:
        # print('Ошибка выполнения запроса:', response_data['error'])
        pass