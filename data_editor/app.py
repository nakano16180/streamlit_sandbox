# c.f. https://docs.streamlit.io/develop/api-reference/data/st.data_editor
# c.f. https://zenn.dev/tatsurokawamoto/articles/f3f18e0d12ad78

import streamlit as st
import pandas as pd

df = pd.DataFrame([{"column 1": "st.selectbox", "column 2": 3}])
edited_df = st.data_editor(df, num_rows="dynamic") # 👈 An editable dataframe