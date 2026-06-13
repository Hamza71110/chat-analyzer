import pandas as pd
import calendar
import re
import seaborn as sns
import emoji

from collections import Counter
import stop_words
from wordcloud import WordCloud
import matplotlib.pyplot as plt
from urlextract import URLExtract
extract = URLExtract()

def fetch_stats(selected_user,df):
    if selected_user != 'Overall':
        df = df[df['users'] == selected_user]
    # Total Number of Messages
    num_of_msg=df.shape[0]
    # Total Number of Words
    words = []
    for msg in df['messages']:
        words.extend(msg.split())

   #Fetching Media Related Messages
    num_of_media_msg=df[df['messages']=='<Media omitted>\n'].shape[0]

   # Fetching Links
    links=[]
    for msg in df['messages']:
        links.extend(extract.find_urls(msg))
    return num_of_msg, len(words), num_of_media_msg,len(links)

def most_busy_users(df):
    x = df['users'].value_counts().head()
    df=round((df['users'].value_counts()/len(df))*100,2).reset_index().rename(columns={'index':'name','user':'percentage'})
    return x, df

def create_wordcloud(selected_user,df):
    f = open('stop_hinglish.txt','r', encoding='utf-8')
    stopwords = set(f.read().split())
    if selected_user != 'Overall':
        df = df[df['users'] == selected_user]
    temp = df[
        (df['users'] != 'group_notification') &
        (~df['messages'].str.contains('media omitted', case=False, na=False))
        ].copy()

    def clean_text(text):
        text = str(text).lower()
        # remove URLs
        text = re.sub(r'http\S+|www\.\S+', '', text)
        return text

    temp['messages'] = temp['messages'].apply(clean_text)
    def remove_stopwords(message):
        y = []
        for word in message.lower().split():
            if word not in stopwords:
                y.append(word)
        return " ".join(y)

    wc = WordCloud(width=500, height=500, min_font_size=10, background_color='white')
    temp['messages'] = temp['messages'].apply(remove_stopwords)
    text = " ".join(temp['messages'].astype(str))
    return wc.generate(text)

def most_common_words(selected_user,df):
    f = open('stop_hinglish.txt','r')
    stop_words = f.read()
    if selected_user != 'Overall':
        df = df[df['users'] == selected_user]
    temp = df[df['users'] != 'group_notification']
    temp = temp[temp['messages']!='<Media omitted>\n']
    words = []
    for msg in temp['messages']:
        for word in msg.lower().split():
            if word not in stop_words:
                words.append(word)
    most_common_words_df = pd.DataFrame(Counter(words).most_common(20))
    return most_common_words_df


def emoji_fetch(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['users'] == selected_user]
    emojiz = []
    for msg in df['messages']:
        msg = str(msg)
        for c in msg:
            if c in emoji.EMOJI_DATA:
                emojiz.append(c)
    emoji_df = pd.DataFrame(Counter(emojiz).most_common(len(Counter((emojiz)))))
    return emoji_df

def monthly_timeline(selected_user,df):
    if selected_user != 'Overall':
        df = df[df['users'] == selected_user]
    timeline = df.groupby(['year','month']).count()['messages'].reset_index()
    time = []
    for i in range(timeline.shape[0]):
        time.append(str(timeline['month'].iloc[i]) + '-' + str(timeline['year'].iloc[i]))
    timeline['time'] = time
    return timeline

def daily_timeline(selected_user,df):
    if selected_user != 'Overall':
        df = df[df['users'] == selected_user]
    daily_time = df.groupby(['only_date']).count()['messages'].reset_index()
    return daily_time

def week_activity_map(selected_user,df):
    if selected_user != 'Overall':
        df = df[df['users'] == selected_user]
    return df['day'].value_counts()

def month_activity_map(selected_user,df):
    if selected_user != 'Overall':
        df = df[df['users'] == selected_user]
    return df['month'].value_counts()

def activity_heatmap(selected_user,df):
    if selected_user != 'Overall':
        df = df[df['users'] == selected_user]
    activity_map = df.pivot_table(index='day', columns='month', values='messages', aggfunc='count').fillna(0)
    return activity_map