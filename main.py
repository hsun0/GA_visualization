import streamlit as st
import pandas as pd
from GA_TSP_page import GA_TSP_page
from home import home_page
from crossover_page import crossover_page
from mutation_page import mutation_page
from TSP import TSP_page
st.set_page_config(page_title="GA Solves TSP", layout="wide")

# 設定深色模式 CSS
st.markdown("""
<style>
.stApp {
    background-color: #0E1117;
    color: #FAFAFA;
}
.stSidebar {
    background-color: #262730;
}
.stSelectbox > div > div {
    background-color: #262730;
    color: #FAFAFA;
}
</style>
""", unsafe_allow_html=True)

# 新增一個頁面選單
page = st.sidebar.selectbox("Page", ["Home", "TSP", "Crossover", "Mutation", "GA for TSP"])

if page == "Home":
    home_page()
if page == "TSP":
    TSP_page()
if page == "Crossover":
    crossover_page()
if page == "GA for TSP":
    GA_TSP_page()
if page == "Mutation":
    mutation_page()