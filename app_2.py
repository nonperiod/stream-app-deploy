import streamlit as st

# タイトル・テキスト
st.title("Streamlit 基本操作")
st.header("1. 入力パーツ")

# テキスト入力とボタン
user_name = st.text_input("お名前を入力してください")
if st.button("挨拶する"):
    st.success(f"こんにちは、{user_name}さん！")

# スライダーと結果の表示
st.header("2. 数値の操作")
age = st.slider("年齢を選択", 0, 100, 25)
st.write(f"選択された年齢: **{age} 歳**")


# 文字数のカウント
input_message = st.text_input(label="文字数のカウント対象となるテキストを入力してください。")

text_count = len(input_message)

if st.button("実行"):
    st.write(f"文字数: **{text_count}**")


