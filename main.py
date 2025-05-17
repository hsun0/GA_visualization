import streamlit as st
import pandas as pd
from GA_TSP_page import GA_TSP_page
from crossover_page import crossover_page
from mutation_page import mutation_page
st.set_page_config(page_title="GA Solves TSP", layout="wide")  # ✅ 必須是第一個 Streamlit 指令

# 新增一個頁面選單
page = st.sidebar.selectbox("頁面", ["GA 主頁", "Crossover", "Mutation"])

if page == "Crossover":
    crossover_page()
if page == "GA 主頁":
    GA_TSP_page()
if page == "Mutation":
    mutation_page()