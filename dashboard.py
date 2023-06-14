import sys
import subprocess
# installing new package here because requirements.txt for streamlit_option_menu has error with dependency 
name = 'streamlit_option_menu'
if name in sys.modules:
    print(f"{name!r} already in sys.modules")
else:
    subprocess.check_call([sys.executable, "-m", "pip", "install", 'streamlit_option_menu']) 

import streamlit as st
import altair as alt
import pandas as pd
from streamlit_option_menu import option_menu

st.set_page_config(
    page_title='PC: Platform Terpopuler Perilisan Game Sepanjang Masa',
    layout='wide',
)

selected = option_menu(
    None, 
    ["Background", "Data Collecting",  "Data Overview", 'Analysis'], 
    icons=['house', 'arrows-angle-contract', "eye", 'graph-up'], 
    menu_icon="cast", default_index=0, orientation="horizontal",
    styles={
        "container": {"padding": "0px!important", "background-color": "#fafafa", "font-family":"arial", "letter-spacing":"0.5px"},
        "icon": {"color": "orange", "font-size": "18px"}, 
        "nav-link": {"font-size": "18px", "text-align": "center", "padding":"10px", "margin":"0px", "--hover-color": "#eee", "color": "#2b2b2b"},
        "nav-link-selected": {"background-color": "#E3476C"},
    }
)

st.markdown("<h1 style='text-align: center;'>PC: Platform Terpopuler Perilisan Game Sepanjang Masa</h1>", unsafe_allow_html=True)
st.markdown("<h6 style='text-align: center; color: grey;'>Data Source: Metascrap (Scraped on June 9, 2023)</h6>", unsafe_allow_html=True)

"\n\n"

if selected == 'Background':
    background = '''
        Saat ini, terdapat beragam jenis platform yang tersedia untuk bermain game, termasuk PC, PlayStation, Nintendo Switch, XBOX, dan berbagai platform lainnya. Meskipun sebagian besar platform tersebut membutuhkan konsol gaming yang sederhana dan mudah digenggam, platform PC tetap menjadi pilihan yang populer bagi mayoritas pengguna dalam bermain game. Hal ini dapat dijelaskan oleh keunggulan yang dimiliki oleh PC itu sendiri. Berikut ini adalah beberapa alasan yang mendasari mengapa banyak orang lebih memilih menggunakan PC daripada konsol gaming.\n
        1. Hardware pada PC mudah untuk **_dikustomisasi_**. Misalnya, pengguna dapat mengupgrade komponen perangkat dengan mudah, seperti GPU, RAM, SSD guna meningkatkan performa perangkat agar sesuai dengan requirement terbaru game, tanpa perlu membeli perangkat baru.
        2. **_Kendali game_** lebih nyaman menggunakan keyboard dan mouse. Misalnya, game tembak-tembakan lebih nyaman dimainkan menggunakan keyboard dan mouse. Bahkan pada game lain, pengguna dapat menambahkan joystick sendiri jika diperlukan.
        3. Pengguna dapat **_menambahkan mod_** pada game untuk memperoleh pengalaman yang lebih menarik dari bermain game tersebut.
        4. Banyak **_game gratis_** yang resmi untuk dimainkan di PC.
        5. PC menawarkan **_fungsional yang beragam_**. Selain untuk bermain game, PC juga dapat membantu menyelesaikan pekerjaan seperti menulis dokumen.

        Sedangkan, keunggulan dari konsol gaming yang membuatnya tidak kalah populer adalah:
        1. Pengguna tidak perlu memeriksa kesesuaian **_spek hardware_** dengan requirement game.
        2. Dapat dimainkan dengan **_posisi yang fleksibel_**, seperti dalam keadaan duduk di sofa.
        3. Konsol gaming saat ini telah dilengkapi dengan **_fitur hiburan_** lain seperti pemutar TV, musik, gambar, dan fitur-fitur lainnya.
        4. Terkadang game tertentu hanya dirilis secara **_eksklusif_** untuk platform yang menggunakan konsol gaming, bukan PC.
        5. Umumnya harga konsol gaming **_lebih murah_** daripada PC yang diperuntukkan untuk gaming.
    '''
    st.markdown(background)

    "\n\n"

    hipotesis = """
        <div style='
            display: grid;
            border: 1px solid #E3476C;
            padding: 20px 25px;
            margin: 0 15% 50px;
            align-items: center;'>
            <h2 style='text-align: center; margin: 0 0 10px 0; padding: 0;'>Hipotesis</h2>
            <p style='text-align: center; margin:0px; padding:0px;'><i>Berdasarkan fenomena kepopuleran platform PC untuk bermain game ini, berikut hipotesis yang ingin dibuktikan:</i></p>
            <p style='text-align: center; font-size: 20px; font-weight: bold; margin:0px; padding:0px;'>\"Semakin hari, jumlah game yang dirilis pada platform PC akan semakin meningkat.\"</p>
        </div>
    """
    st.markdown(hipotesis, unsafe_allow_html=True)
    
    transition = '''
        Selanjutnya, hipotesis tersebut akan dibuktikan pada halaman 'Analysis'. Pada halaman tersebut pula, akan digali berbagai insight lainnya terkait popularitas PC sebagai platform perilisan games.
        Namun, untuk membantu penelusuran insight tersebut, berikut disajikan rumusan masalah yang dapat menjadi arahan untuk melakukan proses analisis pada tahap berikutnya.
    '''
    st.markdown(transition)

    rumusan = '''

    '''

elif selected == 'Analysis':

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

    st.caption('Grafik di atas menunjukkan bahwa platform PC, PlayStation 4, PlayStation 5, dan Switch mendominasi dalam perilisan game dengan menempati posisi teratas. Perlu dicatat bahwa PlayStation 4, yang sebelumnya menjadi salah satu platform utama yang menggunakan konsol, telah digantikan oleh generasi terbarunya, yaitu PlayStation 5. Sejak tahun 2022, jumlah perilisan game untuk PlayStation 5 mulai meningkat, meskipun platform tersebut sudah dirilis sejak tahun 2020.')

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

elif selected == 'Data Overview':
    st.markdown('*Metacritic merupakan suatu situs web yang memberikan informasi tentang review (ulasan) games. Situs ini menyajikan 2 jenis review, yaitu metascore dan userscore. Metascore adalah skor penilaian game yang diberikan oleh para kritikus game terpercaya, sementara Userscore adalah skor penilaian game yang diberikan oleh pengguna atau gamer itu sendiri. Dengan kombinasi kedua jenis skor tersebut, Metacritic memberikan panduan bagi para pecinta game untuk mengevaluasi dan memilih berbagai game yang ingin mereka mainkan.*')


"\n\n"
st.markdown("<h6 style='text-align: center; color: grey;'>By: Hikmawati Fajriah Ayu Wardana (<a href = 'mailto: hf.ayuwardana@gmail.com'>hf.ayuwardana@gmail.com</a>)</h6>", unsafe_allow_html=True)