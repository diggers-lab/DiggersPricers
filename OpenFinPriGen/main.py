import matplotlib.pyplot as plt

from OpenFinPriGen.MonteCarloPricing import MonteCarloPricing
from OpenFinPriGen.AnalyticalExpressions import AnalyticalExpressions
from OpenFinPriGen.BlackScholesAnalytics import BlackScholesAnalytics
from OpenFinPriGen.InterestRateGen import InterestRateGen
from OpenFinPriGen.HestonGen import HestonGen
import time
import numpy as np
import pyEX
import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta
from pyEX.studies import *
import talib as t

N = 5000
T = 1200
rf = 0.0153
q = 0.003
s0 = 43
k = 45
sigma = 0.04
dt = 1 / 100
kappa = 0.125
theta = 0.20
volvol = 0.2
rho = -0.6

aapl_price = 1.18


def main():

    # Testing Heston Dynamics
    # my_heston_gen = HestonGen(N, T, rf, q, s0, sigma, dt, kappa, theta, volvol, rho)
    # my_heston_price = my_heston_gen.PathGenerate()
    #
    # # Testing Analytical Expressions
    # tickers = ["AAPL"]
    # start_date = '2022-01-01'
    # end_date = '2022-06-10'
    # stock_data = yf.download(tickers, start=start_date, end=end_date)
    # price = stock_data['Adj Close'].values
    # # print(price)
    #
    # my_analytics = AnalyticalExpressions(s0, "c", k, 12 / 250, rf, q)
    # ret = my_analytics.getReturns(price)
    # # print(ret)
    #
    # hist_vol = my_analytics.HistoricalVol(price)
    # # print(hist_vol)
    #
    # # Testing IEXCloud Data - Calibration
    # my_client = pyEX.Client(api_token="", version="sandbox")
    # my_options = my_client.options("AAPL", expiration="20220923", format='json')
    # df = pd.DataFrame(my_options)
    #
    # # print(df['side'].iloc[0])
    # # print(df.columns)
    # # print(df['side'])
    #
    # temp = []
    # for i in range(len(df)):
    #     call_type = df['side'].iloc[i]
    #     if "p" in call_type:
    #         temp.append(i)
    # print(temp)
    # df = df.drop(labels=temp)
    # print(df)

    # # Testing MC Pricing
    # start = time.time()
    # # my_MC_pricing = MonteCarloPricing("options", s0, k, sigma, T, N, "none", dt, "european", 0, "bsm", "c", "gbm",
    # #                                  "arithmetic", rf, q)
    # my_MC_pricing = MonteCarloPricing("options", s0, k, sigma, T, N, "none", dt, "european", 0, "bsm", "c", "heston",
    #                                   kappa, theta, volvol, rho, "arithmetic", rf, q)
    # MC_price = my_MC_pricing.Price()
    # end = time.time()
    # elapsed = end - start
    # print(f'Execution Time in seconds: ', elapsed)
    # print(MC_price)
    #
    # Testing BSM Analytical expressions
    # my_analytical_expression_bs = BlackScholesAnalytics(s0, "c", k, 12 / 250, rf, q)
    # BS_price = my_analytical_expression_bs.PriceBlackScholes(sigma)
    # print(BS_price)
    #
    # # Test of implied volatility under Black-Scholes
    # implied_vol_bsm = my_analytical_expression_bs.ImpliedVolBlackScholes(aapl_price)
    # print(implied_vol_bsm)

    # Test of Vasicek generation
    my_interest_rate = InterestRateGen(N, T)
    interest_rate_df = my_interest_rate.vasicek(0.01, 0.5, 0.75, 0.2)
    print(interest_rate_df)
    plt.plot(interest_rate_df.iloc[1])
    plt.plot(interest_rate_df.iloc[2])
    plt.ylabel("Rates")
    plt.title("Examples of Vasicek paths")
    plt.show()


if __name__ == '__main__':
    main()
