from OpenFinPriGen.BlackScholesGen import BlackScholesGen
from OpenFinPriGen.ExoticOptions import ExoticOptions
from OpenFinPriGen.MonteCarloPricing import MonteCarloPricing
from OpenFinPriGen.AnalyticalExpressions import AnalyticalExpressions
from OpenFinPriGen.StructuredProducts import StructuredProducts

N = 10000
T = 12
rf = 0.01
q = 0.003
s0 = 45
k = 46
sigma = 0.25
dt = 1 / 250


def main():
    # FORMER VERSION

    # my_GBM = BlackScholesGen(N, T, rf, q, s0, sigma, dt)
    # GBM = my_GBM.PathGenerate()
    # print(GBM)
    # df = pd.DataFrame
    # my_exotic_option = ExoticOptions(GBM, df, "c", 46, T, N, "none", 0, "arithmetic", rf, q)

    # NEW VERSION

    # my_exotic_option = ExoticOptions(s0, k, sigma, T, N, "none", 0, "c", "bsm", "arithmetic", rf, q)
    # df_payoff = my_exotic_option.PayoffExotic()
    # print(df_payoff)

    my_MC_pricing = MonteCarloPricing("options", s0, k, sigma, T, N, "none", dt, "american", 0, "bsm", "c", "bsm",
                                      "arithmetic", rf, q)
    MC_price = my_MC_pricing.Price()
    print(MC_price)

    my_analytical_expression_bs = AnalyticalExpressions(s0, "c", 46, T / 250, rf, q)
    BS_price = my_analytical_expression_bs.PriceBlackScholes(sigma)
    print(BS_price)


if __name__ == '__main__':
    main()
