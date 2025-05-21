import streamlit as st
import pandas as pd
from GA_TSP_page import GA_TSP_page
from crossover_page import crossover_page
from mutation_page import mutation_page
st.set_page_config(page_title="GA Solves TSP", layout="wide")

# 新增一個頁面選單
page = st.sidebar.selectbox("Page", ["GA for TSP", "Crossover", "Mutation"])

if page == "Crossover":
    crossover_page()
if page == "GA for TSP":
    GA_TSP_page()
if page == "Mutation":
    mutation_page()