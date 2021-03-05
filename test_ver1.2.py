
# -*- coding: utf-8 -*-

import sys


import pandas as pd
import streamlit as st

import numpy as np
import sqlite3

# 文字化けを防ぐおまじない
# reload(sys)
# sys.setdefaultencoding('utf8')

# SQLiteにつなげる際のみに使う
# conn = sqlite3.connect('database_test4.db')
# c = conn.cursor()

# テーブルを作成

# c.execute('CREATE TABLE articles(schools_name text, address text, experience_year_play int, number_of_student int)')
#
# conn.close()

########################以下、本番のアプリ部分##########################

st.title('あなたの教室 How much α版 ver1.1')
st.header("【アプリ概要】"
          "  \n【想定ユーザー】"
          "  \n　その1:音楽教室運営を行っている人"
          "  \n　その2:音楽教室運営をこれから行いたいと考えている人"
          "  \n【出来ること】"
          "  \n　その1:お住まいの市区町村における音楽教室数や音楽教室の価格情報を入手できます。"
          "  \n　その2:約1300件のデータを元に簡易AIがあなたの音楽教室の適正価格を提案します。"
          "  \n【ご容赦頂きたいこと】"
          "  \n　その1:プログラミング初心者が作成してます。"
          "  \n　その2:不具合しかございません。そのうちアップデートしていきます。")

st.header("【近隣の音楽教室数や音楽教室の価格情報を入手】"
             "  \n下記項目をご記入ください。")

school_name = st.text_input("▼教室名▼")

name_city = st.text_input("▼教室住所▼(市もしくは区のみを入れてください。例：港区, 枚方市)")

name_city_with_prefecture = st.text_input("▼教室住所_都道府県▼(都道府県も入れてください。例：東京都港区, 大阪府枚方市)")

if st.button("▼お住まいの市区町村の音楽教室情報を知る▼"):

#############市区町村別の音楽教室情報################

    # ファイルを読み込む
    #
    # music_school_df = pd.read_excel("pivot_data_music_school.xls")
    # populations = pd.read_excel("市区町村別人口.xlsx")
    col_names_for_pivot_data = ['formed_address', 'number_of_schools', 'average_price', 'max_price', 'min_price']

    music_school_df = pd.read_csv("pivot_data_music_school.csv", names = col_names_for_pivot_data)
    populations = pd.read_csv("市区町村別人口.csv")

    # 市区町村平均人口の算出

    average_population_in_japan = populations["人口数"].mean()

    # 市区町村の人口算出

    population_in_the_city = populations[populations[
        "市区町村"].isin([name_city])]["人口数"]

    # 市区町村の平均年齢の算出

    average_age_in_the_city = populations[populations[
        "市区町村"].isin([name_city])]["平均年齢"]

    # expanderで情報を表示させていく。
    #　人口を表示させる。
    expander_population = st.beta_expander(name_city + 'の人口を知る')
    expander_population.write(population_in_the_city)

    # 平均年齢を表示させる。
    expander_ages = st.beta_expander(name_city + 'の平均年齢を知る')
    expander_ages.write(average_age_in_the_city)

    #
    # st.write("全国平均人口", average_population_in_japan)
    #
    # # 平均年齢の表示
    # st.write("全国平均年齢", 48.36)

    number_of_population = music_school_df[music_school_df[
        "formed_address"].isin([name_city_with_prefecture])]["number_of_schools"]

    number_of_music_school = music_school_df[music_school_df[
        "formed_address"].isin([name_city_with_prefecture])]["number_of_schools"]

    average_price = music_school_df[music_school_df[
        "formed_address"].isin([name_city_with_prefecture])]["average_price"]

    min_price = music_school_df[music_school_df[
        "formed_address"].isin([name_city_with_prefecture])]["min_price"]

    max_price = music_school_df[music_school_df[
        "formed_address"].isin([name_city_with_prefecture])]["max_price"]

    # 音楽教室の数を表示させる。
    expander_number_of_music_schools = st.beta_expander(name_city + 'の音楽教室の数を知る')
    expander_number_of_music_schools.write(number_of_music_school)

    average_price = average_price.values
    min_price = min_price.values
    max_price = max_price.values

    price_list = [61.93, 20.63, 200.00]
    df = pd.DataFrame(price_list, index=['average_price', 'min_price', 'max_price'],
                      columns=['全国の教室価格情報'])
    #
    # st.write('全国の教室価格情報', df)

    price_list_in_the_area = [average_price, min_price, max_price]
    df_in_the_area = pd.DataFrame(price_list_in_the_area, index=['average_price', 'min_price', 'max_price'],
                                  columns=[name_city_with_prefecture])

    expander_schools_price = st.beta_expander(name_city + 'のレッスン価格(円)/1分　を知る')
    expander_schools_price.write(df_in_the_area)


    # st.write('あなたの市区町村の教室価格情報', df_in_the_area)
    # グラフ化させる。
    # fig = plt.figure(figsize=(6.4, 4.8))
    # ax = fig.add_subplot(111, xlabel=df_in_the_area.index.name, ylabel=df_in_the_area[name_city_with_prefecture].name)
    # ax.bar(df_in_the_area.index, df_in_the_area[name_city_with_prefecture])
    # st.pyplot(fig)

    st.write('【市町村別音楽教室データ(ご参考)】', music_school_df)

    st.write('【市町村別統計情報(ご参考)】', populations)

