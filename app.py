# pylint: disable=missing-module-docstring

import duckdb
import streamlit as st

con = duckdb.connect(database="data/exercices_sql_tables.duckdb", read_only=False)

with st.sidebar:
    theme = st.selectbox(
        "What would you like to review",
        ["cross_joins", "GroupBy", "Window Functions"],
        index=None,
        placeholder="Select a theme",
    )

    st.write(theme)

    exercise = (
        con.execute(f"SELECT * FROM memory_state WHERE theme = '{theme}'")
        .df()
        .sort_values("last_reviewed")
        .reset_index()
    )
    st.write(exercise)

    exercise_name = exercise.loc[0, "exercise_name"]

    with open(file=f"answers/{exercise_name}.sql", mode="r") as f:
        answer = f.read()

    solution_df = con.execute(answer).df()

st.header("Enter your code")
query = st.text_area(label="Input query SQL", key="user_input")

if query:
    result = con.execute(query).df()
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


tab1, tab2 = st.tabs(["Tables", "Solutions"])

with tab1:
    exercises_tables = exercise.loc[0, "tables"]
    for table in exercises_tables:
        st.write(f"table: {table}")
        df_table = con.execute(f"SELECT * FROM {table}").df()
        st.write(df_table)

with tab2:
    st.write(answer)
