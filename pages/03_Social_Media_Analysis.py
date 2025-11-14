import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import date, timedelta, datetime

# The actual page content is executed here by Streamlit
st.title("📱 Student 03: Social Media Analysis")
st.markdown("---")

# Retrieve shared data from the Home page's session state
if 'student_data' not in st.session_state or st.session_state['student_data']['st03_df'].empty:
    st.warning("Data not loaded. Please ensure the main Home Page ran successfully and the data files exist.")
else:
    df = st.session_state['student_data']['st03_df']

    # --- Student Introductory Section ---
    st.header("1. Introduction and Project Goal")
    st.markdown("""
        **Data Description:** This dataset contains **wikipedia pageviews** for eight different social media platforms from 2017 - 2022.
        
        **Research Question:** How has **engagement** with **social media companies** fluncuated over the years, based on **Wiki pageviews** in the years 2017 - 2022?
        
        **Interaction:** Use the selection box below to choose which social media platform to display on the line graph below. You can keep all datasets in display or choose to specifically compare certain platforms.
    """)
    st.markdown("---")
    
    # --- 2. Data Preparation ---
    qid_to_platform = {
        'Q209330': 'Instagram',
        'Q48938223': 'TikTok',
        'Q355': 'Facebook',
        'Q170726': 'Snapchat',
        'Q866': 'Youtube',
        'Q4555537': 'Twitch',
        'Q918': 'Twitter',
        'Q1049511': 'WhatsApp'
    }
    df['platform'] = df['qid'].map(qid_to_platform)
    df['views'] = df['views'].astype(int)
    df['date'] = pd.to_datetime(df['date'])

    df_monthly = (
        df.groupby(['platform', pd.Grouper(key='date', freq='M')])['views']
        .sum()
        .reset_index()
    )

    # --- 3. Platform Filter ---
    selected_platforms = st.multiselect(
        "Select social media platforms to display:",
        options=df_monthly['platform'].unique(),
        default=df_monthly['platform'].unique()
    )

    selected_years = st.slider(
        "Select date range of wikipedia pageviews to display:",
        min_value = date(2017, 2, 9),
        max_value= date(2021, 12, 31),
        value = (date(2017, 2, 9), date(2021, 12, 31)),
        step = timedelta(days=30),
        key='a2_bin_slider'
    )

    min_selected, max_selected = selected_years

    min_selected = datetime.combine(min_selected, datetime.min.time())
    max_selected = datetime.combine(max_selected, datetime.max.time())


    filtered_df = df_monthly[
        (df_monthly['platform'].isin(selected_platforms)) &
        (df_monthly['date'] >= min_selected) &
        (df_monthly['date'] <= max_selected)
    ]

    # --- 4. Plotly Line Chart ---
    st.subheader("2. Monthly Wikipedia Pageviews by Platform (2017–2022)")
    st.write(f"**Displaying data from {min_selected.strftime('%Y-%m-%d')} to {max_selected.strftime('%Y-%m-%d')}**")

    fig = px.line(
        filtered_df,
        x="date",
        y="views",
        color="platform",
        title="How has engagement with social media companies fluctuated<br>based on Wiki pageviews",
        labels={
            "date": "Years (Monthly)",
            "views": "Pageviews (Millions)",
            "platform": "Platform"
        },
        color_discrete_map={
            'Instagram': '#E193ED',
            'TikTok': "#D92076",
            'Youtube': 'red',
            'Facebook': "#156EC8",
            'Twitter': "#33C6EF",
            'Twitch': "#8133EF",
            'Snapchat': 'yellow',
            'WhatsApp': 'green'
        },
        template="plotly_white"
    )

    fig.update_layout(
        legend_title_text="Platform",
        legend=dict(x=1, y=1),
        margin=dict(t=80, b=40),
        height=500
    )

    st.plotly_chart(fig, use_container_width=True)

    if df_monthly.empty:
        st.info(f"No pageviews found")
    else:
        st.subheader(f"Pageviews for each platform from {min_selected.strftime('%Y-%m-%d')} to {max_selected.strftime('%Y-%m-%d')}")
        
        result_counts = (
        filtered_df.groupby('platform')['views']
        .sum()
        .sort_values(ascending=False)
        .reset_index()
        )

        # Display as a small table
        st.table(result_counts)
