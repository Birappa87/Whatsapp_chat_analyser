import pandas as pd
from urlextract import URLExtract
from collections import Counter
extractor = URLExtract()
import emoji
import matplotlib.pyplot as plt
from wordcloud import WordCloud
from gensim.parsing.preprocessing import remove_stopwords
import re

def fetch_stats(selected_user, df):

    if selected_user != 'Overall':
        df = df[df['users'] == selected_user]

    num_messages = df.shape[0]

    words = []
    links = []
    emojis = []
    for message in df['messages']:
        words.extend(message.split())
        links.extend(extractor.find_urls(message))
        emojis.extend([c for c in message if c in emoji.UNICODE_EMOJI['en']])

    image_count = df['messages'].str.count('image omitted').sum()
    video_count = df['messages'].str.count('video omitted').sum()
    audio_count = df['messages'].str.count('audio omitted').sum()
    emoji_df = pd.DataFrame(Counter(emojis).most_common(len(Counter(emojis))))

    return num_messages, words, image_count, video_count, audio_count, len(links), emoji_df

def deEmojify(text):
    regrex_pattern = re.compile(pattern = "["
        u"\U0001F600-\U0001F64F"  # emoticons
        u"\U0001F300-\U0001F5FF"  # symbols & pictographs
        u"\U0001F680-\U0001F6FF"  # transport & map symbols
        u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                           "]+", flags = re.UNICODE)
    return regrex_pattern.sub(r'',text)

def create_wordcloud(selected_user, df):

    df = df[~df['messages'].str.contains('image omitted')]
    df = df[~df['messages'].str.contains('audio omitted')]
    df = df[~df['messages'].str.contains('video omitted')]

    df = df[df['users'] != 'group notification']

    if selected_user != 'Overall':
        df = df[df['users'] == selected_user]

    wc = WordCloud(width=500, height=500, min_font_size=10, background_color='white')

    all_words = df['messages'].str.cat(sep=" ")

    all_words = deEmojify(all_words)
    filtered_words = remove_stopwords(all_words)

    df_wc = wc.generate(filtered_words)

    return df_wc

def user_activity(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['users'] == selected_user]

    msg_per_day = df.groupby('message_date')['messages'].count()

    day_of_week_count = df.groupby('day_of_week')['messages'].count()
    day_of_week_count = day_of_week_count.reindex(index=['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'])

    month_count = df.groupby('month')['messages'].count()
    month_count = month_count.reindex(index=['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December'])

    return msg_per_day, day_of_week_count, month_count




'''
    if selected_user == 'Overall':
        # fetch number of messages
        num_messages = df.shape[0]

        words = []
        for message in df['messages']:
            words.extend(message.split())

        return num_messages, words

    else:
        new_df = df[df['users'] == selected_user]
        num_messages = new_df.shape[0]
        words = []
        for message in new_df['messages']:
            words.extend(message.split())

        return num_messages, words
'''