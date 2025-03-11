import math
from abc import ABC


class Probability(ABC):
    def __init__(self, *args):
        if len(args) == 1:
            assert isinstance(args[0], Probability)
            prob = args[0]
            self.count = prob.count
            self.total = prob.total
        elif len(args) == 2:
            count, total = args
            assert isinstance(count, int) and isinstance(total, int)
            if not (0 <= count <= total):
                raise ValueError("Count must be between 0 and total.")
            self.count = count
            self.total = total
        else:
            raise ValueError("Invalid number of arguments.")

    @property
    def value(self):
        return self.count

    def __add__(self, other):
        if not isinstance(other, Probability):
            return NotImplemented
        return self.__class__(self.count + other.count, max(self.total, other.total))

    def __sub__(self, other):
        if not isinstance(other, Probability):
            return NotImplemented
        return self.__class__(max(self.count - other.count, 0), max(self.total, other.total))

    def __mul__(self, other):
        if not isinstance(other, Probability):
            return NotImplemented
        return self.__class__(max(self.count * other.count, 0), self.total * other.total)

    def __truediv__(self, other):
        if not isinstance(other, Probability):
            return NotImplemented
        if other.count == 0 or other.total == 0:
            return zeroProbability
        return self.__class__(int(max(self.count / other.count, 0)), int(self.total / other.total))

    def __repr__(self):
        return f"{self.value:.2f}"


class AbsoluteProbability(Probability):
    pass


class RelativeProbability(Probability):
    @property
    def value(self):
        return self.count / self.total if self.total > 0 else 0.0


class RelativeProbabilityPerMillion(RelativeProbability):
    @property
    def value(self):
        if self.total == 0:
            return math.inf
        return super().value * 1_000_000


class LogarithmicProbability(Probability):
    @property
    def value(self):
        return math.log(self.count / self.total) if self.count > 0 and self.total > 0 else float('-inf')


zeroProbability = AbsoluteProbability(0, 0)


def ratio(freqs, cmp_freqs):
    return {key: (freq / cmp_freqs.get(key, zeroProbability)) for key, freq in freqs.items()}
