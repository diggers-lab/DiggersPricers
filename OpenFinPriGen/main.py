import matplotlib.pyplot as plt
import yfinance as yf
import pandas as pd
import numpy as np
from OpenFinPriGen.BlackScholesGen import BlackScholesGen
from OpenFinPriGen.ExoticOptions import ExoticOptions
from OpenFinPriGen.MonteCarloPricing import MonteCarloPricing

N = 1000
T = 12
rf = 0.01
q = 0.003
s0 = 45
sigma = 0.25
dt = 1 / 250


def main():
    my_GBM = BlackScholesGen(N, T, rf, q, s0, sigma, dt)
    GBM = my_GBM.path_generate()
    print(GBM)
    df = pd.DataFrame
    my_exotic_option = ExoticOptions(GBM, df, "c", 46, T, N, "a", 0, "arithmetic", rf, q)
    df_payoff = my_exotic_option.payoff_exotic()
    print(df_payoff)
    tab_r = np.ones(N, T)
    r = pd.DataFrame(tab_r)
    my_MC_pricing = MonteCarloPricing(df_payoff, r, GBM, 46, dt, "european")




if __name__ == '__main__':
    main()
