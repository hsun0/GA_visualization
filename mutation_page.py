import streamlit as st
import pandas as pd
import random
import matplotlib.pyplot as plt
def mutation_page():
    # st.set_page_config(page_title="Mutation", layout="wide")
    st.title("Mutation (Swap & Inversion)")

    st.markdown("""
    **Mutation** is an operation in genetic algorithms used to increase diversity. Common mutations for TSP include:
    - **Swap Mutation**: Randomly select and swap two positions.
    - **Inversion Mutation**: Randomly select a segment and reverse it.
    """)

    st.subheader("Mutation Demo")

    # 產生隨機 permutation
    size = st.slider("Gene length", 5, 20, 8)
    if 'mutation_perm' not in st.session_state:
        st.session_state['mutation_perm'] = list(range(1, size+1))

    if st.button("Generate random permutation"):
        perm = list(range(1, size+1))
        random.shuffle(perm)
        st.session_state['mutation_perm'] = perm

    parent = st.session_state['mutation_perm']
    df = pd.DataFrame({'Before': parent})
    st.dataframe(df, use_container_width=True)

    mutation_type = st.radio("Choose Mutation Type", ["Swap", "Inversion"])

    if mutation_type == "Swap":
        idx = st.slider("Select two positions to swap", 0, size-1, (1, 5))
        if st.button("Excute Swap Mutation"):
            child = parent.copy()
            i, j = idx
            child[i], child[j] = child[j], child[i]
            df_mut = pd.DataFrame({'Before': parent, 'After': child})
            def highlight_swap(val, col):
                if col == 'After':
                    if val == child[i] or val == child[j]:
                        return 'background-color: #808080'  # 灰色
                return ''
            def style_swap(s):
                return [highlight_swap(v, s.name) for v in s]
            st.dataframe(df_mut.style.apply(style_swap, axis=0))
            st.info("Gray indicates the two swapped positions")

    elif mutation_type == "Inversion":
        idx = st.slider("Select inversion segment (start, end)", 0, size-1, (2, 5))
        if st.button("Excute Inversion Mutation"):
            child = parent.copy()
            start, end = idx
            child[start:end+1] = list(reversed(child[start:end+1]))
            df_mut = pd.DataFrame({'Before': parent, 'After': child})
            def highlight_inv(val, col):
                if col == 'Child':
                    for k, v in enumerate(child):
                        if v == val and start <= k <= end:
                            return 'background-color: #808080'  # 黃色
                return ''
            def style_inv(s):
                return [highlight_inv(v, s.name) for v in s]
            st.dataframe(df_mut.style.apply(style_inv, axis=0))
            st.info("Gray indicates the inverted segment")
