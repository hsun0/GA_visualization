import numpy as np
import random as rd
from numpy.typing import NDArray

# Calculate the distance between two points
def distance(point1: tuple, point2: tuple) -> float:
    return np.sqrt((point1[0] - point2[0]) ** 2 + (point1[1] - point2[1]) ** 2)

class Chromosome:
    def __init__(self, genes: list[int]):
        self.genes = genes
        self.fitness = 0

class GA:
    def __init__(self, cities: np.ndarray, populationSize: int, generations: int, crossoverRate: float, mutation_rate: float):
        self.cities = cities
        self.populationSize = populationSize
        self.generations = generations
        self.crossoverRate = crossoverRate
        self.mutationRate = mutation_rate
        self.num_cities = len(cities)
        self.elitismRate = 0.01
        self.elitismNum = min(1, int(self.populationSize * self.elitismRate))
        # self.elitismNum = 2
        # 初始化距離矩陣
        self.distMat = np.zeros((self.num_cities, self.num_cities))
        for i in range(self.num_cities):
            for j in range(self.num_cities):
                if i != j:
                    self.distMat[i][j] = np.linalg.norm(self.cities[i] - self.cities[j])
        # 初始化族群
        self.chromosomes = [Chromosome(list(rd.sample(range(self.num_cities), self.num_cities))) for _ in range(self.populationSize)]

    def evaluation(self):
        for chromosome in self.chromosomes:
            totalDistance = 0
            for i in range(self.num_cities):
                totalDistance += self.distMat[chromosome.genes[i]][chromosome.genes[(i + 1) % self.num_cities]]
            chromosome.fitness = totalDistance
        # Sort by fitness
        self.chromosomes.sort(key=lambda c: c.fitness)
        

    def select(self) -> Chromosome:
        parent1 = rd.choice(self.chromosomes)
        parent2 = rd.choice(self.chromosomes)
        return parent1 if parent1.fitness < parent2.fitness else parent2

    def crossover(self, p1: Chromosome, p2: Chromosome) -> Chromosome:
        if rd.random() > self.crossoverRate:
            return Chromosome(p1.genes.copy())
        start, end = sorted(rd.sample(range(self.num_cities), 2))
        childGenes = [-1] * self.num_cities
        childGenes[start:end + 1] = p1.genes[start:end + 1]
        ptr = 0
        for gene in p2.genes:
            if gene not in childGenes:
                while childGenes[ptr] != -1:
                    ptr += 1
                childGenes[ptr] = gene
        return Chromosome(childGenes)

    def mutate(self, individual: Chromosome):
        if rd.random() > self.mutationRate:
            return
        start, end = sorted(rd.sample(range(self.num_cities), 2))
        individual.genes[start:end + 1] = list(reversed(individual.genes[start:end + 1]))


    def local_search_2opt(self, individual: Chromosome):
        # 簡單 2-opt local search，嘗試改善路徑
        improved = True
        while improved:
            improved = False
            for i in range(1, self.num_cities - 2):
                for j in range(i + 1, self.num_cities):
                    if j - i == 1:
                        continue
                    new_genes = individual.genes[:]
                    new_genes[i:j] = reversed(new_genes[i:j])
                    # 計算新路徑長度
                    new_dist = 0
                    for k in range(self.num_cities):
                        new_dist += self.distMat[new_genes[k]][new_genes[(k + 1) % self.num_cities]]
                    if new_dist < individual.fitness:
                        individual.genes = new_genes
                        individual.fitness = new_dist
                        improved = True
                        break
                if improved:
                    break

    def run(self):
        best_dists = []
        for _ in range(self.generations):
            self.evaluation()
            new_population = [Chromosome(self.chromosomes[i].genes.copy()) for i in range(self.elitismNum)]
            while len(new_population) < self.populationSize:
                p1 = self.select()
                p2 = self.select()
                child = self.crossover(p1, p2)
                self.mutate(child)
                self.evaluation()  # 先算 fitness
                # self.local_search_2opt(child)  # 交配後加強
                new_population.append(child)
            self.chromosomes = new_population
            self.evaluation()
            best_dists.append(self.chromosomes[0].fitness)
        best_path = self.chromosomes[0].genes
        return best_path, best_dists