import streamlit as st
import pandas as pd
from PIL import Image
import datetime
import plotly.express as px
import plotly.graph_objects as go
import os
import warnings

warnings.filterwarnings('ignore')

st.set_page_config(
    page_title="Sales Forecasting and Optimization Dashboard",
    layout="wide",
    page_icon="📊"
)
st.markdown('<style>div.block-container{padding-top:1rem;}</style>', unsafe_allow_html=True)

# Load Image with error handling
image_path = "Forecasting.jpg"
if os.path.exists(image_path):
    image = Image.open(image_path)
else:
    image = None
    st.warning(f"Image file '{image_path}' not found.")

@st.cache_data  # Cache data for better performance
def load_data():
    data_path = ("Retail.xlsx")
    if os.path.exists(data_path):
        df = pd.read_excel(data_path)
        return df
    else:
        st.error(f"Data file '{data_path}' not found in the current directory.")
        return pd.DataFrame()  # Return empty DataFrame if file not found

df = load_data()
if df.empty:
    st.stop()

# Load Image
col1, col2 = st.columns([0.2, 0.9])
with col1:
    if image:
        st.image(image, width=200, output_format="auto")

html_title = """
     <style>
     .title-test {
     font-weight:bold;
     padding:5px;
     border-radius:6p
     }
     </style>
     <center><h1 class = "title-test" >Sales Forecasting and Optimization Dashboard</h1></center>"""
with col2:
    st.markdown(html_title, unsafe_allow_html=True)

col3, col4, col5 = st.columns([0.2, 0.45, 0.45])

with col3:
    box_date = str(datetime.datetime.now().strftime("%d %B %Y"))
    st.write(f"Last updated by : \n {box_date}")

with col4:
    fig = px.bar(df, x='Category', y='Sales', labels={'Sales': 'Sales {$}'},
                 title="Total sales by Category", hover_data=['Sales'],
                 template='gridon', height=500)
    st.plotly_chart(fig, use_container_width=True)

_, view1, dwn1, view2, dwn2 = st.columns([0.15, 0.20, 0.20, 0.20, 0.20])
with view1:
    expander = st.expander("Category sales")
    data = df[['Category', 'Sales']].groupby(by='Category')['Sales'].sum()
    expander.write(data)

with dwn1:
    st.download_button("Get Table Data", data=data.to_csv().encode('utf-8'),
                       file_name="Total sales by Category.csv", mime='text/csv')

df['Price'] = df['Sales'] / df['Quantity']
df["Month_Year"] = pd.to_datetime(df["Order Date"]).dt.strftime("%b %y")
result = df.groupby(by=df["Month_Year"])["Sales"].sum().reset_index()

with col5:
    fig1 = px.line(result, x='Month_Year', y='Sales', title='Total Sales Over Time',
                   template='gridon')
    st.plotly_chart(fig1, use_container_width=True)

with view2:
    expander = st.expander("Monthly Sales Over Years")
    data = result
    expander.write(data)

with dwn2:
    st.download_button("Get Table Data", data=result.to_csv().encode('utf-8'),
                       file_name="Total Sales Over Time.csv", mime='text/csv')

st.divider()

result1 = df.groupby(['Category', 'Sub-Category'])['Sales'].sum().reset_index()
fig3 = px.bar(
    result1,
    x='Sub-Category',
    y='Sales',
    color='Category',
    orientation='v',
    color_discrete_map={
        'Furniture': '#636EFA',
        'Office Supplies': '#EF553B',
        'Technology': '#00CC96'
    },
    title='Sales by Sub-Category'
)
fig3.update_layout(
    xaxis={'categoryorder': 'total descending'},
    yaxis_title='Total Sales ($)',
    xaxis_title='Sub-Category',
    plot_bgcolor='rgba(0,0,0,0)',
    height=600,
    hovermode='x unified'
)

_, col6 = st.columns([0.1, 1])
with col6:
    st.plotly_chart(fig3, use_container_width=True)
_, view3, dwn3 = st.columns([0.5, 0.45, 0.45])

with view3:
    expander = st.expander("Sales by Sub-Category")
    data = result1
    expander.write(data)

with dwn3:
    st.download_button("Get Table Data", data=result1.to_csv().encode('utf-8'),
                       file_name="Sales by Sub-Category.csv", mime='text/csv')

st.divider()

# Calculate average price per category
avg_prices = df.groupby('Category')['Price'].mean().reset_index()

# Create pie chart
fig4 = px.pie(
    avg_prices,
    names='Category',
    values='Price',
    title='Proportion of Average Price by Category',
    hole=0.3,
    color_discrete_sequence=px.colors.qualitative.Pastel
)

fig4.update_traces(
    textposition='inside',
    textinfo='percent+label',
    pull=[0.02] * len(avg_prices)
)

_, col7, col8 = st.columns([0.2, 0.45, 0.45])
with col7:
    st.plotly_chart(fig4, use_container_width=True)
