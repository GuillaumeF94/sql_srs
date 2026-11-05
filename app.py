# pylint: disable=missing-module-docstring


import io

import duckdb as ddb
import pandas as pd
import streamlit as st

CSV = """
beverage,price
orange_juice,2.5
Espresso,2
Tea,3
"""

CSV2 = """
food_item,food_price
cookie,2.5
chocolatine,2
muffin,3
"""

beverages = pd.read_csv(io.StringIO(CSV))
food_items = pd.read_csv(io.StringIO(CSV2))

ANSWER_STR = """
SELECT * FROM beverages
CROSS JOIN food_items
"""

solution_df = ddb.sql(ANSWER_STR).df()

with st.sidebar:
    option = st.selectbox(
        "What would you like to review",
        ["Joins", "GroupBy", "Window Functions"],
        index=None,
        placeholder="Select a theme",
    )

    st.write(option)

st.header("Enter your code")
query = st.text_area(label="Input query SQL", key="user_input")

if query:
    result = ddb.sql(query).df()
    st.dataframe(result)

    try:
        result = result[solution_df.columns]
        st.dataframe(result.compare(solution_df))
    except KeyError as e:
        print("Some columns are missing")

    nb_lignes_difference = result.shape[0] - solution_df.shape[0]
    if nb_lignes_difference != 0:
        st.write(
            f"Result has a difference of {nb_lignes_difference} lignes compared to solution_df"
        )


tab1, tab2 = st.tabs(["Tables", "Solutions"])

with tab1:
    st.write("table: beverages")
    st.dataframe(beverages)
    st.write("table: food_items")
    st.dataframe(food_items)
    st.write("Expected Output")
    st.dataframe(solution_df)

with tab2:
    st.write(ANSWER_STR)
