from OpenFinPriGen.BlackScholesGen import BlackScholesGen
from OpenFinPriGen.ExoticOptions import ExoticOptions
from OpenFinPriGen.MonteCarloPricing import MonteCarloPricing
from OpenFinPriGen.AnalyticalExpressions import AnalyticalExpressions
from OpenFinPriGen.StructuredProducts import StructuredProducts
import datetime
import time

N = 1000
T = 10
rf = 0.0153
q = 0.003
s0 = 45
k = 47
sigma = 0.20
dt = 1 / 250


def main():
    start = time.time()
    my_MC_pricing = MonteCarloPricing("options", s0, k, sigma, T, N, "none", dt, "american", 0, "bsm", "c", "gbm",
                                      "arithmetic", rf, q)
    MC_price = my_MC_pricing.Price()
    end = time.time()
    elapsed = end - start
    print(f'Execution Time in seconds: ', elapsed)

    print(MC_price)

    my_analytical_expression_bs = AnalyticalExpressions(s0, "c", k, T / 250, rf, q)
    BS_price = my_analytical_expression_bs.PriceBlackScholes(sigma)
    print(BS_price)


if __name__ == '__main__':
    main()
