from abc import abstractmethod

import numpy as np
import pandas as pd
from scipy.stats import stats


class StructuredProducts:

    def __init__(self, s: pd.DataFrame):
        """ @param s: underlying described in a DataFrame"""
        self.s = s

    @abstractmethod
    def payoff(self, s):
        pass


class VanillaProducts(StructuredProducts):

    def __init__(self, s: pd.DataFrame, style: str, k: float, maturity: float, trajectories: int,
                 rf: float = 0, q: float = 0):

        """
                This class describes the key parameters of Vanilla products as well as their payoff
                @param s: stock price evolution described in a DataFrame
                @param style: call ("c") or put ("p").
                @param k: Strike price of your option.
                @param maturity: Time until the end of life of the option.
                @param trajectories: Number of trajectories eq. number of rows in the dataframe
                @param rf: Risk free rate to apply for the calculations.default=0.
                @param q: Dividend yield (if existing). Default=0.
        """

        StructuredProducts.__init__(self, s)
        self.style = style
        self.k = k
        self.maturity = maturity
        self.trajectories = trajectories
        self.rf = rf
        self.q = q

    def payoff(self, s):
        tab = np.zeros(shape=(self.trajectories, self.maturity))
        df = pd.DataFrame(tab)

        if self.style == "c":
            for i in range(self.trajectories):
                df.iat[i, self.maturity - 1] = max(self.s.iat[i, self.maturity - 1] - self.k, 0)

        elif self.style == "p":
            for i in range(self.trajectories):
                df.iat[i, self.maturity - 1] = max(self.k - self.s.iat[i, self.maturity - 1], 0)

        else:
            raise Exception("Combination (position, style) not existing. Check your input.")

        return df


class ExoticOptions(VanillaProducts):

    def __init__(self, s: pd.DataFrame, style: str, k: float, maturity: float, trajectories: int, exotic_style: str,
                 barrier: float, mean_style: str = "arithmetic", rf: float = 0, q: float = 0):
        VanillaProducts.__init__(self, s, style, k, maturity, trajectories, rf, q)
        self.exotic_style = exotic_style
        self.barrier = barrier
        self.mean_style = mean_style

    def payoff_exotic(self, s):
        tab = np.zeros(shape=(self.trajectories, self.maturity))
        df_exotic = pd.DataFrame(tab)

        if self.exotic_style == "a" and self.mean_style == "arithmetic":
            for i in range(self.trajectories):
                A_T = np.mean(self.s.iloc[i])
                df_exotic.iat[i, self.maturity - 1] = A_T
            VanillaProducts.payoff(self, df_exotic)
        if self.exotic_style == "a" and self.mean_style == "geometric":
            for i in range(self.trajectories):
                A_T = 1
                for j in range(self.maturity):
                    A_T = A_T * self.s.iat[i, j]
                df_exotic.iat[i, self.maturity - 1] = A_T ^ (1 / self.maturity)
            VanillaProducts.payoff(self, df_exotic)

        elif self.exotic_style == "do":
            for i in range(self.trajectories):
                if np.min(self.s.iloc[i]) > self.barrier:
                    df_exotic.iat[i, self.maturity - 1] = self.s.iat[i, self.maturity - 1]
                else:
                    df_exotic.iat[i, self.maturity - 1] = 0
            VanillaProducts.payoff(self, df_exotic)

        elif self.exotic_style == "di":
            for i in range(self.trajectories):
                if np.min(self.s.iloc[i]) <= self.barrier:
                    df_exotic.iat[i, self.maturity - 1] = self.s.iat[i, self.maturity - 1]
                else:
                    df_exotic.iat[i, self.maturity - 1] = 0
            VanillaProducts.payoff(self, df_exotic)

        elif self.exotic_style == "uo":
            for i in range(self.trajectories):
                if np.max(self.s.iloc[i]) < self.barrier:
                    df_exotic.iat[i, self.maturity - 1] = self.s.iat[i, self.maturity - 1]
                else:
                    df_exotic.iat[i, self.maturity - 1] = 0
            VanillaProducts.payoff(self, df_exotic)

        elif self.exotic_style == "ui":
            for i in range(self.trajectories):
                if np.max(self.s.iloc[i]) >= self.barrier:
                    df_exotic.iat[i, self.maturity - 1] = self.s.iat[i, self.maturity - 1]
                else:
                    df_exotic.iat[i, self.maturity - 1] = 0
            VanillaProducts.payoff(self, df_exotic)

        else:
            raise Exception("Combination (position, style) not existing. Check your input.")
