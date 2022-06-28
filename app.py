import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st
import preprocessor
import helper
import seaborn as sns

st.sidebar.title("Whatsapp Chat Analyser")
uploaded_file = st.sidebar.file_uploader("Choose a file")

if uploaded_file is not None:
    bytes_data = uploaded_file.getvalue()
    data = bytes_data.decode("utf-8")
    df = preprocessor.preprocess(data)
    st.dataframe(df)

    # fetch unique users
    user_list = df['users'].unique().tolist()
    if 'group notification' in user_list:
        user_list.remove("group notification")
    user_list.sort()
    user_list.insert(0, "Overall")
    selected_user = st.sidebar.selectbox("Show analysis wrt to", user_list)

    if st.sidebar.button("Show Analysis"):

        num_messages, words, image_count, video_count, audio_count, links, emoji_df = helper.fetch_stats(selected_user, df)

        col1, col2, col3, col4, col5, col6 = st.columns(6)

        with col1:
            st.subheader("Total Messages")
            st.subheader(num_messages)

        with col2:
            st.subheader("Total Words")
            st.subheader(len(words))

        with col3:
            st.subheader("Media Files shared")
            st.subheader(image_count)

        with col4:
            st.subheader("Video Files shared")
            st.subheader(video_count)

        with col5:
            st.subheader("Audio Files Shared")
            st.subheader(audio_count)

        with col6:
            st.subheader("Total Links shared")
            st.subheader(links)

        st.title('Emoji Analysis')
        col1, col2 = st.columns(2)

        with col1:
            st.dataframe(emoji_df)

        with col2:
            fig, ax = plt.subplots()
            ax.pie(emoji_df[1].head(), labels = emoji_df[0].head(), autopct="%0.2f")
            st.pyplot(fig)



        # Finding busiest person
        if selected_user == 'Overall':
            st.title('Most busy users')

            user_dict = df['users'].value_counts()
            user_df = round(df['users'].value_counts()/df.shape[0]*100, 2).reset_index().rename(columns={'index': 'name', 'users': 'percent'})
            fig, ax = plt.subplots()
            col1, col2 = st.columns(2)

            with col1:
                ax.bar(user_dict.index, user_dict.values, color = 'red')
                plt.xticks(rotation='vertical')
                plt.xlabel('User')
                plt.ylabel('Percentage Activity')
                st.pyplot(fig)

            with col2:
                st.dataframe(user_df)


        if selected_user != 'Overall':
            df = df[df['users'] == selected_user]

        st.title('Activity')

        col1, col2 = st.columns(2)
        msg_per_day, day_of_week_count, month_count = helper.user_activity(selected_user, df)

        with col1:
            fig, ax = plt.subplots(figsize=(10, 10))
            st.write(sns.violinplot(x='day_of_week', y='hour', data=df, order=['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']))
            ax.set_xticklabels(['Mon', 'Tue', 'Wed', 'Thur', 'Fri', 'Sat', 'Sun'])
            st.pyplot(fig)

        with col2:
            fig, ax = plt.subplots(figsize=(10, 10))
            ax.plot(msg_per_day[1:])
            st.pyplot(fig)

        col1, col2 = st.columns(2)

        with col1:
            fig, ax = plt.subplots()
            ax.bar(day_of_week_count.index, day_of_week_count.values, color='green')
            plt.xticks(rotation='vertical')
            plt.xlabel('Day of the Week')
            plt.ylabel('Percentage Activity')
            st.pyplot(fig)
        #st.line_chart(timeline_dict, width=5, height=0)

        with col2:
            fig, ax = plt.subplots()
            ax.bar(month_count.index, month_count.values, color='orange')
            plt.xticks(rotation='vertical')
            plt.xlabel('Day of the Week')
            plt.ylabel('Percentage Activity')
            st.pyplot(fig)

        st.title('Your Word Cloud')
        df_wc = helper.create_wordcloud(selected_user, df)
        fig, ax = plt.subplots()
        ax.imshow(df_wc)
        st.pyplot(fig)
