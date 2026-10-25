import streamlit as st
import pandas as pd
import duckdb as ddb

data = {"a": [1, 2, 3], "b":[4, 5, 6]}
df = pd.DataFrame(data)
st.write("Spaced Repetition System SQL review")

option = st.selectbox("What would you like to review",
    ["Joins", "GroupBy", "Window Functions"],
    index=None,
    placeholder="Select a theme")

st.write(option)

tab1, = st.tabs(["G"])

with tab1:
    st.write(df)
    query = st.text_area(label="Input query SQL")

    dftest = ddb.sql(query)
    st.write(dftest)









