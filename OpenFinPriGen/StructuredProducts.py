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

    def __init__(self, s: pd.DataFrame, position: str, style: str, k: float, maturity: float, trajectories: int,
                 rf: float = 0, q: float = 0):

        """
                This class describes the key parameters of Vanilla products as well as their payoff
                @param s: stock price evolution described in a DataFrame
                @param position: "sell" or "long"
                @param style: call ("c") or put ("p").
                @param k: Strike price of your option.
                @param maturity: Time until the end of life of the option.
                @param trajectories: Number of trajectories eq. number of rows in the dataframe
                @param rf: Risk free rate to apply for the calculations.default=0.
                @param q: Dividend yield (if existing). Default=0.
        """

        StructuredProducts.__init__(self, s)
        self.position = position
        self.style = style
        self.k = k
        self.maturity = maturity
        self.trajectories = trajectories
        self.rf = rf
        self.q = q

    def payoff(self, s):
        tab = np.zeros(shape=(self.trajectories, self.maturity))
        df = pd.DataFrame(tab)

        if self.position == "long" and self.style == "c":
            for i in range(self.trajectories):
                df.iat[i, self.maturity - 1] = max(self.s.iat[i, self.maturity - 1] - self.k, 0)

        elif self.position == "long" and self.style == "p":
            for i in range(self.trajectories):
                df.iat[i, self.maturity - 1] = max(self.k - self.s.iat[i, self.maturity - 1], 0)

        elif self.position == "short" and self.style == "c":
            for i in range(self.trajectories):
                df.iat[i, self.maturity - 1] = min(self.k - self.s.iat[i, self.maturity - 1], 0)

        elif self.position == "short" and self.style == "p":
            for i in range(self.trajectories):
                df.iat[i, self.maturity - 1] = min(self.s.iat[i, self.maturity - 1] - self.k, 0)
        else:
            raise Exception("Combination (position, style) not existing. Check your input.")

        return df


class ExoticOptions(StructuredProducts):

    def __init__(self, s: pd.DataFrame, position: str, style: str, k: float, maturity: float, trajectories: int,
                 barrier: float,
                 rf: float = 0, q: float = 0):
        StructuredProducts.__init__(self, s)
        self.position = position
        self.style = style
        self.k = k
        self.maturity = maturity
        self.trajectories = trajectories
        self.barrier = barrier
        self.rf = rf
        self.q = q

    def payoff(self, s):
        tab = np.zeros(shape=(self.trajectories, self.maturity))
        df = pd.DataFrame(tab)

        if self.position == "long" and self.style == "a":
            for i in range(self.trajectories):
                A_T = np.sum(self.s.iloc[i])
                df[i, self.maturity - 1] = max(A_T - self.k, 0)

        elif self.position == "short" and self.style == "a":
            for i in range(self.trajectories):
                A_T = np.sum(self.s.iloc[i])
                df[i, self.maturity - 1] = min(self.k - A_T, 0)

        else:
            raise Exception("Combination (position, style) not existing. Check your input.")

        return df
