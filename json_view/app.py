# c.f. https://docs.streamlit.io/develop/api-reference/data/st.json
# c.f. https://docs.streamlit.io/develop/api-reference/layout/st.columns

# https://www.kikagaku.co.jp/kikagaku-blog/python-requests/

import streamlit as st
import requests

st.title("HTTPリクエストサンプル")

left, right = st.columns(2)

url = left.text_input("URLを入力してください", "https://jsonplaceholder.typicode.com/posts")

data = {}

with left:
    if st.button("リクエスト送信"):
        try:
            response = requests.get(url)
            response.raise_for_status()  # エラーが発生した場合に例外を発生させる
            st.success("リクエスト成功！")
            st.write("ステータスコード:", response.status_code)

            data = response.json()
        except requests.exceptions.RequestException as e:
            st.error(f"エラーが発生しました: {e}")

right.json(data, expanded=2)
