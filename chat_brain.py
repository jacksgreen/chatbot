import random
import math
import time
import requests


counter = 0
animations = ['afraid', 'bored', 'confused', 'crying', 'dancing', 'dog', 'excited', 'giggling', 'heartbroken', 'inlove', 'laughing', 'money', 'no', 'ok', 'takeoff', 'waiting']

def func(user_message):
    global counter
    user_message = user_message.lower()
    to_send = rude_words(user_message)
    if to_send:
        return ('crying', "I don't like that language!")
    to_send = boto_name(user_message)
    if to_send:
        return ('excited', "My name is Boto")
    to_send = user_name(user_message)
    if to_send is not False:
        return to_send
    to_send = current_time(user_message)
    if to_send is not False:
        return to_send
    to_send = joke(user_message)
    if to_send is not False:
        return to_send
    to_send = weather_update(user_message)
    if to_send is not False:
        return to_send
    to_send = ny_times_headline(user_message)
    if to_send is not False:
        return to_send

    if counter == 0:
        counter += 1
        return ('excited', f'Hi {user_message}')

    random_animation = random.randrange(0, len(animations) - 1)
    return(animations[random_animation], 'ask me something else')



def rude_words(user_message):
    if user_message[-1] == '?':
        user_message = user_message[:-1]
    user_message = user_message.split()
    with open('rude_words.txt') as swear_words:
        swear_words = swear_words.readlines()
        for lines in swear_words:
            word = lines.split()
            if word[0] in user_message:
                return True

def boto_name(user_message):
    if 'your' in user_message and 'name' in user_message:
        return True

def user_name(user_message):
    if 'my' in user_message and 'is' in user_message and 'name' in user_message:
        user_message = user_message.split()
        name_index = user_message.index('is') + 1
        return ('ok', f'Hi {user_message[name_index]}')
    else:
        return False

def current_time(user_message):
    if 'time' in user_message:
        seconds = time.time()
        local_time = time.localtime(seconds)
        return ('waiting', f'The time is {local_time.tm_hour}:{local_time.tm_min}')
    else:
        return False

def joke(user_message):
    if 'joke' in user_message:

        random_number = random.random() * 169
        random_number = math.ceil(random_number)
        with open('joke_list.txt') as joke_list:
            joke_list = joke_list.readlines()
            joke = joke_list[random_number]
        return ('laughing', joke)
    else:
        return False

def weather_update(user_message):
    if 'weather' in user_message:
        key = '85560421f770605c1d50a905ec19876c'
        city = 'Tel Aviv'
        request = requests.get(f'http://api.openweathermap.org/data/2.5/weather?q={city}&appid={key}')
        data = request.json()

        description = data['weather'][0]['description']
        temp = round(data['main']['temp'] - 273.15, 1)

        return ('takeoff', f'The weather in {city} is currently {temp}°C with {description}')
    else:
        return False

def ny_times_headline(user_message):
    if 'news' in user_message:
        key = 'y3m1ggaFqxNhKZmjZdu48sI0gqVw20uZ'
        request = requests.get(f'https://api.nytimes.com/svc/topstories/v2/home.json?api-key={key}')
        data = request.json()
        return ('confused', data['results'][0]['title'])
    else:
        return False