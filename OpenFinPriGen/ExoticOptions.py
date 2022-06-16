import numpy as np
import pandas as pd
from scipy.stats import stats

from OpenFinPriGen.VanillaProducts import VanillaProducts


class ExoticOptions(VanillaProducts):

    def __init__(self, s: pd.DataFrame, df_options: pd.DataFrame, style: str, k: float, maturity: int,
                 trajectories: int, exotic_style: str,
                 barrier: float, mean_style: str = "arithmetic", rf: float = 0, q: float = 0):
        """
            @param exotic_style: style of the exotic option ("none", not an exotic option; "a", asian option; "do",
                                 down-and-out option; "di", down-and-in option; "uo", up-and-out option;
                                  "ui", up-and-in option)
            @param barrier: value of the barrier for barrier options
            @param mean_style: type of mean considered for asian options ("arithmetic" or "geometric")
        """

        VanillaProducts.__init__(self, s, df_options, style, k, maturity, trajectories, rf, q)
        self.exotic_style = exotic_style
        self.barrier = barrier
        self.mean_style = mean_style

    def payoff_exotic(self):
        tab = np.zeros(shape=(self.trajectories, self.maturity))
        df_exotic = pd.DataFrame(tab)

        if self.exotic_style == "none":
            self.df_options = df_exotic
            self.payoff()

        elif self.exotic_style == "a" and self.mean_style == "arithmetic":
            for i in range(self.trajectories):
                A_T = np.mean(self.s.iloc[i])
                df_exotic.iat[i, self.maturity - 1] = A_T
            self.df_options = df_exotic
            return self.payoff()

        elif self.exotic_style == "a" and self.mean_style == "geometric":
            for i in range(self.trajectories):
                A_T = 1
                for j in range(self.maturity):
                    A_T = A_T * self.s.iat[i, j]
                df_exotic.iat[i, self.maturity - 1] = A_T ^ (1 / self.maturity)
            self.df_options = df_exotic
            return self.payoff()

        elif self.exotic_style == "do":
            for i in range(self.trajectories):
                if np.min(self.s.iloc[i]) > self.barrier:
                    df_exotic.iat[i, self.maturity - 1] = self.s.iat[i, self.maturity - 1]
                else:
                    df_exotic.iat[i, self.maturity - 1] = 0
            self.df_options = df_exotic
            return self.payoff()

        elif self.exotic_style == "di":
            for i in range(self.trajectories):
                if np.min(self.s.iloc[i]) <= self.barrier:
                    df_exotic.iat[i, self.maturity - 1] = self.s.iat[i, self.maturity - 1]
                else:
                    df_exotic.iat[i, self.maturity - 1] = 0
            self.df_options = df_exotic
            return self.payoff()

        elif self.exotic_style == "uo":
            for i in range(self.trajectories):
                if np.max(self.s.iloc[i]) < self.barrier:
                    df_exotic.iat[i, self.maturity - 1] = self.s.iat[i, self.maturity - 1]
                else:
                    df_exotic.iat[i, self.maturity - 1] = 0
            self.df_options = df_exotic
            return self.payoff()

        elif self.exotic_style == "ui":
            for i in range(self.trajectories):
                if np.max(self.s.iloc[i]) >= self.barrier:
                    df_exotic.iat[i, self.maturity - 1] = self.s.iat[i, self.maturity - 1]
                else:
                    df_exotic.iat[i, self.maturity - 1] = 0
            self.df_options = df_exotic
            return self.payoff()

        else:
            raise Exception("Combination (position, style) not existing. Check your input.")
