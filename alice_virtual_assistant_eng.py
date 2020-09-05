import datetime as dt
import requests

DATABASE = {
    'Sergey': 'Omsk',
    'Sonya': 'Moscow',
    'Alexey': 'Kaliningrad',
    'Michael': 'Moscow',
    'Dmitry': 'Chelyabinsk',
    'Alina': 'Krasnoyarsk',
    'Egor': 'Perm',
    'Nikolay': 'Krasnoyarsk',
    'Artem': 'Vladivostok',
    'Petr': 'Mikhaylovka'
}

UTC_OFFSET = {
    'Moscow': 3,
    'Saint-Petersburgh': 3,
    'Novosibirsk': 7,
    'Ekaterinburg': 5,
    'Nizhny Novgorod': 3,
    'Kazan': 3,
    'Chelyabinsk': 5,
    'Omsk': 6,
    'Samara': 4,
    'Rostov-on-Don': 3,
    'Ufa': 5,
    'Krasnoyarsk': 7,
    'Voronezh': 3,
    'Perm': 5,
    'Volgograd': 4,
    'Krasnodar': 3,
    'Kaliningrad': 2,
    'Vladivostok': 10
}


def format_count_friends(count_friends):
    if count_friends == 1:
        return '1 friend'
    else:
        return f'{count_friends} friends'


def what_time(city):
    offset = UTC_OFFSET[city]
    city_time = dt.datetime.utcnow() + dt.timedelta(hours=offset)
    f_time = city_time.strftime("%H:%M")
    return f_time


def what_weather(city):
    url = f'http://wttr.in/{city}'
    weather_parameters = {
        'format': 2,
        'M': ''
    }
    try:
        response = requests.get(url, params=weather_parameters)
    except requests.ConnectionError:
        return '<Connection Error>'
    if response.status_code == 200:
        return response.text.strip()
    else:
        return '<Wheather server error>'


def process_anfisa(query):
    if query == 'How many friends do I have?':
        count_string = format_count_friends(len(DATABASE))
        return f'You have {count_string}'
    elif query == 'Who are all my friends?':
        friends_string = ', '.join(DATABASE.keys())
        return f'Your friends are: {friends_string}'
    elif query == 'Where are all my friends?':
        unique_cities = set(DATABASE.values())
        cities_string = ', '.join(unique_cities)
        return f'Your friends are in cities: {cities_string}'
    else:
        return '<Unknown request>'


def process_friend(name, query):
    if name in DATABASE:
        city = DATABASE[name]
        if query == 'Where are you?':
            return f'{name} is in city {city}'
        elif query == 'What time is it?':
            if city not in UTC_OFFSET:
                return f'<Cant define the time in the city {city}>'
            time = what_time(city)
            return f'There is time {time}'
        elif query == 'What is the wheather?':
            return what_weather(city)
        else:
            return '<Unknown request>'
    else:
        return f'You dont have a friend named {name}'


def process_query(query):
    tokens = query.split(', ')
    name = tokens[0]
    if name == 'Anfisa':
        return process_anfisa(tokens[1])
    else:
        return process_friend(name, tokens[1])


def runner():
    queries = [
        'Anfisa, How many friends do I have?',
        'Анфиса, Who are all my friends?',
        'Анфиса, Where are all my friends?',
        'Анфиса, Who is guilty?',
        'Nikolay, Where are you?',
        'Sonya, What to do?',
        'Anton, Where are you?',
        'Alexey, What time is it?',
        'Artem, What time is it?',
        'Anton, What time is it?',
        'Petr, What time is it?',
        'Nikolay, What is the wheather?',
        'Sonya, What is the wheather?',
        'Anton, What is the wheather?'
    ]
    for query in queries:
        print(query, '-', process_query(query))


runner()