import numpy as np

from agent import Agent
from state import State
from utils import add_noise, calc_loss_GDP


class Nation(Agent):
    def __init__(
        self,
        config_par,
        contact_matrix,
        cont_param,
        population,
        C,
        name,
        state,
        parameters,
    ):

        Agent.__init__(self, config_par=config_par, name=name)

        self.contact_matrix = contact_matrix
        self.cont_param = cont_param
        self.population = population
        self.C = C
        self.state = State(population, **state)
        self.parameters = parameters
        self.alpha = config_par["alpha"]
        self._history = [self.state.to_array, self.state.to_array]

    def __repr__(self):

        return "\nNation %s :\n\t Contact matrix:\n\t %s \n\n\t %s,\n\t " % (
            self.name,
            self.contact_matrix,
            self.state,
        )

    def state_to_array(self, state):
        return state.to_array

    def update_C(self, C):

        self.C = C

        return self

    def immigrate(self, mig_agent, value):
        # TODO make sure that this method and related methods get called

        calc_new_seir = (
            (mig_agent.state.SEAIRDV * value) + (self.state.SEAIRDV * self.state.N)
        ) / (value + self.state.N)

        new_state = State(value + self.state.N, *calc_new_seir)

        return new_state

    def emigrate(self, value):

        new_state = State(self.state.set_value("-", value), *self.state.SEAIRDV)

        self.replace_state(new_state)

        return self

    # Interaction between agents ivolves migration of population from one agent to other(s)
    def interact(self, conn_agents, value):

        if type(value) is float:  # if migration is fixed to a certain value

            previous_N = self.state.N

            # calculating the percentage of migration population scaled by the containment policy value
            # NOTE here we use alpha and not alpha*compliance because here compliance does not matter as full lockdown can be enforced
            migration = (1 - self.alpha) * (self.state.N * value)

            # add noise to not have constatnt migrations (unrealistic)
            migration_noise = add_noise(migration, 0.2)

            # set new state
            self.emigrate(migration_noise)

            for agent in conn_agents:

                # add noise to single self to agent migration
                noise = add_noise(migration_noise / len(conn_agents), 0.1)

                # calculate new SEAIRDV value after immigration
                new_state_agent = agent.immigrate(self, noise)

                # set new state
                agent.replace_state(new_state_agent)

            return self, conn_agents

        else:  # if the migration data is not fixed (aviation data)

            for agent in conn_agents:

                if np.isclose(value[agent.name].get("departures"), 0):

                    continue

                # Calculate percentage of population travelling out the country every day
                pop_perc = (
                    value[agent.name].get("departures") / 365
                ) / self.state.N.sum()

                # Calcuate number from percantage and scale by the containment policy value
                # NOTE here we use alpha and not alpha*compliance because here compliance does not matter as full lockdown can be enforced
                migration = (1 - self.alpha) * (self.state.N * pop_perc)

                # Add noise
                migration_noise = add_noise(migration, 0.2)

                # Set new state
                self.emigrate(migration_noise)

                # Calculate new SEAIRDV values for state receiving population
                new_state_agent = agent.immigrate(self, migration_noise)

                # Set new state (SEAIRDV receiving state)
                agent.replace_state(new_state_agent)

            return self, conn_agents

    def next_state(self, t):
        """
        b= rate of transmission
        n= natural death rate
        alpha / c(t)= containment policy
        s= measuring effect of isolation policy
        g=infected/aymptomatic recovery rate
        d=infected die rate
        e=
        k=
        w_a, w_i= environment contamination
        f = lost immunity ratio
        rho= removal environment contamination

        next_S = S - (b * S * c) * (s * I + E + A) - (n * S) + (n * (1 - D))  # Add fraction of recovered compartment.
        next_E = E + (b * c * S) * (s * I + E + A) - (k + n)*E
        next_A = A + (1 - e) * k * E - (g + n) * A
        next_I = I + (e * k * E) - (g + d + n) * I
        next_R = R + (g * (A + I)) - (n * R)
        next_D = D + d * I  # Remove fraction of recovered compartment.
        next_V = w_a*A+w_i*I
        """

        # Extract components of current state
        N, S, E, A, I, R, D, V, loss = self.state.to_array

        # Get total and environment contact matrices (with alpha/lockdown strength already incorporated)
        C, C_v, inv_p = self.C

        # Get parameters of model
        b, n, c, s, g, d, e, k, w_a, w_i, f, rho = [*self.parameters.values()]
        b = np.array(b)

        # Make b one dimensional if there are no age groups
        if C.shape != (3, 3):
            b = b.sum()

        # Update Susceptible

        # people moving from Susceptible to Exposed
        S_to_E = b * S * (C_v @ V + C @ ((A + I) / N))

        R_to_S = f * R

        next_S = (
            S
            + n * (1 - D)  # replenish the natural deaths in S, E, A, I, and R
            + R_to_S  # people moving from Recovered to Susceptible
            - S_to_E  # people moving from Susceptible to Exposed
            - n * S  # natural deaths
        )

        # Update Exposed

        E_to_AI = k * E  # people moving from E to either A or I

        next_E = (
            E
            + S_to_E  # people moving from Susceptible to Exposed
            - E_to_AI  # people moving from E to either A or I
            - n * E  # natural deaths
        )

        # Update Asymptomatic

        A_to_R = g * A  # people moving from Asymptomatic to Recovered

        next_A = (
            A
            + (1 - e) * E_to_AI  # people moving from Exposed to Asymptomatic
            - A_to_R  # people moving from Asymptomatic to Recovered
            - n * A  # natural deaths
        )

        # Update Infected

        I_to_R = g * I  # people moving from Infected to Recovered
        I_to_D = d * I  # people moving from Infected to Dead

        next_I = (
            I
            + e * E_to_AI  # people moving from Exposed to Infected
            - I_to_R  # people moving from infected to Recovered
            - I_to_D  # people moving from Infected to Dead
            - n * I  # natural deaths
        )

        # Update Recovered

        next_R = (
            R
            + A_to_R  # people moving from Asymptomatic to Recovered
            + I_to_R  # people moving from Infected to Recovered
            - R_to_S  # people moving from Recovered to Susceptible
            - n * R  # natural deaths
        )

        # Update Deaths

        next_D = D + I_to_D  # people moving from Infected to Dead

        # Update Environment

        next_V = (
            V
            + (w_a * inv_p * A)  # environment contaminants from Asymptomatic
            + (w_i * inv_p * I)  # environment contaminants from Infected
            - rho * V  # normal rate of environment decontamination
        )

        # TODO check calc loss
        next_loss = loss + calc_loss_GDP(self, t)

        return State(
            N, next_S, next_E, next_A, next_I, next_R, next_D, next_V, next_loss
        )

    def policy(self):
        return self.alpha
