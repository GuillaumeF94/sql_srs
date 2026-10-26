import io
import streamlit as st
import pandas as pd
import duckdb as ddb


csv = '''
beverage,price
orange_juice,2.5
Espresso,2
Tea,3
'''

csv2 = '''
food_item,food_price
cookie,2.5
chocolatine,2
muffin,3
'''

beverages = pd.read_csv(io.StringIO(csv))
food_items = pd.read_csv(io.StringIO(csv2))

answer = """
SELECT * FROM beverages
CROSS JOIN food_items
"""

solution = ddb.sql(answer).df()

st.header("Enter your code")
query = st.text_area(label="Input query SQL", key="user_input")

if query:
    result = ddb.sql(query).df()
    st.dataframe(result)

tab1, tab2 = st.tabs(["Tables", "Solutions"])

with tab1:
    st.write("table: beverages")
    st.dataframe(beverages)
    st.write("table: food_items")
    st.dataframe(food_items)
    st.write("Expected Output")
    st.dataframe(solution)

with tab2:
    st.write(answer)









