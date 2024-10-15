# c.f. https://docs.streamlit.io/develop/api-reference/widgets/st.file_uploader
# https://docs.streamlit.io/develop/api-reference/write-magic/st.write

import streamlit as st
import pandas as pd

# TODO: ファイル設定(区切り文字とか文字コードとか)

uploaded_file = st.file_uploader("Choose a file")
if uploaded_file is not None:
    # Can be used wherever a "file-like" object is accepted:
    dataframe = pd.read_csv(uploaded_file)
    st.write(dataframe)