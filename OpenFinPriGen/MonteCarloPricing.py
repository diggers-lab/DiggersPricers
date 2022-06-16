import numpy as np
import pandas as pd
from scipy.stats import stats

from OpenFinPriGen.Pricer import Pricer


class MonteCarloPricing(Pricer):

    def __init__(self, df_payoff: pd.DataFrame, r: pd.DataFrame, s: pd.DataFrame, k: float,
                 dt: float, option_style: str = "european"):
        """
                        This abstract class aims to provide different techniques to price financial instruments
                        @param df_payoff: the payoff must be a DataFrame
                        @param r: the evolution of interest rates must be described as a Dataframe
                        @param s: evolution of the underlying in a Dataframe. Useful for american-style option
                        @param k: strike considered for the underlying, float
                        @param dt: time consideration must be specified: float (monthly, daily, yearly)
                        @param option_style: "european" or "american"
        """
        Pricer.__init__(self, df_payoff, r, s, k, dt, option_style)

    def Price(self):

        tab_valuation = np.zeros(shape=(len(self.df_payoff), len(self.df_payoff.iloc[0])))
        df_eu_valuation = pd.DataFrame(tab_valuation)
        df_us_valuation = pd.DataFrame(tab_valuation)
        for j in range(len(df_eu_valuation.iloc[0]) - 2, -1, -1):
            for i in range(len(df_eu_valuation)):
                df_eu_valuation.iat[i, j] = np.exp(-self.dt * self.r.iat[i, j]) * (self.df_payoff.iat[i, j + 1]
                                                                                   + df_eu_valuation.iat[i, j + 1])
        if self.option_style == "european":
            print(df_eu_valuation)
            MC_price = np.mean(df_eu_valuation[0])
        elif self.option_style == "american":
            for j in range(len(df_us_valuation.iloc[0]) - 1, -1, -1):
                for i in range(len(df_us_valuation)):
                    df_us_valuation.iat[i, j] = max(self.s.iat[i, j]-self.k, df_eu_valuation[i, j])
            MC_price = np.mean(df_us_valuation[0])
        return MC_price
