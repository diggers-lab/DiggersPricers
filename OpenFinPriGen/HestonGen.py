from abc import ABC

import matplotlib.pyplot as plt
from math import log, sqrt, pi, exp
import scipy.special
import matplotlib.pylab as pylab

from scipy.optimize import minimize
import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
from scipy.optimize import dual_annealing

import numpy as np
import pandas as pd

from OpenFinPriGen.StockGen import StockGen


class HestonGen(StockGen, ABC):
    """
        Subclass of StockGen, that generates the stock
        as it is specified by Heston assumptions.
    """

    def __init__(self, N: int, T: int, r: float, q: float, s0: float, sigma: float, dt: float, kappa: float,
                 theta: float, volvol: float, rho: float):
        StockGen.__init__(self, N, T)
        self.r = r
        self.q = q
        self.s0 = s0
        self.sigma = sigma
        self.dt = dt
        self.kappa = kappa
        self.theta = theta
        self.volvol = volvol
        self.rho = rho

    def PathGenerate(self):
        price = np.zeros(shape=(self.N, self.T))
        volatility = np.zeros(shape=(self.N, self.T))
        price[:, 0] = self.s0
        volatility[:, 0] = self.sigma

        means = [0, 0]
        stdevs = [1, 1]
        covs = [[stdevs[0] ** 2, stdevs[0] * stdevs[1] * self.rho],
                [stdevs[0] * stdevs[1] * self.rho, stdevs[1] ** 2]]

        Z = np.random.multivariate_normal(means, covs, (self.T, self.N))

        for i in range(1, self.T):
            # Use Z2 to calculate Vt
            Z2 = Z[i - 1]
            volatility[:, i] = np.maximum(volatility[:, i - 1] +
                                          self.kappa * (self.theta - volatility[:, i - 1]) * self.dt + self.volvol
                                          * np.sqrt(volatility[:, i - 1] * self.dt) * Z2[:, 1], 0.05)

            # Use all V_t calculated to find the value of S_t
            price[:, i] = price[:, i - 1] + self.r * price[:, i - 1] * self.dt + np.sqrt(volatility[:, i - 1] * self.dt) \
                          * price[:, i - 1] * Z2[:, 0]
        price = pd.DataFrame(price)
        print(price)
        volatility = pd.DataFrame(volatility)
        return price, volatility

    # To be used in the Heston Analytical pricing
    def fHeston(self, s, s0, K, r, T, sigma, kappa, theta, volvol, rho):
        i = complex(0, 1)
        prod = rho * sigma * i * s

        d1 = (prod - kappa) ** 2
        d2 = (sigma ** 2) * (-2 * i * s + s ** 2)
        d = np.sqrt(d1 + d2)

        g1 = kappa - prod - d
        g2 = kappa - prod + d
        g = g1 / g2
        # Calculate first exponential
        exp1 = np.exp(np.log(s0) * i * s) * np.exp(i * s * r * T)
        exp2 = 1 - g * np.exp(-d * T)
        exp3 = 1 - g
        mainExp1 = exp1 * np.power(exp2 / exp3, -2 * theta * kappa / (sigma ** 2))
        # Calculate second exponential
        exp4 = theta * kappa * T / (sigma ** 2)
        exp5 = volvol / (sigma ** 2)
        exp6 = (1 - np.exp(-d * T)) / (1 - g * np.exp(-d * T))
        mainExp2 = np.exp((exp4 * g1) + (exp5 * g1 * exp6))
        return mainExp1 * mainExp2

    # Heston Pricer
    def priceHestonMid(self, s0, K, r, q, T, sigma, kappa, theta, volvol, rho):
        i = complex(0, 1)
        P, iterations, maxNumber = 0, 1000, 100
        ds = maxNumber / iterations
        element1 = 0.5 * (s0 * np.exp(-q * T) - K * np.exp(-r * T))
        # Calculate the complex integral
        # Using j instead of i to avoid confusion
        for j in range(1, iterations):
            s1 = ds * (2 * j + 1) / 2
            s2 = s1 - i
            numerator1 = self.fHeston(s2, s0, K, r, T,
                                      sigma, kappa, theta, volvol, rho)
            numerator2 = K * self.fHeston(s1, s0, K, r, T, sigma, kappa, theta, volvol, rho)
            denominator = np.exp(np.log(K) * i * s1) * i * s1
            P += ds * (numerator1 - numerator2) / denominator
        element2 = P / np.pi
        return np.real((element1 + element2))

    # Annealing calibration function for Call options using Heston
    def calibratorHestonSA(self, real_market_price, s0, strike, r, q, T, lowerBounds=[1e-2, 1e-2, 1e-2, 1e-2, -1],
                           upperBounds=[10, 10, 10, 10, 1]):
        # Note the difference in the objective function (sum of squares vs vector of errors)
        objectiveFunctionHeston = lambda paramVect: np.sum(np.square((real_market_price -
                                                                      self.priceHestonMid(s0, strike, r, q, T,
                                                                                          paramVect[0], paramVect[1],
                                                                                          paramVect[2], paramVect[3],
                                                                                          paramVect[4]))
                                                                     / real_market_price))
        # Define the upper and lower bounds
        bounds = list(zip(lowerBounds, upperBounds))

        # Minimize the function
        calibrated_parameters = dual_annealing(objectiveFunctionHeston, bounds=bounds)

        return calibrated_parameters


