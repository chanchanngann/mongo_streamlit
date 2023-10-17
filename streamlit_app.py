import streamlit as st
import pymongo
import os


# Initialize connection.
# only runs when the query changes or after 10 minutes
@st.cache_resource
def init_connection():
    return pymongo.MongoClient(**st.secrets["mongo"])

client = init_connection()
mydb = client["HealthDB"]
mycollection = mydb["HeartAttack"]

# Pull data from the collection.
# Uses st.cache_data to only rerun when the query changes or after 10 min.
@st.cache_data(ttl=600)
def get_data():
    items = mycollection.find()
    items = list(items)  # make hashable for st.cache_data
    return items

items = get_data()[0]

# Print results.
for item in items:
    st.write(item)