import streamlit as st

def crossover_page():
    st.title("Order Crossover (OX)")
    st.markdown("""
    - 隨機選擇一段區間，將 Parent1 的該區間複製到子代對應位置。
    - 其餘位置依序填入 Parent2 中未出現過的基因，保持順序。
    """)

    st.subheader("Order Crossover (OX) Demo")
    st.write("請直接在下方表格修改 Parent 1 與 Parent 2 的基因序列，然後按下按鈕產生 Child。")
    import pandas as pd
    import random
    default_p1 = [1,2,3,4,5,6,7,8]
    default_p2 = [5,6,7,8,1,2,3,4]
    if 'parent_df' not in st.session_state:
        st.session_state['parent_df'] = pd.DataFrame({'Parent 1': default_p1, 'Parent 2': default_p2})
    size = len(st.session_state['parent_df'])

    if st.button("產生隨機 Parent permutation"):
        perm = list(range(1, size+1))
        random.shuffle(perm)
        perm2 = perm.copy()
        while True:
            random.shuffle(perm2)
            if perm2 != perm:
                break
        st.session_state['parent_df'] = pd.DataFrame({'Parent 1': perm, 'Parent 2': perm2})

    edited_df = st.data_editor(st.session_state['parent_df'], num_rows="fixed", use_container_width=True, key="parent_editor")
    size = len(edited_df)
    idx = st.slider("選擇交配區間 (start, end)", 0, size-1, (2,5))

    if st.button("執行 Crossover"):
        p1 = list(edited_df['Parent 1'])
        p2 = list(edited_df['Parent 2'])
        start, end = idx
        child = [-1]*size
        child[start:end+1] = p1[start:end+1]
        fill = [gene for gene in p2 if gene not in child[start:end+1]]
        ptr = 0
        for i in range(size):
            if child[i] == -1:
                child[i] = fill[ptr]
                ptr += 1
        # 標記每個 child 基因來源
        child_source = []
        for i in range(size):
            if start <= i <= end:
                child_source.append('p1')
            else:
                child_source.append('p2')
        df_child = pd.DataFrame({
            'Parent 1': p1,
            'Parent 2': p2,
            'Child': child
        })
        def highlight_child(val, col):
            if col == 'Child':
                for i, v in enumerate(child):
                    if v == val:
                        source = child_source[i]
                        if source == 'p1':
                            return 'background-color: #ffa500'
                        elif source == 'p2':
                            return 'background-color: #0000cd'
            return ''
        def style_child(s):
            return [highlight_child(v, s.name) for v in s]
        st.dataframe(df_child.style.apply(style_child, axis=0))
        st.info("表格顯示每個位置的基因來源，黃色來自 Parent 1，藍色來自 Parent 2（順序保留且不重複）")