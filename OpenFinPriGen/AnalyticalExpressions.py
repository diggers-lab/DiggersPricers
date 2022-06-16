from abc import ABC

import numpy as np
import pandas as pd
import statistics
import scipy.stats as si
from scipy.stats import norm

from OpenFinPriGen.Pricer import Pricer


class AnalyticalExpressions(Pricer, ABC):

    def __init__(self, s: pd.DataFrame, style: str, k: float, maturity: float, rf: float = 0, q: float = 0):
        """
                    This class describes the key parameters of Vanilla products as well as their payoff
                    @param s: stock price at time zero
                    @param style: call ("c") or put ("p").
                    @param k: Strike price of your option.
                    @param maturity: Time until the end of life of the option.
                    @param rf: Risk free rate to apply for the calculations.default=0.
                    @param q: Dividend yield (if existing). Default=0.
        """
        self.s = s
        self.style = style
        self.k = k
        self.maturity = maturity
        self.rf = rf
        self.q = q

    def PriceBlackScholes(self, sigma: float):
        d1 = (np.log(self.s / self.k) + (self.rf - self.q + sigma ** 2 * 0.5) * self.T) / (sigma * np.sqrt(self.T))
        d2 = d1 - sigma * np.sqrt(self.T)

        if self.style == 'c':
            price = (self.s.iat[0, 0] * np.exp(-self.q * self.maturity) * si.norm.cdf(d1, 0.0, 1.0)
                     - self.k * np.exp(-self.rf * self.maturity) * si.norm.cdf(d2, 0.0, 1.0))
            return price

        elif self.style == 'p':
            price = (self.k * np.exp(-self.rf * self.maturity) * si.norm.cdf(-d2, 0.0, 1.0)
                     - self.s.iat[0, 0] * np.exp(-self.q * self.maturity) * si.norm.cdf(-d1, 0.0, 1.0))
            return price

        else:
            print(f"No such option type, check function parameters")

    def DeltaBlackScholes(self, sigma):
        d1 = (np.log(self.s / self.k) + (self.rf - self.q + sigma ** 2 * 0.5) * self.T) / (sigma * np.sqrt(self.T))
        d2 = d1 - sigma * np.sqrt(self.T)

        if self.style == 'c':
            delta = np.exp(-self.q * self.maturity) * norm.cdf(d1)
            return delta

        elif self.style == 'p':
            delta = -np.exp(-self.q * self.maturity) * norm.cdf(-d1)
            return delta

        else:
            print(f"No such option type, check function parameters")

    def GammaBlackScholes(self, sigma):
        d1 = (np.log(self.s / self.k) + (self.rf - self.q + sigma ** 2 * 0.5) * self.T) / (sigma * np.sqrt(self.T))
        gamma = np.exp(-self.q * self.maturity) * norm.pdf(d1) / (self.s.iat[0, 0] * sigma * np.sqrt(self.maturity))
        return gamma

    def VegaBlackScholes(self, sigma):
        d1 = (np.log(self.s / self.k) + (self.rf - self.q + sigma ** 2 * 0.5) * self.T) / (sigma * np.sqrt(self.T))
        vega = 0.01 * np.exp(-self.q * self.maturity) * (self.s.iat[0, 0] * norm.pdf(d1) * np.sqrt(self.maturity))
        return vega

