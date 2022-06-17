import numpy as np
import pandas as pd
from scipy.stats import stats

from OpenFinPriGen.VanillaProducts import VanillaProducts
from OpenFinPriGen.BlackScholesGen import BlackScholesGen


class ExoticOptions(VanillaProducts):

    def __init__(self, s0: float, k: float, sigma: float, maturity: int,
                 trajectories: int, exotic_style: str, dt: float,
                 barrier: float, vanilla_style: str, underlying_style: str, mean_style: str = "arithmetic",
                 rf: float = 0, q: float = 0):
        """
            @param s0: stock price at time zero
            @param k: Strike price of your option.
            @param sigma: value of the volatility considered
            @param maturity: Time until the end of life of the option.
            @param trajectories: Number of trajectories eq. number of rows in the dataframe
            @param exotic_style: style of the exotic option ("none", not an exotic option; "a", asian option; "do",
                                 down-and-out option; "di", down-and-in option; "uo", up-and-out option;
                                  "ui", up-and-in option)
            @param barrier: value of the barrier for barrier options
            @param vanilla_style: call ("c") or put ("p").
            @param mean_style: type of mean considered for asian options ("arithmetic" or "geometric")
            @param rf: Risk free rate to apply for the calculations.default=0.
            @param q: Dividend yield (if existing). Default=0.
        """

        self.s0 = s0
        self.k = k
        self.sigma = sigma
        self.maturity = maturity
        self.trajectories = trajectories
        self.exotic_style = exotic_style
        self.dt = dt
        self.barrier = barrier
        self.vanilla_style = vanilla_style
        self.underlying_style = underlying_style
        self.mean_style = mean_style
        self.rf = rf
        self.q = q

    def PayoffExotic(self):
        tab = np.zeros(shape=(self.trajectories, self.maturity))
        df_exotic = pd.DataFrame(tab)

        if self.underlying_style == "bsm":
            my_bsm = BlackScholesGen(self.trajectories, self.maturity, self.rf, self.q, self.s0, self.sigma, self.dt)
            df_underlying = my_bsm.PathGenerate()
            self.s = df_underlying

        if self.exotic_style == "none":
            for i in range(self.trajectories):
                df_exotic.iat[i, self.maturity - 1] = self.s.iat[i, self.maturity - 1]
            self.df_options = df_exotic
            return self.Payoff()

        elif self.exotic_style == "a" and self.mean_style == "arithmetic":
            for i in range(self.trajectories):
                A_T = np.mean(self.s.iloc[i])
                df_exotic.iat[i, self.maturity - 1] = A_T
            self.df_options = df_exotic
            return self.Payoff()

        elif self.exotic_style == "a" and self.mean_style == "geometric":
            for i in range(self.trajectories):
                A_T = 1
                for j in range(self.maturity):
                    A_T = A_T * self.s.iat[i, j]
                df_exotic.iat[i, self.maturity - 1] = A_T ^ (1 / self.maturity)
            self.df_options = df_exotic
            return self.Payoff()

        elif self.exotic_style == "do":
            for i in range(self.trajectories):
                if np.min(self.s.iloc[i]) > self.barrier:
                    df_exotic.iat[i, self.maturity - 1] = self.s.iat[i, self.maturity - 1]
                else:
                    df_exotic.iat[i, self.maturity - 1] = 0
            self.df_options = df_exotic
            return self.Payoff()

        elif self.exotic_style == "di":
            for i in range(self.trajectories):
                if np.min(self.s.iloc[i]) <= self.barrier:
                    df_exotic.iat[i, self.maturity - 1] = self.s.iat[i, self.maturity - 1]
                else:
                    df_exotic.iat[i, self.maturity - 1] = 0
            self.df_options = df_exotic
            return self.Payoff()

        elif self.exotic_style == "uo":
            for i in range(self.trajectories):
                if np.max(self.s.iloc[i]) < self.barrier:
                    df_exotic.iat[i, self.maturity - 1] = self.s.iat[i, self.maturity - 1]
                else:
                    df_exotic.iat[i, self.maturity - 1] = 0
            self.df_options = df_exotic
            return self.Payoff()

        elif self.exotic_style == "ui":
            for i in range(self.trajectories):
                if np.max(self.s.iloc[i]) >= self.barrier:
                    df_exotic.iat[i, self.maturity - 1] = self.s.iat[i, self.maturity - 1]
                else:
                    df_exotic.iat[i, self.maturity - 1] = 0
            self.df_options = df_exotic
            return self.Payoff()

        else:
            raise Exception("Combination (position, style) not existing. Check your input.")