##########################価格に効く情報を獲得する##########################

st.header("【「" + school_name + "」教室の適正価格を提案してもらう】"
                               "  \n下記項目をご記入ください。")

coaching_records = st.number_input("▼指導歴▼",
                                           min_value = 0,
                                           max_value = 100,
                                           value = 0,
                                           step = 1)

childminder = st.radio("▼保育士志望の顧客もターゲットの対象としていますか▼",
                               ('はい', 'いいえ'))

if childminder == "はい":
    childminder = 1
else:
    childminder = 0

kindergarten = st.radio("▼幼稚園教諭志望の顧客もターゲットの対象としていますか▼",
                                ('はい', 'いいえ'))

if kindergarten == "はい":
    kindergarten = 1
else:
    kindergarten = 0

vocal_music = st.radio("▼声楽コースをご用意されていますか▼",
                               ('はい', 'いいえ'))

if vocal_music == "はい":
    vocal_music = 1
else:
    vocal_music = 0

beginner = st.radio("▼初心者をターゲットの対象としていますか▼",
                            ('はい', 'いいえ'))

if beginner == "はい":
    beginner = 1
else:
    beginner = 0

world_competition = st.radio("▼コンクール(世界)の入賞経験がありますか▼",
                                     ('はい', 'いいえ'))

if world_competition == "はい":
    world_competition = 1
else:
    world_competition = 0

#東京芸術大学は質問のみ。計算式には組み込まない。
tokyo_university = st.radio("▼東京藝術大学/大学院のご出身ですか▼",
                                    ('はい', 'いいえ'))


toho_university = st.radio("▼桐朋音学大学/大学院のご出身ですか▼",
                                   ('はい', 'いいえ'))

if toho_university == "はい":
    toho_university = 1
else:
        toho_university = 0

tokyo_university = st.radio("▼東京音学大学/大学院のご出身ですか▼",
                                    ('はい', 'いいえ'))

if tokyo_university == "はい":
    tokyo_university = 1
else:
    tokyo_university = 0


composition = st.radio("▼作曲コースをご用意されていますか▼",
                               ('はい', 'いいえ'))

if composition == "はい":
    composition = 1
else:
    composition = 0

study_abroad = st.radio("留学のご経験はありますか▼",
                                ('はい', 'いいえ'))

if study_abroad == "はい":
    study_abroad = 1
else:
    study_abroad = 0


#######################
#我々の欲しい情報を獲得する#
#######################

# レッスン稼働可能時間の記入をしてもらう
available_lesson_time = st.number_input("▼レッスン稼働が可能な時間/(週)▼",
                                                    min_value=0,
                                                    max_value=100,
                                                    value=0,
                                                    step=1)

expander_lesson_time = st.beta_expander('レッスン稼働が可能な時間とは？')
expander_lesson_time.write("レッスン稼働が可能な時間とは・・・"
                           "  \n「" + school_name + "」教室様がレッスンを行うために確保している時間の合計/(週)です。"
                                                   "  \n例えば、下記の時間で運営をしている教室の場合。"
                                                   "  \n"
                                                   "  \n【有井音楽教室_運営時間(例)】"
                                                   "  \n平日　:10時~17時"
                                                   "  \n土曜日:10時~18時""  \n日曜日:定休日"
                                                   "  \n"
                                                   "  \nレッスン稼働可能枠 = 平日運営時間 + 土曜日運営時間 となりますので"
                                                   "  \n43(時間) = 5(日間)×7(時間) + 1(日間)×8(時間)"
                                                   "  \n有井教室のレッスン稼働が可能な時間は、43時間になります。"
                           )


# 稼働時間の記入をしてもらう
operating_time = st.number_input("▼稼働時間/(週)▼",
                                             min_value=0,
                                             max_value=100,
                                             value=0,
                                             step=1)

