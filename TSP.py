import streamlit as st

def TSP_page(): 
    st.title("Traveling Salesman Problem (TSP)")

    st.markdown("""
    Do you know the fastest way to travel around Taiwan in a complete loop?
    """)

    st.image("TAIWAN.jpg", caption="Taiwan", width=300)

    st.markdown("""
    The Traveling Salesman Problem (TSP) is a classic optimization problem that asks for the shortest possible route that visits each city exactly once and returns to the origin city.
    """)

    st.image("tsp.jpg", width=600)