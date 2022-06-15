from abc import abstractmethod

import numpy as np
import pandas as pd
from scipy.stats import stats


class Pricer:
    def __init__(self, df_payoff: pd.DataFrame, r: pd.DataFrame, s: pd.DataFrame, k: float, dt: float,
                 option_style: str = "european"):
        """
                        This abstract class aims to provide different techniques to price financial instruments
                        @param df_payoff: the payoff must be a DataFrame
                        @param r: the evolution of interest rates must be described as a Dataframe
                        @param s: evolution of the underlying in a Dataframe. Useful for american-style option
                        @param k: strike considered for the underlying, float
                        @param dt: time consideration must be specified: float (monthly, daily, yearly)
                        @param option_style: "european" or "american"
        """
        self.df_payoff = df_payoff
        self.r = r
        self.s = s
        self.k = k
        self.dt = dt
        self.option_style = option_style

    @abstractmethod
    def price(self, df_payoff: pd.DataFrame, r: pd.DataFrame, s: pd.DataFrame, k: float,
              dt: float, option_style: str = "european"):
        pass
