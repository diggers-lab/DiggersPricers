from abc import ABC

import numpy as np
import pandas as pd
from scipy.stats import stats

from OpenFinPriGen.Pricer import Pricer
from OpenFinPriGen.ExoticOptions import ExoticOptions
from OpenFinPriGen.BlackScholesGen import BlackScholesGen


class MonteCarloPricing(Pricer, ABC):

    def __init__(self, payoff_product: str, s0: float, k: float, sigma: float, maturity: int,
                 trajectories: int, exotic_style: str, dt: float, option_style: "str",
                 barrier: float, rate_model: str, vanilla_style: str, underlying_style: str,
                 mean_style: str = "arithmetic", rf: float = 0, q: float = 0):
        """
                        This abstract class aims to provide different techniques to price financial instruments
                        @param payoff_product: the payoff must be a DataFrame
                        @param : the evolution of interest rates must be described as a Dataframe
                        @param s0: Stock price at time zero
                        @param k: strike considered for the underlying, float
                        @param dt: time consideration must be specified: float (monthly, daily, yearly)
                        @param option_style: "european" or "american"
        """
        Pricer.__init__(self, payoff_product, rate_model, k, dt, option_style)
        self.s0 = s0
        self.k = k
        self.sigma = sigma
        self.maturity = maturity
        self.trajectories = trajectories
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
            if self.underlying_style == "bsm" and self.rate_model == "bsm":
                tab_r = self.rf * np.ones(shape=(self.trajectories, self.maturity))
                r = pd.DataFrame(tab_r)

            my_exotic_option = ExoticOptions(self.s0, self.k, self.sigma, self.maturity, self.trajectories,
                                             self.exotic_style, self.dt,
                                             self.barrier, self.vanilla_style, self.underlying_style, self.mean_style,
                                             self.rf,
                                             self.q)
            df_payoff, s = my_exotic_option.PayoffExotic()
            # print(df_payoff)
            # print(s)

        tab_valuation = np.zeros(shape=(len(df_payoff), len(df_payoff.iloc[0])))
        df_eu_valuation = pd.DataFrame(tab_valuation)
        df_us_valuation = pd.DataFrame(tab_valuation)
        for j in range(len(df_eu_valuation.iloc[0]) - 2, -1, -1):
            for i in range(len(df_eu_valuation)):
                df_eu_valuation.iat[i, j] = np.exp(-self.dt * r.iat[i, j]) * (df_payoff.iat[i, j + 1]
                                                                              + df_eu_valuation.iat[i, j + 1])
        if self.option_style == "european":
            # print(df_eu_valuation)
            MC_price = np.mean(df_eu_valuation[0])
        elif self.option_style == "american":
            for j in range(len(df_us_valuation.iloc[0]) - 1, -1, -1):
                for i in range(len(df_us_valuation)):
                    df_us_valuation.iat[i, j] = max(s.iat[i, j] - self.k, df_eu_valuation.iat[i, j])
            MC_price = np.mean(df_us_valuation[0])
        return MC_price
