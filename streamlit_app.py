import streamlit as st
import pymongo
import os
import pandas as pd
import plotly.express as px


################### Initialize connection ##############
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

# load data into dataframe
data = get_data()
df = pd.json_normalize(data)

################### Plots ##############
st.title("Heart Attack Risk Dataset")

#plot
st.header("Dataset preview")
st.write(df.head().set_index("Patient ID"))

#plot
st.header("Dataset profile")
st.write(df.describe())

#plot
df1 = df.drop(['Patient ID','Sex','Blood Pressure','Diet','Country','Continent','Hemisphere'],axis=1).corr()
st.header("Correlations between attributes")
st.write(df1)

#plots
st.header("Distribution")
col1, col2, col3 = st.columns(3)
with col1:
    df2 = df.Sex.value_counts().reset_index()
    df2.columns=["Sex","Count"]
    st.subheader("Sex")
    st.bar_chart(df2,x='Sex',y='Count')
with col2:
    df3 = df.Age.value_counts().reset_index()
    df3.columns=["Age","Count"]
    st.subheader("Age")
    st.bar_chart(df3,x='Age',y='Count')
with col3:
    df4 = df.Smoking.value_counts().reset_index()
    df4.columns=["Smoking","Count"]
    st.subheader("Smoking")
    st.bar_chart(df4,x='Smoking',y='Count')

col1, col2, col3 = st.columns(3)
with col1:
    df5 = df.Diet.value_counts().reset_index()
    df5.columns=["Diet","Count"]
    st.subheader("Diet")
    st.bar_chart(df5,x='Diet',y='Count')
with col2:
    df6 = df["Stress Level"].value_counts().reset_index()
    df6.columns=["Stress Level","Count"]
    st.subheader("Stress Level")
    st.bar_chart(df6,x='Stress Level',y='Count')
with col3:
    df7 = df["Alcohol Consumption"].value_counts().reset_index()
    df7.columns=["Alcohol Consumption","Count"]
    st.subheader("Alcohol Consumption")
    st.bar_chart(df7,x='Alcohol Consumption',y='Count')

col1, col2, col3 = st.columns(3)
with col1:
    df8 = df.Obesity.value_counts().reset_index()
    df8.columns=["Obesity","Count"]
    st.subheader("Obesity")
    st.bar_chart(df8,x='Obesity',y='Count')
with col2:
    df9 = df["Diabetes"].value_counts().reset_index()
    df9.columns=["Diabetes","Count"]
    st.subheader("Diabetes")
    st.bar_chart(df9,x='Diabetes',y='Count')
with col3:
    df10 = df["Heart Attack Risk"].value_counts().reset_index()
    df10.columns=["Heart Attack Risk","Count"]
    st.subheader("Heart Attack Risk")
    st.bar_chart(df10,x='Heart Attack Risk',y='Count')


st.caption("data source: https://www.kaggle.com/datasets/iamsouravbanerjee/heart-attack-prediction-dataset/data")
st.caption("dashboard prepared on 2023-10-19")