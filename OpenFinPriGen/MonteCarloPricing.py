from abc import ABC

import numpy as np
import pandas as pd

from OpenFinPriGen.Pricer import Pricer
from OpenFinPriGen.ExoticOptions import ExoticOptions


class MonteCarloPricing(Pricer, ABC):

    def __init__(self, payoff_product: str, s0: float, k: float, sigma: float, T: int,
                 N: int, exotic_style: str, dt: float, option_style: "str",
                 barrier: float, rate_model: str, vanilla_style: str, underlying_style: str,
                 mean_style: str = "arithmetic", rf: float = 0, q: float = 0):
        """
                        Subclass of Pricer, with Price() method override. The goal is to price any instruments thanks to
                        Monte-Carlo methods.

                        @param payoff_product: payoff type (options, fixed-income...), str
                        @param s0: underlying price at time t=0, float
                        @param k: strike considered for the underlying, float
                        @param sigma: voaltility considered for pricing, float
                        @param T: time until maturity, int
                        @param N: number of trajectories simulated, int
                        @param exotic_style: exotic-style specified ("none","a","do","di","uo","ui"), str
                        @param dt: time consideration must be specified: float (monthly, daily, yearly)
                        @param option_style: "european" or "american"
                        @param barrier: barrier considered for barrier options, float
                        @param rate_model: rate model specified, str
                        @param vanilla_style: call ("c") or put ("p"), str
                        @param underlying_style: underlying considered ("gbm"), str
                        @param mean_style: type of mean considered for asian options ("arithmetic" or "geometric"), str
                        @param rf: risk-free interest rate
                        @param q: dividend yield
        """
        Pricer.__init__(self, payoff_product, rate_model, k, dt, option_style)
        self.s0 = s0
        self.k = k
        self.sigma = sigma
        self.T = T
        self.N = N
        self.exotic_style = exotic_style
        self.barrier = barrier
        self.rate_model = rate_model
        self.vanilla_style = vanilla_style
        self.underlying_style = underlying_style
        self.mean_style = mean_style
        self.rf = rf
        self.q = q

    def Price(self):
        if self.payoff_product == "options":

            if self.underlying_style == "gbm" and self.rate_model == "bsm" and self.option_style == 'american':
                r = self.rf * np.ones(shape=(self.N, self.T))
                r = pd.DataFrame(r)

            my_exotic_option = ExoticOptions(self.s0, self.k, self.sigma, self.T, self.N,
                                             self.exotic_style, self.dt,
                                             self.barrier, self.vanilla_style, self.underlying_style, self.mean_style,
                                             self.rf,
                                             self.q)
            payoff, s = my_exotic_option.PayoffExotic()

        if self.underlying_style == "gbm" and self.rate_model == "bsm" and self.option_style == 'european':
            MC_price = np.exp(-self.rf * self.T) * np.mean(payoff[self.T - 1])
            return MC_price

        valuation = np.zeros(shape=(len(payoff), len(payoff.iloc[0])))
        eu_valuation = pd.DataFrame(valuation)
        us_valuation = pd.DataFrame(valuation)
        for j in range(len(eu_valuation.iloc[0]) - 2, -1, -1):
            for i in range(len(eu_valuation)):
                eu_valuation.iat[i, j] = np.exp(-self.dt * r.iat[i, j]) * (payoff.iat[i, j + 1]
                                                                           + eu_valuation.iat[i, j + 1])
        if self.option_style == "european":
            MC_price = np.mean(eu_valuation[0])
        elif self.option_style == "american":
            for j in range(len(us_valuation.iloc[0]) - 1, -1, -1):
                for i in range(len(us_valuation)):
                    us_valuation.iat[i, j] = max(s.iat[i, j] - self.k, eu_valuation.iat[i, j])
            MC_price = np.mean(us_valuation[0])
        return MC_price
