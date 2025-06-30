# c.f. https://docs.streamlit.io/develop/api-reference/execution-flow/st.dialog
# c.f. https://docs.streamlit.io/develop/api-reference/widgets/st.checkbox
# c.f. https://js2iiu.com/2024/09/07/streamlit-11-api/
# c.f. https://docs.python.org/ja/3/library/secrets.html
# c.f. https://docs.streamlit.io/develop/api-reference/widgets/st.page_link
# c.f. https://docs.streamlit.io/develop/api-reference/caching-and-state/st.session_state
# c.f. https://docs.streamlit.io/develop/api-reference/execution-flow/st.fragment

import streamlit as st
import requests
import secrets

CLIENT_ID = st.secrets["Qiita_CLIENT_ID"]
CLIENT_SECRET = st.secrets["Qiita_CLIENT_SECRET"]

st.title("Qiita API Explorer")

@st.dialog("Available authorizations")
def autholize():
    client_id = st.text_input("client_id:", CLIENT_ID)
    st.write("scopes:")
    scopes = []
    if st.checkbox("read_qiita"):
        scopes.append("read_qiita")
    if st.checkbox("read_qiita_team"):
        scopes.append("read_qiita_team")
    if st.checkbox("write_qiita"):
        scopes.append("write_qiita")
    if st.checkbox("write_qiita_team"):
        scopes.append("write_qiita_team")
    
    state = secrets.token_hex(12)

    baseUrl = "https://qiita.com/api/v2/oauth/authorize"

    if st.button("Autholize"):
        url = f"{baseUrl}?client_id={client_id}&scope={'+'.join(scopes)}&state={state}"
        st.session_state.url = url
        st.rerun()
    if st.button("Close"):
        st.rerun()

@st.fragment
def autholize_with_qiita():
    if "url" not in st.session_state:
        if st.button("Autholize with Qiita"):
            autholize()
    else:
        st.page_link(st.session_state.url, label="Get AccessToken")

    if "code" in st.query_params:
        code = st.query_params["code"]
        request_body = {
            "client_id": CLIENT_ID,
            "client_secret": CLIENT_SECRET,
            "code": code
        }

        try:
            response = requests.post("https://qiita.com/api/v2/access_tokens", json=request_body)
            response.raise_for_status()  # エラーが発生した場合に例外を発生させる

            st.success("認証に成功しました！")
            st.write("ステータスコード:", response.status_code)
            st.json(response.json())

            st.query_params.clear()

            st.session_state.token = response.json()["token"]

        except requests.exceptions.RequestException as e:
            st.error(f"エラーが発生しました: {e}")

autholize_with_qiita()


if "token" in st.session_state:
    if st.button("Get User Info"):
        try:
            headers = {"Authorization": f"Bearer {st.session_state.token}"}
            res = requests.get("https://qiita.com/api/v2/authenticated_user", headers=headers)
            res.raise_for_status()

            st.json(res.json())
            st.session_state.id = res.json()["id"]

        except requests.exceptions.RequestException as e:
            st.error(f"エラーが発生しました: {e}")

st.json(st.session_state)

"""
if "id" in st.session_state:
    if st.button("Get Stock List"):
        try:
            user_id = st.session_state.id
            page = 1
            per_page = 100
            headers = {"Authorization": f"Bearer {st.session_state.token}"}
            res = requests.get(f"https://qiita.com/api/v2/users/{user_id}/stocks?page={page}&per_page={per_page}", headers=headers)
            res.raise_for_status()

            st.json(res.json())
        except requests.exceptions.RequestException as e:
            st.error(f"エラーが発生しました: {e}")
"""