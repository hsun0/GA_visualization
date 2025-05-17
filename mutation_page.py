import streamlit as st
import pandas as pd
import random
import matplotlib.pyplot as plt
def mutation_page():
    # st.set_page_config(page_title="Mutation", layout="wide")
    st.title("Mutation (Swap & Inversion) 演算法視覺化")

    st.markdown("""
    **Mutation** 是基因演算法中用來增加多樣性的操作，常見於 TSP 的 mutation 包括：
    - **Swap Mutation**：隨機選兩個位置交換。
    - **Inversion Mutation**：隨機選一段區間反轉。

    下方互動式範例展示 mutation 的過程：
    """)

    st.subheader("Mutation Demo")

    # 產生隨機 permutation
    size = st.slider("基因長度", 5, 20, 8)
    if 'mutation_perm' not in st.session_state:
        st.session_state['mutation_perm'] = list(range(1, size+1))

    if st.button("產生隨機 Parent permutation"):
        perm = list(range(1, size+1))
        random.shuffle(perm)
        st.session_state['mutation_perm'] = perm

    parent = st.session_state['mutation_perm']
    df = pd.DataFrame({'Parent': parent})
    st.dataframe(df, use_container_width=True)

    mutation_type = st.radio("選擇 Mutation 類型", ["Swap", "Inversion"])

    if mutation_type == "Swap":
        idx = st.slider("選擇交換的兩個位置", 0, size-1, (1, 5))
        if st.button("執行 Swap Mutation"):
            child = parent.copy()
            i, j = idx
            child[i], child[j] = child[j], child[i]
            df_mut = pd.DataFrame({'Parent': parent, 'Child': child})
            def highlight_swap(val, col):
                if col == 'Child':
                    if val == child[i] or val == child[j]:
                        return 'background-color: #FFFF00'  # 黃色
                return ''
            def style_swap(s):
                return [highlight_swap(v, s.name) for v in s]
            st.dataframe(df_mut.style.apply(style_swap, axis=0))
            st.info("黃色為交換的兩個位置")

    elif mutation_type == "Inversion":
        idx = st.slider("選擇反轉區間 (start, end)", 0, size-1, (2, 5))
        if st.button("執行 Inversion Mutation"):
            child = parent.copy()
            start, end = idx
            child[start:end+1] = list(reversed(child[start:end+1]))
            df_mut = pd.DataFrame({'Parent': parent, 'Child': child})
            def highlight_inv(val, col):
                if col == 'Child':
                    for k, v in enumerate(child):
                        if v == val and start <= k <= end:
                            return 'background-color: #FFD700'  # 黃色
                return ''
            def style_inv(s):
                return [highlight_inv(v, s.name) for v in s]
            st.dataframe(df_mut.style.apply(style_inv, axis=0))
            fig, ax = plt.subplots(figsize=(8,1))
            ax.axis('off')
            for k, val in enumerate(child):
                color = '#FFD700' if start <= k <= end else '#87CEEB'
                ax.text(k, 0, str(val), fontsize=18, ha='center', va='center', bbox=dict(facecolor=color, edgecolor='k'))
            st.pyplot(fig)
            st.info("黃色為反轉區間")
