import matplotlib.pyplot as plt

from OpenFinPriGen.MonteCarloPricing import MonteCarloPricing
from OpenFinPriGen.AnalyticalExpressions import AnalyticalExpressions
from OpenFinPriGen.BlackScholesAnalytics import BlackScholesAnalytics
from OpenFinPriGen.InterestRateGen import InterestRateGen
import time
import pyEX
import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta
from pyEX.studies import *
import talib as t


N = 5000
T = 48
rf = 0.0153
q = 0.003
s0 = 43
k = 45
sigma = 0.2
dt = 1 / 1000


aapl_price = 1.18


def main():
    tickers = ["AAPL"]
    start_date = '2022-01-01'
    end_date = '2022-06-10'
    stock_data = yf.download(tickers, start=start_date, end=end_date)
    price = stock_data['Adj Close'].values
    print(price)

    my_analytics = AnalyticalExpressions(s0, "c", k, 12 / 250, rf, q)
    ret = my_analytics.getReturns(price)
    print(ret)

    hist_vol = my_analytics.HistoricalVol(price)
    print(hist_vol)

    # c = pyEX.Client(api_token='', version='v1', api_limit=5)
    # yield_df = pyEX.studies.yieldCurve(c, curves='DGS3MO', from_='2022-01-01', to_='2022-06-06', wide_or_long='wide')
    # yield_df = c.yieldCurve(curves='DGS3MO', from_='2022-01-01', to_='2022-06-06', wide_or_long='wide')
    # print(yield_df)

    start = time.time()
    my_MC_pricing = MonteCarloPricing("options", s0, k, sigma, T, N, "none", dt, "european", 0, "bsm", "c", "gbm",
                                      "arithmetic", rf, q)
    MC_price = my_MC_pricing.Price()
    end = time.time()
    elapsed = end - start
    print(f'Execution Time in seconds: ', elapsed)
    print(MC_price)

    my_analytical_expression_bs = BlackScholesAnalytics(s0, "c", k, 12 / 250, rf, q)
    BS_price = my_analytical_expression_bs.PriceBlackScholes(sigma)
    print(BS_price)

    # Test of implied volatility under Black-Scholes
    implied_vol_bsm = my_analytical_expression_bs.ImpliedVolBlackScholes(aapl_price)
    print(implied_vol_bsm)

    # Test of Vasicek generation
    my_interest_rate = InterestRateGen(N, T)
    interest_rate_df = my_interest_rate.vasicek(0.01, 0.3, 0.9, 0.2)
    print(interest_rate_df)
    plt.plot(interest_rate_df.iloc[0])
    plt.show()


if __name__ == '__main__':
    main()
