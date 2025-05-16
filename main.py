# ga_tsp_visualizer.py
import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from GA import GA
from GA import Chromosome
import pandas as pd

# --- Streamlit UI ---
st.set_page_config(page_title="GA Solves TSP", layout="wide")
st.title("🚀 Genetic Algorithm for Traveling Salesman Problem")

# Sidebar controls
with st.sidebar:
    st.header("⚙️ Parameters")
    city_source = st.radio("City Source", ["Random", "From File"])
    if city_source == "Random":
        num_cities = st.slider("Number of Cities", 5, 30, 15)
    else:
        import os
        tsp_files = [f for f in os.listdir("problems") if f.endswith(".tsp")]
        tsp_file = st.selectbox("Select TSP File", tsp_files)
    popSize = st.slider("Population Size", 10, 200, 50)
    generations = st.slider("Number of Generations", 1, 500, 100)
    crossoverRate = st.slider("Crossover Rate", 0.0, 1.0, 0.5)
    mutationRate = st.slider("Mutation Rate", 0.0, 1.0, 0.01)
    run = st.button("Run Simulation")

# --- Main App ---
if city_source == "Random":
    cities = np.random.rand(num_cities, 2) * 100
elif city_source == "From File":
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
else:
    cities = np.random.rand(10, 2) * 100  # fallback

if run:
    progress_bar = st.progress(0, text="GA Running...")
    ga = GA(cities=cities, populationSize=popSize, generations=generations, crossoverRate=crossoverRate, mutation_rate=mutationRate)
    best_dists = []
    best_path = None
    for gen in range(generations):
        ga.evaluation()
        ga.chromosomes.sort(key=lambda c: c.fitness)
        best_dists.append(ga.chromosomes[0].fitness)
        # Elitism: 保留最優個體
        new_population = [Chromosome(ga.chromosomes[0].genes.copy())]
        while len(new_population) < ga.populationSize:
            p1 = ga.select()
            p2 = ga.select()
            child = ga.crossover(p1, p2)
            ga.mutate(child)
            new_population.append(child)
        ga.chromosomes = new_population
        if best_path is None or ga.chromosomes[0].fitness < ga.chromosomes[0].fitness:
            best_path = ga.chromosomes[0].genes.copy()
        progress_bar.progress((gen+1)/generations, text=f"Generation {gen+1}/{generations}")
    # 最後再做一次評估，確保結果正確
    ga.evaluation()
    ga.chromosomes.sort(key=lambda c: c.fitness)
    best_path = ga.chromosomes[0].genes

    # --- Plotting ---
    st.subheader("🔍 Best Path Found")
    fig, ax = plt.subplots()
    coords = cities[best_path + [best_path[0]]]
    ax.plot(coords[:, 0], coords[:, 1], '-o')
    for i, (x, y) in enumerate(cities):
        ax.text(x, y, str(i), fontsize=8)
    st.pyplot(fig)

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