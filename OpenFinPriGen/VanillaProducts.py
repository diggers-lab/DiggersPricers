import numpy as np
import pandas as pd
from scipy.stats import stats

from OpenFinPriGen import StructuredProducts


class VanillaProducts(StructuredProducts):

    def __init__(self, s: pd.DataFrame, df_options: pd.DataFrame, style: str, k: float, maturity: float,
                 trajectories: int, rf: float = 0, q: float = 0):

        """
                This class describes the key parameters of Vanilla products as well as their payoff
                @param s: stock price evolution described in a DataFrame
                @param df_options : Dataframe describing the payoff along each trajectory
                @param style: call ("c") or put ("p").
                @param k: Strike price of your option.
                @param maturity: Time until the end of life of the option.
                @param trajectories: Number of trajectories eq. number of rows in the dataframe
                @param rf: Risk free rate to apply for the calculations.default=0.
                @param q: Dividend yield (if existing). Default=0.
        """

        StructuredProducts.__init__(self, s)
        self.df_options = df_options
        self.style = style
        self.k = k
        self.maturity = maturity
        self.trajectories = trajectories
        self.rf = rf
        self.q = q

    def payoff(self):
        if self.style == "c":
            for i in range(self.trajectories):
                self.df_options.iat[i, self.maturity - 1] = max(self.s.iat[i, self.maturity - 1] - self.k, 0)

        elif self.style == "p":
            for i in range(self.trajectories):
                self.df_options.iat[i, self.maturity - 1] = max(self.k - self.s.iat[i, self.maturity - 1], 0)

        else:
            raise Exception("Combination (position, style) not existing. Check your input.")

        return self.df_options
