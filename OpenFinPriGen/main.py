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
tab_r = rf * np.ones(shape=(N, T))
r = pd.DataFrame(tab_r)


def main():
    my_GBM = BlackScholesGen(N, T, rf, q, s0, sigma, dt)
    GBM = my_GBM.PathGenerate()
    print(GBM)
    df = pd.DataFrame
    my_exotic_option = ExoticOptions(GBM, df, "c", 46, T, N, "a", 0, "arithmetic", rf, q)
    df_payoff = my_exotic_option.PayoffExotic()
    print(df_payoff)
    my_MC_pricing = MonteCarloPricing(df_payoff, r, GBM, 46, dt, "european")
    MC_price = my_MC_pricing.Price()
    print(MC_price)


if __name__ == '__main__':
    main()
