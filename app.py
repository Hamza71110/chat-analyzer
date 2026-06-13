from matplotlib import pyplot as plt
import preprocessor, helper_functions
import seaborn as sns
import streamlit as st
st.sidebar.title("Chat Analysis")
uploaded_file = st.sidebar.file_uploader("Browse a file")
if uploaded_file is not None:
    bytes_data = uploaded_file.getvalue()
    data = bytes_data.decode("utf-8")
    df = preprocessor.data_preprocess(data)

    # Fetching users in groups provided export chats is from group chat
    user_list = df['users'].unique().tolist()
    user_list.remove('group_notification')
    user_list.sort()
    user_list.insert(0,'Overall')

    selected_user = st.sidebar.selectbox('Show Analysis with',user_list)
    if st.sidebar.button('Start Analysis'):
       #For displaying total number of messages, words, links, and media shared
       num_of_messages, words, links, media = helper_functions.fetch_stats(selected_user,df)
       st.title("Top Analysis")
       col1, col2, col3, col4 = st.columns(4)
       with col1:
           st.header("Total Messages")
           st.title(num_of_messages)
       with col2:
           st.header("Total Words")
           st.title(words)
       with col3:
           st.header("Media Shared")
           st.title(media)
       with col4:
           st.header("Links Shared")
           st.title(links)

       #Monthly base analysis
       st.title("Monthly Analysis")
       timeline = helper_functions.monthly_timeline(selected_user, df)
       fig, ax = plt.subplots()
       ax.plot(timeline['time'],timeline['messages'], color = 'red')
       plt.xticks(rotation='vertical')
       st.pyplot(fig)

       # Daily base analysis
       st.title("Daily Base Analysis")
       daily_timeline = helper_functions.daily_timeline(selected_user, df)
       fig, ax = plt.subplots()
       ax.plot(daily_timeline['only_date'], daily_timeline['messages'], color='blue')
       plt.xticks(rotation='vertical')
       st.pyplot(fig)

       #Activity Map
       st.title("Activity Map")
       col1, col2 = st.columns(2)
       with col1:
           st.header("Most Busy Days")
           busy_day = helper_functions.week_activity_map(selected_user, df)
           fig, ax = plt.subplots()
           ax.bar(busy_day.index, busy_day.values, color='green')
           plt.xticks(rotation='vertical')
           st.pyplot(fig)
       with col2:
           st.header("Most Busy Months")
           busy_month = helper_functions.month_activity_map(selected_user, df)
           fig, ax = plt.subplots()
           ax.bar(busy_month.index, busy_month.values, color='orange')
           plt.xticks(rotation='vertical')
           st.pyplot(fig)

       st.title('Weekly Analysis')
       user_heatmap = helper_functions.activity_heatmap(selected_user, df)
       fig, ax = plt.subplots()
       ax = sns.heatmap(user_heatmap)
       st.pyplot(fig)

       #now finding most busiest users among group chats
       if selected_user == 'Overall':
           st.title("Most Busy Persons")
           x,new_df = helper_functions.most_busy_users(df)
           fig, ax = plt.subplots()
           col1, col2 = st.columns(2)
           with col1:
               ax.bar(x.index, x.values, color='purple')
               plt.xticks(rotation='vertical')
               st.pyplot(fig)
           with col2:
               st.dataframe(new_df)
       # WordCloud
       st.title('WordCloud')
       wc = helper_functions.create_wordcloud(selected_user, df)
       fig, ax = plt.subplots()
       ax.imshow(wc)
       st.pyplot(fig)

       # Most common words used
       m_c_w = helper_functions.most_common_words(selected_user, df)
       fig, ax = plt.subplots()
       ax.barh(m_c_w[0], m_c_w[1], color='yellow')
       plt.xticks(rotation='vertical')
       st.title('Most Common Words')
       st.pyplot(fig)

       #Emoji analysis
       e = helper_functions.emoji_fetch(selected_user, df)
       st.title('Emoji Analysis')
       col1, col2 = st.columns(2)
       with col1:
           st.dataframe(e)
       with col2:
           fig, ax = plt.subplots()
           ax.pie(e[1].head(), labels=e[0].head(), autopct='%0.2f')
           st.pyplot(fig)
