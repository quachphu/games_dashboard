import streamlit as st
import altair as alt
from vega_datasets import data
import pandas as pd
from numerize import numerize
from datetime import datetime

st.set_page_config(
    page_title='PC: Platform Terpopuler Perilisan Game Sepanjang Masa',
    layout='wide',
)

st.markdown("<h1 style='text-align: center;'>PC: Platform Terpopuler Perilisan Game Sepanjang Masa</h1>", unsafe_allow_html=True)
st.markdown("<h6 style='text-align: center; color: grey;'>Data source: Metacritic</h6>", unsafe_allow_html=True)
st.markdown('*Metacritic merupakan suatu situs web yang memberikan informasi tentang review (ulasan) games. Situs ini menyajikan 2 jenis review, yaitu metascore dan userscore. Metascore adalah skor penilaian game yang diberikan oleh para kritikus game terpercaya, sementara Userscore adalah skor penilaian game yang diberikan oleh pengguna atau gamer itu sendiri. Dengan kombinasi kedua jenis skor tersebut, Metacritic memberikan panduan bagi para pecinta game untuk mengevaluasi dan memilih berbagai game yang ingin mereka mainkan.*')

"\n"

df = pd.read_csv('metacritic_scrap.csv')
df['id'] = df['id'].astype('object')
df['release_date'] = pd.to_datetime(df['release_date'])
df['is_online'] = df['is_online'].astype('object')

# game yang paling banyak direview pengguna di pc
pc_popular_game = df.loc[df['platform'] == 'PC'].nlargest(1, 'userscore_review')['title'].iloc[0]
# game yang memiliki review tertinggi di pc
pc_highest_review_score = df.loc[df['platform'] == 'PC'].nlargest(1, ['metascore', 'userscore'])['title'].iloc[0]
# game yang memiliki review terendah di pc
pc_lowest_review_score = df.loc[df['platform'] == 'PC'].nsmallest(1, ['metascore', 'userscore'])['title'].iloc[0]

a, b, c = st.columns(3)
with a:
    st.metric(
        label='Game Terpopuler di PC*',
        value=pc_popular_game
    )
    st.caption('*Berdasarkan banyaknya user yang memberi userscore')
with b:
    st.metric(
        label='Game dengan Review Tertinggi di PC*',
        value=pc_highest_review_score,
    )
    st.caption('*Berdasarkan metascore dan userscore')
with c:
    st.metric(
        label='Game dengan Review Terendah di PC*',
        value=pc_lowest_review_score,
    )
    st.caption('*Berdasarkan metascore dan userscore')

'\n\n'

df['release_year'] = df['release_date'].dt.year
df_count = df.groupby(['platform', 'release_year']).size().reset_index(name='frequency')

line = alt.Chart(df_count[df_count['release_year'] < 2023]).mark_line().encode(
    x=alt.X('release_year', title='Tahun Rilis'),
    y=alt.Y('frequency:Q', title='Jumlah Game yang Dirilis'),
    color='platform',
    tooltip=['platform', 'release_year', 'frequency']
).properties(
    title='Tren Jumlah Perilisan Game pada Berbagai Platform dalam Periode 1994-2022',
)
dots = alt.Chart(df_count[df_count['release_year'] < 2023]).mark_circle(size=50).encode(
    x='release_year',
    y='frequency:Q',
    color='platform',
    tooltip=['platform', 'release_year', 'frequency']
)
c = line + dots
st.altair_chart(c, use_container_width=True)

st.caption('Terdapat variasi jumlah game yang dirilis di platform-platform tersebut selama periode 1994-2022. Terlihat bahwa pada tahun 2008-2011, jumlah game yang dirilis di XBOX berhasil mengungguli PC. Pada tahun 2010, PlayStation 3 juga berhasil menyalip PC. Selain itu, pada tahun 2010-2013, iOS berhasil mengungguli PC. Meskipun demikian, secara keseluruhan, game PC tetap mendominasi dengan jumlah perilisan game yang lebih banyak dibandingkan platform lain sepanjang masa.')

