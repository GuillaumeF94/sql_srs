# pylint: disable=missing-module-docstring

import os
import logging
import duckdb
import streamlit as st
from datetime import timedelta


def check_users_solution(user_query: str):
    """
    Checks the user solution by comparing :
    1: the columns
    2: the values
    :param user_query:
    :return:
    """
    result = con.execute(user_query).df()
    st.dataframe(result)

    try:
        result = result[solution_df.columns]
        st.dataframe(result.compare(solution_df))
    except KeyError as e:
        st.write("Some columns are missing")

    nb_lignes_difference = result.shape[0] - solution_df.shape[0]
    if nb_lignes_difference != 0:
        st.write(
            f"Result has a difference of {nb_lignes_difference} lignes compared to solution_df"
        )

if "data" not in os.listdir():
    logging.error(os.listdir())
    logging.error("Creating folder data")
    os.mkdir("data")

if "exercices_sql_tables.duckdb" not in os.listdir("data"):
    exec(open("init_db.py").read())

con = duckdb.connect(database="data/exercices_sql_tables.duckdb", read_only=False)

with st.sidebar:
    memory_state = con.execute("SELECT * FROM memory_state").df()
    available_theme = memory_state["theme"].unique()

    theme = st.selectbox(
        "What would you like to review",
        options=available_theme,
        index=None,
        placeholder="Select a theme",
    )

    if theme:
        st.write(theme)
        query = f"SELECT * FROM memory_state WHERE theme = '{theme}'"
    else:
        query = "SELECT * FROM memory_state"

    exercise = (
        con.execute(query).df().sort_values("last_reviewed").reset_index(drop=True)
    )

    st.write(exercise)
    exercise_name = exercise.loc[0, "exercise_name"]

    with open(file=f"answers/{exercise_name}.sql", mode="r") as f:
        answer = f.read()

    solution_df = con.execute(answer).df()

st.header("Enter your code")
query = st.text_area(label="Input query SQL", key="user_input")

if query:
    check_users_solution(query)

for n_days in [2, 7, 21]:
    if st.button(f"Revoir dans {n_days} jours"):
        new_date = datetoday() + timedelta(days=n_days)
        con.execute(f"UPDATE memory_state SET last_reviewed = '{new_date}' WHERE exercise_name = '{exercise_name}'")
        st.rerun()
if st.button('Reset'):
    con.execute("UPDATE memory_state SET last_reviewed = '1970-01-01'")
    st.rerun()

tab1, tab2 = st.tabs(["Tables", "Solutions"])

with tab1:
    exercises_tables = exercise.loc[0, "tables"]
    for table in exercises_tables:
        st.write(f"table: {table}")
        df_table = con.execute(f"SELECT * FROM {table}").df()
        st.write(df_table)

with tab2:
    st.write(answer)
