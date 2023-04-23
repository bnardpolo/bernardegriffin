import pandas as pd
import streamlit as st
import plotly.express as px
import plotly.figure_factory as ff
import matplotlib.pyplot as plt
import altair as alt

st.set_page_config(page_title = "Dashboard", layout="wide")

df = pd.read_csv("veh.csv")
# print(df)
st.sidebar.header("Please check the box")
agree = st.sidebar.checkbox('Show sales summary')


    

st.sidebar.header("Please filter here")
type = st.sidebar.multiselect(
    "Select the type of vehicle",
    options=df['type'].unique(),
    default=df['type'].unique()
)

st.sidebar.header("Please filter here")
transmission = st.sidebar.multiselect(
    "Select the transmission type",
    options=df['transmission'].unique(),
    default=df['transmission'].unique()
)

df_selection = df.query(
    "type == @type & transmission == @transmission" 
)

    
    
st.title("Dashboard")
st.markdown("---")

Total_number_of_vehicles = int(df_selection['model'].count())
total_price = int(df_selection['price'].sum())
average_price = round(df_selection['price'].mean(), 1)


left_column, middle_column, right_column = st.columns(3)
with left_column:
    st.subheader("Total Number of vehicles")
    st.subheader(f"{Total_number_of_vehicles}")
with middle_column:
    st.subheader("Total price of vehicles:")
    st.subheader(f"US $ {total_price}")
with right_column:
    st.subheader("Average price of vehicles:")
    st.subheader(f"US $ {average_price}")
    

st.markdown("---")

sales_by_model = (
    df_selection.groupby(by="model").sum('Total')[['price']]
)

fig1 = px.bar(
    sales_by_model,
    x = "price",
    y = sales_by_model.index,
    orientation="h",
    title="<b>Sales by Model</b>",
    template="plotly_white",
)

fig1.update_layout(
    plot_bgcolor = "rgba(0,0,0,0)",
    xaxis = (dict(showgrid=False))
)



sales_by_condition =(
    df_selection.groupby("condition")["price"].sum().sort_values()
)
fig2 = px.bar(
    sales_by_condition,
    title="<b>Sales by Condition</b>",
    template="plotly_white",
)
fig2.update_layout(
    plot_bgcolor = "rgba(0,0,0,0)",
    xaxis = (dict(showgrid=False))
)

# left_column, right_column = st.columns(2)

if agree:
    st.plotly_chart(fig1, use_container_width=True)
    st.plotly_chart(fig2, use_container_width=True)
else:
    st.write("Sales Summary")

car_per_type = (
    df_selection.type.value_counts()
)
fig3 = px.bar(
    car_per_type,
    title="<b>Number of cars per type</b>",
    template="plotly_white",
)
fig3.update_layout(
    plot_bgcolor = "rgba(0,0,0,0)",
    xaxis = (dict(showgrid=False))
)
st.plotly_chart(fig3)



fig4 = px.scatter(
    df_selection,
    x='price',
    y="model",
    title="<b>Price distribution of the model</b>",    
)
st.plotly_chart(fig4, use_container_width=True)

st.dataframe(df_selection)






