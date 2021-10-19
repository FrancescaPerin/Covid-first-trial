from collections import namedtuple

 State= namedtuple("State", ["S", "E", "I", "R", "N"])
 State.__eq__ = lambda x, y: x.S == y.S and x.E == y.E and x.I == y.I and x.R == y.R

Parameters = namedtuple("Parameters", ["a", "b", "d", "g", "r"])


def iterate_state(state, params):
    """
    Performs one iteration using the state-params combination.
    :return: State namedtuple using
    """

    S, E, I, R, N = state
    a, b, g, d, r = params

    next_S = S - (r * b * S * I) + (d * R)  # Add fraction of recovered compartment.
    next_E = E + (r * b * S * I - a * E)
    next_I = I + (a * E - g * I)
    next_R = R + (g * I) - (d * R)  # Remove fraction of recovered compartment.

    return State(next_S, next_E, next_I, next_R, N)