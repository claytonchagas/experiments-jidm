from solver import Solver
from model import Model
import time
import sys

def define_parameters(n):
    dimensionality = (2, 2)
    nx = 0.15
    ny = 0.15
    delta_t = n
    return dimensionality, nx, ny, delta_t

def create_model(nx, ny, dimensionality):
    model = Model(nx, ny, dimensionality)
    return model

def create_solver(model, delta_t):
    solver = Solver(model, delta_t)
    return solver

def run_solver(solver):
    solver.solve()

def main(n):
    dimensionality, nx, ny, delta_t = define_parameters(n)
    start_time = time.perf_counter()
    model = create_model(nx, ny, dimensionality)
    solver = create_solver(model, delta_t)
    run_solver(solver)
    end_time = time.perf_counter()
    print(end_time - start_time)

if __name__ == '__main__':
    n = float(sys.argv[1])
    main(n)
