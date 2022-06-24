from abc import ABC

import numpy as np
import pandas as pd
import scipy.stats as si
from scipy.stats import norm

from OpenFinPriGen.AnalyticalExpressions import AnalyticalExpressions


class BlackScholesAnalytics(AnalyticalExpressions, ABC):

    def __init__(self, s0: float, vanilla_style: str, k: float, tau: float, rf: float = 0, q: float = 0):
        """
            This class provides the different closed-form expressions obtained with Black-Scholes-Merton
            @param s0: stock price at time zero, float
            @param vanilla_style: call ("c") or put ("p"), str
            @param k: Strike price of your option, float
            @param tau: Time until the end of life of the option, float
            @param rf: Risk free rate to apply for the calculations, default=0.
            @param q: Dividend yield (if existing), default=0.
        """
        AnalyticalExpressions.__init__(self, s0, vanilla_style, k, tau, rf, q)

    def d12(self, sigma: float):
        d1 = (np.log(self.s0 / self.k) + (self.rf - self.q + sigma ** 2 * 0.5) * self.tau) / \
             (sigma * np.sqrt(self.tau))
        d2 = d1 - sigma * np.sqrt(self.tau)
        return d1, d2

    def PriceBlackScholes(self, sigma: float):
        d1, d2 = self.d12(sigma)

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
        d1, d2 = self.d12(sigma)

        if self.vanilla_style == 'c':
            delta = np.exp(-self.q * self.tau) * norm.cdf(d1)
            return delta

        elif self.vanilla_style == 'p':
            delta = -np.exp(-self.q * self.tau) * norm.cdf(-d1)
            return delta

        else:
            print(f"No such option type, check function parameters")

    def GammaBlackScholes(self, sigma):
        d1, d2 = self.d12(sigma)
        gamma = np.exp(-self.q * self.tau) * norm.pdf(d1) / (self.s0 * sigma * np.sqrt(self.tau))
        return gamma

    def VegaBlackScholes(self, sigma):
        d1, d2 = self.d12(sigma)
        vega = 0.01 * np.exp(-self.q * self.tau) * (self.s0 * norm.pdf(d1) * np.sqrt(self.tau))
        return vega

    def ImpliedVolBlackScholes(self, market_price):
        implied_vol_bs = 0.001
        if self.vanilla_style == 'c':
            while implied_vol_bs < 1:
                d1, d2 = self.d12(implied_vol_bs)
                price_implied = self.s0 * np.exp(-self.q * self.tau) * norm.cdf(d1) - \
                                self.k * np.exp(-self.rf * self.tau) * norm.cdf(d2)
                if market_price - price_implied < 0.001:
                    return implied_vol_bs
                implied_vol_bs += 0.001
            return "Implied volatility not found"
        if self.vanilla_style == 'p':
            self.vanilla_style = 'c'
            while implied_vol_bs < 1:
                price_implied = self.k * np.exp(-self.rf * self.tau) - self.s0 * np.exp(-self.q * self.tau) \
                                + self.PriceBlackScholes(implied_vol_bs)
                if market_price - price_implied < 0.001:
                    return implied_vol_bs
                implied_vol_bs += 0.001
            return "Implied volatility not found"
