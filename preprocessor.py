import re
import pandas as pd

def preprocess(data):
    pattern = '\d{1,2}/\d{1,2}/\d{1,2},\s\d{1,2}:\d{1,2}:\d{1,2}\s(?:AM|PM|am|pm)'
    dates = re.findall(pattern, data)
    messages = re.split(pattern, data)[1:]
    df = pd.DataFrame({'message': messages, 'date': dates})

    users = []
    messages = []

    for message in df['message']:

        message_stipped = message.lstrip('] ').rstrip('\n[')

        if message_stipped.startswith('\u200e'):
            users.append('group notification')
            messages.append(message_stipped.lstrip('\u200e'))

        else:
            entry = message_stipped.split(': ', 1)
            users.append(entry[0])
            messages.append(entry[1].rstrip('\n'))

    df['users'] = users
    df['messages'] = messages

    df['date'] = pd.to_datetime(df['date'], format='%d/%m/%y, %I:%M:%S %p')
    df['month'] = df['date'].dt.month_name()
    df['year'] = df['date'].dt.year
    df['minute'] = df['date'].dt.minute
    df['hour'] = df['date'].dt.hour
    df['timeline'] = df['date'].dt.to_period('M')
    df['day_of_week'] = df['date'].dt.day_name()
    df['message_date'] = df['date'].dt.date

    df.drop(columns = ['message'], inplace = True)

    return df