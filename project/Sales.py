import streamlit as st 
import pandas as pd 
import joblib 
from streamlit_folium import st_folium 
import folium 
 
model = joblib.load('my_model.pkl') 
 
st.title("Predict Sales Based on Location and Features") 
 
st.write("Select Location on Map:") 
m = folium.Map(location=[26, 35], zoom_start=5) 
marker = folium.Marker(location=[26, 35], draggable=True) 
marker.add_to(m) 
output = st_folium(m, width=700, height=500) 
 
LAT, LONG = 26, 35 
if output and output.get("last_clicked"): 
    LAT = output["last_clicked"]["lat"] 
    LONG = output["last_clicked"]["lng"] 
elif output and output.get("last_object_clicked"): 
    LAT = output["last_object_clicked"]["lat"] 
    LONG = output["last_object_clicked"]["lng"] 
 
st.write(f"Latitude: {LAT:.4f}, Longitude: {LONG:.4f}") 
 
discount = st.number_input("Discount", min_value=0.0, max_value=1.0, value=0.0) 
profit = st.number_input("Profit", value=0.0) 
price = st.number_input("Price", value=0.0) 
returned = st.selectbox("Returned_Binary", [0, 1]) 
 
categories = [ 
    'Office Supplies', 'Technology', 'Appliances', 'Art', 'Binders', 'Bookcases', 'Chairs', 'Copiers', 
    'Envelopes', 'Fasteners', 'Furnishings', 'Labels', 'Machines', 'Paper', 'Phones', 'Storage', 
    'Supplies', 'Tables' 
] 
selected_category = st.selectbox("Category", categories) 
segments = ['Corporate', 'Home Office'] 
selected_segment = st.selectbox("Segment", segments) 
year = st.number_input("Year", min_value=2000, max_value=2100, value=2024) 
month = st.number_input("Month", min_value=1, max_value=12, value=1) 
day = st.number_input("Day", min_value=1, max_value=31, value=1) 
 
input_dict = { 
    'Discount': discount, 
    'Profit': profit, 
    'LAT': LAT, 
    'LONG': LONG, 
    'Price': price, 
    'Returned_Binary': returned, 
} 
 
for cat in categories: 
    input_dict[cat] = 1 if cat == selected_category else 0 
for seg in segments: 
    input_dict[seg] = 1 if seg == selected_segment else 0 
 
input_dict['Year'] = year 
input_dict['Month'] = month 
input_dict['Day'] = day 
 
X = pd.DataFrame([input_dict]) 
 
if st.button("Predict Profit"): 
    prediction = model.predict(X)[0] 
    st.success(f"Predicted Sales: {prediction:.2f}")