_, view4, dwn4, view5, dwn5 = st.columns([0.15, 0.20, 0.20, 0.20, 0.20])
with view4:
    expander = st.expander("Average Price by Category")
    expander.write(avg_prices)

with dwn4:
    st.download_button("Get Table Data", data=avg_prices.to_csv().encode('utf-8'),
                       file_name="Average Price by Category.csv", mime='text/csv')

result2 = df.groupby(['Category', 'Sub-Category'])['Quantity'].sum().reset_index()
fig5 = px.bar(
    result2,
    x='Sub-Category',
    y='Quantity',
    color='Category',
    orientation='v',
    color_discrete_map={
        'Furniture': '#636EFA',
        'Office Supplies': '#EF553B',
        'Technology': '#00CC96'
    },
    title='Quantity by Sub-Category'
)
fig5.update_layout(
    yaxis_title='Total Quantity',
    xaxis_title='Sub-Category',
    plot_bgcolor='rgba(0,0,0,0)',
    height=600,
    hovermode='x unified'
)
with col8:
    st.plotly_chart(fig5, use_container_width=True)

with view5:
    expander = st.expander("Quantity by Sub-Category")
    expander.write(result2)

with dwn5:
    st.download_button("Get Table Data", data=result2.to_csv().encode('utf-8'),
                       file_name="Quantity by Sub-Category.csv", mime='text/csv')
st.divider()

_, col9, col10 = st.columns([0.2, 0.45, 0.45])
_, view6, dwn6, view7, dwn7 = st.columns([0.15, 0.20, 0.20, 0.20, 0.20])

# Group by discount and calculate mean profit
agg_df = df.groupby("Discount")["Profit"].mean().reset_index()

fig6 = px.bar(
    agg_df,
    x="Discount",
    y="Profit",
    title="Average Profit at Different Discount Levels"
)

fig6.update_layout(
    xaxis_title="Discount (%)",
    yaxis_title="Average Profit ($)",
    xaxis={"type": "category"}
)
with col9:
    st.plotly_chart(fig6, use_container_width=True)

with view6:
    expander = st.expander("Average Profit at Different Discount Levels")
    expander.write(agg_df)

with dwn6:
    st.download_button("Get Table Data", data=agg_df.to_csv().encode('utf-8'),
                       file_name="Average Profit at Different Discount Levels.csv", mime='text/csv')

avg_discount = df.groupby('Category')['Discount'].mean().reset_index()

fig8 = px.pie(
    avg_discount,
    names='Category',
    values='Discount',
    title='Average Discount by Category',
    hole=0.3,
    color_discrete_sequence=px.colors.qualitative.Pastel
)

fig8.update_traces(
    textposition='inside',
    textinfo='percent+label',
    pull=[0.02] * len(avg_discount),
    marker=dict(line=dict(color='#000000', width=1))
)

fig8.update_layout(
    uniformtext_minsize=12,
    uniformtext_mode='hide',
    legend=dict(orientation="h", yanchor="bottom", y=-0.2)
)

with col10:
    st.plotly_chart(fig8, use_container_width=True)

with view7:
    expander = st.expander("Average Discount by Category")
    expander.write(avg_discount)

with dwn7:
    st.download_button("Get Table Data", data=avg_discount.to_csv().encode('utf-8'),
                       file_name="Average Discount by Category.csv", mime='text/csv')

# 1. Aggregate product performance
product_stats = df.groupby('Product Name').agg({
    'Profit': 'sum',
    'Sales': 'sum',
    'Quantity': 'sum',
    'Discount': 'mean'
}).reset_index()

# 2. Get top 10 best products
top_products = product_stats.nlargest(10, 'Profit').round(2)

# 3. Create the visualization
fig7 = px.bar(
    top_products,
    x='Profit',
    y='Product Name',
    orientation='h',
    title='Top 10 Best-Selling Products by Profit',
    color='Profit',
    color_continuous_scale=['lightgreen', 'darkgreen'],
    hover_data={
        'Sales': ':.2f',
        'Quantity': True,
        'Discount': ':.1%',
        'Product Name': True
    },
    labels={'Profit': 'Total Profit ($)'}
)

fig7.update_layout(
    xaxis_title="Total Profit ($)",
    yaxis={'categoryorder': 'total ascending'},
    hoverlabel=dict(bgcolor="white", font_size=12),
    plot_bgcolor='rgba(0,0,0,0)'
)

fig7.update_traces(
    texttemplate='$%{x:,.2f}',
    textposition='outside',
    marker_line_color='darkgreen',
    marker_line_width=1
)

_, col11 = st.columns([0.1, 1])
with col11:
    st.plotly_chart(fig7, use_container_width=True)
_, view8, dwn8 = st.columns([0.5, 0.45, 0.45])

with view8:
    expander = st.expander("Top 10 Best-Selling Products by Profit")
    data = top_products
    expander.write(data)

with dwn8:
    st.download_button("Get Table Data", data=top_products.to_csv().encode('utf-8'),
                       file_name="Top 10 Best-Selling Products by Profit.csv", mime='text/csv')