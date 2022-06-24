from OpenFinPriGen.MonteCarloPricing import MonteCarloPricing
from OpenFinPriGen.AnalyticalExpressions import AnalyticalExpressions
from OpenFinPriGen.BlackScholesAnalytics import BlackScholesAnalytics
import time

N = 3000
T = 48
rf = 0.0153
q = 0.003
s0 = 43
k = 45
sigma = 0.22
dt = 1 / 1000


# aapl_price = 1.18


def main():
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
    # implied_vol_bsm = my_analytical_expression_bs.ImpliedVolBlackScholes(aapl_price)
    # print(implied_vol_bsm)


if __name__ == '__main__':
    main()
