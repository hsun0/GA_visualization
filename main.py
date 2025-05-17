import streamlit as st
st.set_page_config(page_title="GA Solves TSP", layout="wide")  # ✅ 必須是第一個 Streamlit 指令

import numpy as np
import matplotlib.pyplot as plt
from GA import GA
from GA import Chromosome
import pandas as pd
import random as rd

# 新增一個頁面選單
page = st.sidebar.selectbox("頁面", ["GA 主頁", "Crossover 演算法介紹"])

if page == "Crossover 演算法介紹":
    st.title("Crossover (Order Crossover, OX) 演算法視覺化")
    st.markdown("""
    **Order Crossover (OX)** 是一種常用於旅行推銷員問題（TSP）的基因演算法交配方法。
    
    - 隨機選擇一段區間，將 Parent1 的該區間複製到子代對應位置。
    - 其餘位置依序填入 Parent2 中未出現過的基因，保持順序。
    
    下方互動式範例展示 OX 的過程：
    """)

    st.subheader("Order Crossover (OX) Demo")
    parent1 = st.text_input("Parent 1 基因 (用逗號分隔)", "1,2,3,4,5,6,7,8")
    parent2 = st.text_input("Parent 2 基因 (用逗號分隔)", "5,6,7,8,1,2,3,4")
    size = len(parent1.split(","))
    idx = st.slider("選擇交配區間 (start, end)", 0, size-1, (2,5))

    # ✅ 加入按鈕
    if st.button("執行 Crossover"):
        p1 = [int(x) for x in parent1.split(",")]
        p2 = [int(x) for x in parent2.split(",")]
        start, end = idx
        child = [-1]*size
        child[start:end+1] = p1[start:end+1]
        fill = [gene for gene in p2 if gene not in child[start:end+1]]
        ptr = 0
        for i in range(size):
            if child[i] == -1:
                child[i] = fill[ptr]
                ptr += 1

        st.write(f"Parent 1: {p1}")
        st.write(f"Parent 2: {p2}")
        st.write(f"交配區間: {start} ~ {end}")
        st.write(f"Child: {child}")

        fig, ax = plt.subplots(figsize=(8,1))
        ax.axis('off')
        for i, val in enumerate(child):
            color = '#FFD700' if start <= i <= end else '#87CEEB'
            ax.text(i, 0, str(val), fontsize=18, ha='center', va='center', bbox=dict(facecolor=color, edgecolor='k'))
        st.pyplot(fig)
        st.info("黃色區間來自 Parent 1，其餘來自 Parent 2（順序保留且不重複）")


if page == "GA 主頁":
    st.title("GA for TSP")
    # Sidebar controls
    with st.sidebar:
        st.header("⚙️ Parameters")
        city_source = st.radio("City Source", ["Random", "Default Graph", "Draw by Hand"])
        if city_source == "Random":
            num_cities = st.slider("Number of Cities", 5, 30, 15)
        elif city_source == "Default Graph":
            import os
            tsp_files = [f for f in os.listdir("problems") if f.endswith(".tsp")]
            tsp_file = st.selectbox("Select TSP File", tsp_files)
        elif city_source == "Draw by Hand":
            st.info("請在下方畫布上點擊新增城市座標。")
        popSize = st.slider("Population Size", 10, 300, 50)
        generations = st.slider("Number of Generations", 1, 1000, 100)
        crossoverRate = st.slider("Crossover Rate", 0.5, 1.0, 0.5)
        mutationRate = st.slider("Mutation Rate", 0.0, 0.3, 0.01)
        run = st.button("Run Simulation")

    # --- Main App ---
    if city_source == "Random":
        cities = np.random.rand(num_cities, 2) * 100
    elif city_source == "Default Graph":
        def load_tsp_file(filepath):
            coords = []
            with open(filepath, 'r') as f:
                for line in f:
                    line = line.strip()
                    if not line or line.startswith('//') or not any(c.isdigit() for c in line):
                        continue
                    parts = line.split()
                    if len(parts) >= 3:
                        try:
                            x = float(parts[1])
                            y = float(parts[2])
                            coords.append([x, y])
                        except ValueError:
                            continue
            return np.array(coords)
        cities = load_tsp_file(f"problems/{tsp_file}")
    elif city_source == "Draw by Hand":
        st.markdown(
            '''
            <style>
            .st-canvas-toolbar button {
                background-color: green !important;
                color: white !important;
                border: 1px solid #ccc !important;
            }
            </style>
            ''',
            unsafe_allow_html=True
        )
        st.subheader("🖊️ Draw Cities (Click to add points)")
        import streamlit_drawable_canvas as dc
        canvas_result = dc.st_canvas(
            fill_color="rgba(0, 0, 0, 1)",
            stroke_width=2,
            background_color="#fff",
            update_streamlit=True,
            height=400,
            width=400,
            drawing_mode="point",
            point_display_radius=5,
            key="canvas"
        )
        if canvas_result.json_data and "objects" in canvas_result.json_data:
            points = [[obj["left"], obj["top"]] for obj in canvas_result.json_data["objects"] if obj["type"] == "circle"]
            cities = np.array([[x, 400-y] for x, y in points])
        else:
            cities = np.empty((0, 2))
    else:
        cities = np.random.rand(10, 2) * 100  # fallback

    if run:
        progress_bar = st.progress(0, text="GA Running...")
        ga = GA(cities=cities, populationSize=popSize, generations=generations, crossoverRate=crossoverRate, mutation_rate=mutationRate)
        best_dists = []
        best_path = None
        route_chart = st.empty()

        ###### GA run loop ######
        ga.evaluation()
        best_dists.append(ga.chromosomes[0].fitness)
        for gen in range(generations):
            new_population = [Chromosome(ga.chromosomes[i].genes.copy()) for i in range(ga.elitismNum)]
            while len(new_population) < ga.populationSize:
                p1 = ga.select()
                p2 = ga.select()
                child = ga.crossover(p1, p2)
                ga.mutate(child)
                if rd.random() < 0.01:
                    ga.local_search_2opt(child)
                new_population.append(child) 
            ga.chromosomes = new_population
            ga.evaluation()
            best_dists.append(ga.chromosomes[0].fitness)
            best_path = ga.chromosomes[0].genes

            # 動態顯示路線
            fig, ax = plt.subplots()
            coords = cities[best_path + [best_path[0]]]
            ax.plot(coords[:, 0], coords[:, 1], '-o')
            ax.set_title(f"Generation {gen+1} | Best distance: {ga.chromosomes[0].fitness:.2f}")
            route_chart.pyplot(fig)
            progress_bar.progress((gen+1)/generations, text=f"Generation {gen+1}/{generations}")

        best_path = ga.chromosomes[0].genes
        ###### GA run loop end ######

        st.subheader("Best distances table")
        st.dataframe(pd.DataFrame({"Generation": list(range(1, len(best_dists)+1)), "Best Distance": best_dists}))

        st.subheader("📈 Distance Over Generations")
        fig2, ax2 = plt.subplots()
        ax2.plot(best_dists)
        ax2.set_xlabel("Generation")
        ax2.set_ylabel("Distance")
        st.pyplot(fig2)
    else:
        st.info("請從左側選擇參數後按下 [Run Simulation] 開始。")