expander_operating_time = st.beta_expander('稼働時間とは？')
expander_operating_time.write("稼働時間とは・・・"
                              "  \n「"+ school_name + "」教室様が現在レッスンを実施している時間の合計/(週)です。"
                                                  "  \nつまり、実際にレッスンを行っている時間のみを指します。"
                                                  "  \n例えば、下記の時間で運営をしている教室の場合。"
                                                  "  \n"
                                                  "  \n【有井音楽教室_運営時間(例)】"
                                                  "  \n平日　:10時~17時"
                                                  "  \n土曜日:10時~18時"
                                                  "  \n日曜日:定休日"
                                                  "  \n"
                                                  "  \n【有井音楽教室_レッスン実施時間(例)】"
                                                  "  \n平日　:17時~19時,"
                                                  "  \n土曜日:12時~17時"
                                                  "  \n日曜日:定休日"
                                                  "  \n"
                                                  "  \n上記のうち平日の例でいうと、レッスン実施時間は17時~19時です。"
                                                  "  \n従って、平日での稼働時間は、17時~19時となります。1週間あたりを計算すると"
                                                  "  \n稼働時間 = 平日稼働時間 + 土曜日稼働時間 ですので。"
                                                  "  \n15(時間) = 5(日間)×2(時間) + 1(日間)×5(時間)　となります。"
                                                  "  \n有井教室の稼働時間は、15時間になります。")


number_of_students = st.number_input("▼生徒数▼",
                                                 min_value=0,
                                                 max_value=100,
                                                 value=0,
                                                 step=1)

lesson_minutes = st.number_input("▼レッスン時間/1レッスン▼",
                                         min_value = 0,
                                         max_value = 240,
                                         value = 0,
                                         step = 1)


lesson_times = st.number_input("▼1カ月のレッスン回数/1人あたり▼",
                                       min_value = 0,
                                       max_value = 240,
                                       value = 0,
                                       step = 1)

price_par_lesson = st.number_input("▼レッスン金額/1レッスンあたり▼",
                                   min_value = 0,
                                   max_value = 100000,
                                   value = 0,
                                   step = 1)


if st.button("▼価格を診断する▼"):
    lesson_price = price_par_lesson / lesson_minutes
    intercept = 59.24843864264586
    explanatory_variable = (intercept +
                            coaching_records*(-0.057814) +
                            childminder*(-2.629911)+
                            kindergarten*(-1.114511)+
                            vocal_music*(-0.475124)+
                            beginner*(2.028346)+
                            world_competition*(2.835193)+
                            toho_university*(11.601225)+
                            tokyo_university*(-0.535470)+
                            composition*(4.651286)+
                            study_abroad*(9.124657))
    #
    # music_school_df = pd.read_excel("/Users/ariikeisuke/Desktop/Datamix_ver1.2/市町村別人口/pivot_data_music_school.xlsx")

    number_of_population = music_school_df[music_school_df[
        "formed_address"].isin([name_city_with_prefecture])]["number_of_schools"]

    number_of_music_school = music_school_df[music_school_df[
        "formed_address"].isin([name_city_with_prefecture])]["number_of_schools"]

    average_price = music_school_df[music_school_df[
        "formed_address"].isin([name_city_with_prefecture])]["average_price"]

    min_price = music_school_df[music_school_df[
        "formed_address"].isin([name_city_with_prefecture])]["min_price"]

    max_price = music_school_df[music_school_df[
        "formed_address"].isin([name_city_with_prefecture])]["max_price"]

    price_predict = st.write('あなたの教室の予測価格(円)/月額　は',round(explanatory_variable*lesson_minutes*lesson_times))
    st.write('あなたの教室の予測価格(円)/1分あたり　は', round(explanatory_variable))
    st.write('あなたの教室の現状価格(円)/月額　は', round(lesson_price*lesson_minutes*lesson_times))
    st.write('あなたの教室の現状価格(円)/1分あたり　は',  round(lesson_price))
    st.write('近隣の音楽教室の平均価格(1分あたり)', round(average_price))
    st.write('近隣の音楽教室の最安価格(1分あたり)', round(min_price))
    st.write('近隣の音楽教室の最高価格(1分あたり)', round(max_price))

    st.write("【▼価格の計算について】"
             "  \n  ・計算に使用したデータはいくつかのwebサイトから引っ張ってきた教室データとなります。"
             "  \n  ・”だいいみんなこのぐらいの価格をつけるのか”と眺めていただければと思います。"
             "  \n  ・アプリに情報を入れて頂くと予測精度がどんどんあがります！")

    ######データへの格納テスト######

    # conn = sqlite3.connect('database_test4.db')
    # # カーソルを取得
    # c = conn.cursor()
    # # c.execute('CREATE TABLE articles(schools_name text, address text, experience_year_play int, number_of_student int)')
    # c.execute("INSERT INTO articles(schools_name, address, experience_year_play, number_of_student) values(?,?,?,?)",
    #           [school_name, name_city_with_prefecture, play_experience, number_of_students])
    #     # コミット
    # conn.commit()
    # #     # コネクションをクローズ
    # conn.close()


