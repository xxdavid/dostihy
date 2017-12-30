#!/usr/bin/env python3
import matplotlib.pyplot as plt
import numpy as np
from abc import ABC, abstractmethod
import re


class Plotter(ABC):
    """
    An abstract plotter that draws a chart.
    It loads the data (if it wasn't done before) and stores them in static variables.

    Each plotter creates one charts.
    Charts are saved in the 'charts' directory in png, svg and pdf format.
    """

    ranks = None
    combinations = None
    set_length = None
    games_of_one_player = None

    def __init__(self):
        if Plotter.ranks is not None:
            return

        with open("../stats.txt") as f:
            lines = f.readlines()

        lines = [x.strip() for x in lines]

        Plotter.combinations = int(lines.pop(0))
        Plotter.set_length = int(lines.pop(0))
        Plotter.games_of_one_player = int(lines.pop(0))
        lines.pop(0)  # blank newline

        ranks = []

        for line in lines:
            line_parts = line.split(" ")
            ranks.append((line_parts[0], int(line_parts[1]), int(line_parts[2])))

        Plotter.ranks = ranks

    @property
    def total_games(self):
        return Plotter.combinations * Plotter.set_length

    @property
    @abstractmethod
    def x_label(self):
        pass

    @property
    @abstractmethod
    def y_label(self):
        pass

    @property
    @abstractmethod
    def title(self):
        pass

    @property
    @abstractmethod
    def name(self):
        pass

    @abstractmethod
    def init_plot(self):
        pass

    def plot(self):
        self.init_plot()

        plt.xlabel(self.x_label)
        plt.ylabel(self.y_label)
        plt.title(self.title)

        plt.tight_layout()

        plt.savefig(f"../charts/{self.name}.png")
        plt.savefig(f"../charts/{self.name}.svg")
        plt.savefig(f"../charts/{self.name}.pdf")
        plt.clf()


class BarPlotter(Plotter):
    @abstractmethod
    def compute_values(self):
        """
        Compute the values for the chart.
        :return: list of tuples in (x, y) format
        """
        pass

    def init_plot(self):
        values = self.compute_values()

        [x, y] = list(zip(*values))

        ind = np.arange(len(x))
        width = .8
        plt.bar(ind, y, width=width)
        plt.xticks(ind - width / 2, x, rotation=70)
        plt.tick_params(bottom='off')


class LinePlotter(Plotter):
    @abstractmethod
    def compute_values(self):
        """
        Compute the values for the chart.
        :return: list of tuples in (x, y) format
        """
        pass

    def init_plot(self):
        values = self.compute_values()

        [x, y] = list(zip(*values))

        ind = np.arange(len(x))
        plt.plot(ind, y)
        plt.xticks(ind, x)


class WinsPlotter(BarPlotter):
    @property
    def name(self):
        return "wins"

    @property
    def title(self):
        return f"Ranks in a tournament of {self.total_games} games" \
               f" ({Plotter.combinations} combinations)"

    @property
    def x_label(self):
        return "Strategies"

    @property
    def y_label(self):
        return "Won games [%]"

    def compute_values(self):
        ranks = list(map(lambda x: (x[0], 100 * x[1] / x[2]), Plotter.ranks))
        ranks.sort(key=lambda x: x[1], reverse=True)
        return ranks


class TiesPlotter(BarPlotter):
    @property
    def name(self):
        return "ties"

    @property
    def title(self):
        return f"Tied games ({self.total_games} games in total)"

    @property
    def x_label(self):
        return "Strategies"

    @property
    def y_label(self):
        return "Ties [%]"

    def compute_values(self):
        ranks = list(map(lambda x: (x[0], (100 *
                                           (Plotter.games_of_one_player - x[2])
                                           / Plotter.games_of_one_player)),
                         Plotter.ranks))
        ranks.sort(key=lambda x: x[1], reverse=True)
        return ranks


class ThresholdPlotter(LinePlotter):
    @property
    def name(self):
        return "threshold"

    @property
    def title(self):
        return f"Ranks of Threshold strategies ({self.total_games} games)"

    @property
    def x_label(self):
        return "Threshold"

    @property
    def y_label(self):
        return "Won games [%]"

    def compute_values(self):
        ranks = list(map(
            lambda x: (int(re.search("\d+", x[0]).group()), 100 * x[1] / x[2]),
            filter(lambda x: x[0].startswith('Threshold'), Plotter.ranks)
        ))

        ranks.sort(key=lambda x: x[0])
        return ranks


WinsPlotter().plot()
TiesPlotter().plot()
ThresholdPlotter().plot()
