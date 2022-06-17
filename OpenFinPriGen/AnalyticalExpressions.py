from abc import ABC

import numpy as np
import pandas as pd
import statistics
import scipy.stats as si
from scipy.stats import norm

from OpenFinPriGen.Pricer import Pricer


class AnalyticalExpressions(Pricer, ABC):

    def __init__(self, s0: float, vanilla_style: str, k: float, tau: float, rf: float = 0, q: float = 0):
        """
                    This class describes the key parameters of Vanilla products as well as their payoff
                    @param s0: stock price at time zero
                    @param vanilla_style: call ("c") or put ("p").
                    @param k: Strike price of your option.
                    @param tau: Time until the end of life of the option.
                    @param rf: Risk free rate to apply for the calculations.default=0.
                    @param q: Dividend yield (if existing). Default=0.
        """
        self.s0 = s0
        self.vanilla_style = vanilla_style
        self.k = k
        self.tau = tau
        self.rf = rf
        self.q = q

    def PriceBlackScholes(self, sigma: float):
        d1 = (np.log(self.s0 / self.k) + (self.rf - self.q + sigma ** 2 * 0.5) * self.tau) / \
             (sigma * np.sqrt(self.tau))
        d2 = d1 - sigma * np.sqrt(self.tau)

        if self.vanilla_style == 'c':
            price = (self.s0 * np.exp(-self.q * self.tau) * si.norm.cdf(d1, 0.0, 1.0)
                     - self.k * np.exp(-self.rf * self.tau) * si.norm.cdf(d2, 0.0, 1.0))
            return price

        elif self.vanilla_style == 'p':
            price = (self.k * np.exp(-self.rf * self.tau) * si.norm.cdf(-d2, 0.0, 1.0)
                     - self.s0 * np.exp(-self.q * self.tau) * si.norm.cdf(-d1, 0.0, 1.0))
            return price

        else:
            print(f"No such option type, check function parameters")

    def DeltaBlackScholes(self, sigma):
        d1 = (np.log(self.s0 / self.k) + (self.rf - self.q + sigma ** 2 * 0.5) * self.tau) / (sigma * np.sqrt(self.tau))
        d2 = d1 - sigma * np.sqrt(self.tau)

        if self.vanilla_style == 'c':
            delta = np.exp(-self.q * self.tau) * norm.cdf(d1)
            return delta

        elif self.vanilla_style == 'p':
            delta = -np.exp(-self.q * self.tau) * norm.cdf(-d1)
            return delta

        else:
            print(f"No such option type, check function parameters")

    def GammaBlackScholes(self, sigma):
        d1 = (np.log(self.s0 / self.k) + (self.rf - self.q + sigma ** 2 * 0.5) * self.tau) / (sigma * np.sqrt(self.tau))
        gamma = np.exp(-self.q * self.tau) * norm.pdf(d1) / (self.s0 * sigma * np.sqrt(self.tau))
        return gamma

    def VegaBlackScholes(self, sigma):
        d1 = (np.log(self.s0 / self.k) + (self.rf - self.q + sigma ** 2 * 0.5) * self.tau) / (sigma * np.sqrt(self.tau))
        vega = 0.01 * np.exp(-self.q * self.tau) * (self.s0 * norm.pdf(d1) * np.sqrt(self.tau))
        return vega

