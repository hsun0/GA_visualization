import streamlit as st

def crossover_page():
    st.title("Order Crossover (OX)")
    st.markdown("""
    - Randomly select a segment and copy that segment from Parent 1 to the corresponding positions in the child.
    - Fill the remaining positions with genes from Parent 2, in order, skipping any genes already present in the child.
    """)

    st.subheader("Order Crossover (OX) Demo")
    st.write("Please edit the gene sequences of Parent 1 and Parent 2 in the table below, then press the button to generate the Child.")
    import pandas as pd
    import random
    default_p1 = [1,2,3,4,5,6,7,8]
    default_p2 = [5,6,7,8,1,2,3,4]
    if 'parent_df' not in st.session_state:
        st.session_state['parent_df'] = pd.DataFrame({'Parent 1': default_p1, 'Parent 2': default_p2})
    size = len(st.session_state['parent_df'])

    if st.button("Generate random Parent permutation"):
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
    idx = st.slider("Select crossover segment (start, end)", 0, size-1, (2,5))

    if st.button("Execute crossover"):
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
                            return 'background-color: #808080'
                        elif source == 'p2':
                            return 'background-color: #000000'
            return ''
        def style_child(s):
            return [highlight_child(v, s.name) for v in s]
        st.dataframe(df_child.style.apply(style_child, axis=0))
        st.info("Gray indicates genes from Parent 1, black indicates genes from Parent 2.")