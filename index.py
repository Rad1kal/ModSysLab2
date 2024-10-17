import time
import matplotlib.pyplot as plt
import numpy as np
from random import random

class LinearCongruentialGenerator:
    def __init__(self, seed, a, c, m):
        self.seed = seed
        self.a = a
        self.c = c
        self.m = m
        self.current = seed

    def next(self):
        self.current = (self.a * self.current + self.c) % self.m
        return self.current

seed = 1234
a = 1103515245
c = 12345
m = 2**32

lcg = LinearCongruentialGenerator(seed, a, c, m)

# Генерация нескольких псевдослучайных чисел
for _ in range(10):
    print(lcg.next())

def calculate_period(lcg):
    seen = {}
    count = 0
    while lcg.current not in seen:
        seen[lcg.current] = count
        lcg.next()
        count += 1
        print(count)
    return count

period = calculate_period(lcg)
print(f"Длина периода: {period}")

def evaluate_distribution(lcg, num_samples, end_title):
    samples = [lcg() for _ in range(num_samples)]
    plt.hist(samples, bins=100, density=True)
    plt.title('Распределение псевдослучайных чисел', end_title)
    plt.show()

evaluate_distribution(lambda: lcg.next(), 100000, 'lcg')
evaluate_distribution(lambda: random()*100000000000000000, 100000, 'random')

def evaluate_autocorrelation(lcg, num_samples, end_title):
    samples = np.array([lcg() for _ in range(num_samples)])
    autocorr = np.correlate(samples - np.mean(samples), samples - np.mean(samples), mode='full')
    autocorr = autocorr[autocorr.size // 2:]
    plt.plot(autocorr[:100])  # Корреляция на первых 100 лагах
    plt.title('Автокорреляционная функция '+ end_title)
    plt.show()

evaluate_autocorrelation(lambda: lcg.next(), 100000, 'lcg')
evaluate_autocorrelation(lambda: random()*100000000000000000, 100000, 'random')

def evaluate_speed(lcg, num_samples, end_title):
    start_time = time.time()
    for _ in range(num_samples):
        lcg()
    end_time = time.time()
    elapsed_time = end_time - start_time
    print(f"Скорость генерации: {num_samples / elapsed_time} чисел в секунду для", end_title)

evaluate_speed(lambda: lcg.next(), 1000000, 'lcg')
evaluate_speed(lambda: random(), 1000000, 'random')
