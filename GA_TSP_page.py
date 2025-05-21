import random as rd
import numpy as np
import pandas as pd
import streamlit as st
from GA import GA
from GA import Chromosome
import matplotlib.pyplot as plt

def GA_TSP_page():
    st.title("GA for TSP")
    # Sidebar controls
    with st.sidebar:
        st.header("🔡 Methods")
        st.info("Crossover: Order Crossover (OX)\nMutation: Inversion")
        st.header("⚙️ Parameters")
        city_source = st.radio("City Source", ["Random", "Default Graph", "Draw by Hand"])
        if city_source == "Random":
            num_cities = st.slider("Number of Cities", 5, 30, 15)
        elif city_source == "Default Graph":
            import os
            tsp_files = [f for f in os.listdir("problems") if f.endswith(".tsp")]
            tsp_file = st.selectbox("Select TSP File", tsp_files)
        elif city_source == "Draw by Hand":
            st.info("Please click to add points on the canvas.")
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
            # 若是 tw*.tsp，x/y 軸比例設為一樣
            if city_source == "Default Graph" and tsp_file.startswith("tw"):
                ax.set_aspect('equal', adjustable='datalim')
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
        st.info("Please select parameters from the sidebar and click [Run Simulation] to start.")