'\n\n'

# Group data by year and platform, count the number of games
df_platform_count = df.groupby(['release_year', 'platform']).size().reset_index(name='game_count')
# Get the top 3 platforms for each year
df_top_platforms = df_platform_count.groupby('release_year').apply(lambda x: x.nlargest(3, 'game_count')).reset_index(drop=True)

chart = alt.Chart(df_top_platforms[(df_top_platforms['release_year'] > 2022-5) & (df_top_platforms['release_year'] < 2023)]).mark_bar().encode(
    x=alt.X('release_year:O', title='Tahun Rilis'),
    y=alt.Y('game_count:Q', title='Jumlah Game yang Dirilis'),
    color='platform:N',
    tooltip=['release_year:O', 'platform:N', 'game_count:Q']
).properties(
    title='Top 3 Platform Perilisan Game dalam 5 Tahun Terakhir',
)
st.altair_chart(chart, use_container_width=True)

st.caption('Grafik di atas menunjukkan bahwa platform PC, PlayStation 4, PlayStation 5, dan Switch mendominasi dalam perilisan game dengan menempati posisi teratas. Perlu dicatat bahwa PlayStation 4, yang sebelumnya menjadi salah satu platform utama yang menggunakan console, telah digantikan oleh generasi terbarunya, yaitu PlayStation 5. Sejak tahun 2022, jumlah perilisan game untuk PlayStation 5 mulai meningkat, meskipun platform tersebut sudah dirilis sejak tahun 2020.')

"\n\n"

# Filter data for the selected platforms
selected_platforms = ['PC', 'PlayStation 4', 'PlayStation 5', 'Switch']
df_selected_platforms = df[df['platform'].isin(selected_platforms)]

# Menentukan rata-rata metascore untuk setiap platform
df_platform_scores = df_selected_platforms.groupby('platform').agg({'metascore': 'mean'}).reset_index()
# Melt the dataframe to long format for visualization
df_scores_long = df_platform_scores.melt(id_vars='platform', var_name='score_type', value_name='score')
# Set order bedasarkan skor rata-rata yang disorting dari terendah
platform_order = df_scores_long.groupby('platform')['score'].mean().sort_values().index.tolist()

chart = alt.Chart(df_scores_long).mark_bar().encode(
    x=alt.X('platform:N', title='Platform', sort=platform_order),
    y=alt.Y('score:Q', title='Skor Rata-Rata'),
    color=alt.Color('platform:N', legend=alt.Legend(title="Platform")),
    column=alt.Column('score_type:N', title='Score Type'),
    tooltip=['platform:N', 'score_type:N', 'score:Q']
).configure_axisX(
    labelAngle=0
).properties(
    title='Perbandingan Rata-Rata Metascore per Platform',
)
st.altair_chart(chart, use_container_width=True)
st.caption('Grafik di atas menunjukkan bahwa PlayStation 4 memiliki rata-rata Metascore terendah, diikuti oleh Nintendo Switch dan PC. Platform PlayStation 5 memiliki rata-rata metascore tertinggi di antara top platform lain. Hal ini menunjukkan bahwa game yang dirilis pada PlayStation 5 memiliki kualitas yang baik dan menarik untuk dimainkan.')
st.caption('Perlu dicatat bahwa meskipun PlayStation 5 dirilis relatif baru pada tahun 2020, tetapi ia telah berhasil mencapai posisi teratas dalam rata-rata Metascore. Hal ini menunjukkan daya tarik yang kuat dari platform tersebut bahwa ia dapat menjadi tujuan pertama perilisan games yang berkualitas. Meskipun demikian, platform PC juga tidak kalah menonjol dari PlayStation 5 dengan menduduki peringkat rata-rata kedua setelah PlayStation 5 dalam hal Metascore. Hal ini menunjukkan bahwa PC juga merupakan platform yang sangat penting dan menarik untuk dimainkan, dengan beragam game berkualitas yang tersedia untuk para penggemar game PC.')