import numpy as np

from state import State
from agent import Agent
from utils import calc_loss_GDP, add_noise


class Nation(Agent):

    # Interaction between agents ivolves migration of population from one agent to other(s)
    def interact(self, conn_agents, value):

        if type(value) is float: #if migration is fixed to a certain value

            previous_N = self.state.N


            # calculating the percentage of migration population scaled by the containment policy value
            migration = self.alpha * (self.state.N * value) # TODO: double check if alpha or 1-alpha

            # add noise to not have constatnt migrations (unrealistic)
            migration_noise = add_noise(migration, 0.2)

            # set new state
            self.emigrate(migration_noise)

            for agent in conn_agents:

                #add noise to single self to agent migration
                noise=add_noise(migration_noise / len(conn_agents), 0.1)
                
                #calculate new SEAIRDV value after immigration
                new_state_agent = agent.immigrate(self, noise)
                
                #set new state
                agent.replace_state(new_state_agent)

            return self, conn_agents

        
        else: #if the migration data is not fixed (aviation data)

            for agent in conn_agents:

                # Calculate percentage of population travelling out the country every day
                pop_perc = int(value[agent.name].get("departures") / 365) / self.state.N.sum()

                # Calcuate number from percantage and scale by the containment policy value
                migration = self.alpha * (self.state.N * pop_perc)

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
        w_a, w_m= environment contamination
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

        N, S, E, A, I, R, D, V, loss = self.state.to_array

        p = self.cont_param

        b, n, c, s, g, d, e, k, w_a, w_i, f, rho = [*self.parameters.values()]

        if self.C.shape != (3, 3):

            p = p[
                1
            ]  # select p value of adult since without age groups all populations will be considered adult of working age

            next_S = (
                S
                - sum(b) * S * (self.C * V + self.C * (A + I))
                - n * S
                - n * (1 - D)
                + f * R
            )

            next_E = E + sum(b) * S * (self.C * V + self.C * (A + I)) - (k + n) * E

        else:

            next_S = (
                S
                - b * S * (self.C @ V + self.C @ ((A + I) / N.sum()))
                - n * S
                - n * (1 - D)
                + f * R
            )

            next_E = (
                E + b * S * (self.C @ V + self.C @ ((A + I) / N.sum())) - (k + n) * E
            )

        next_A = A + (1 - e) * k * E - (g + n) * A

        next_I = I + (e * k * E) - (g + d + n) * I

        next_R = R + (g * (A + I)) - (n * R) - f * R

        next_D = D + d * I

        next_V = (w_a * (1 - p) * A) + (w_i * (1 - p) * I) - rho * V

        next_loss = loss + calc_loss_GDP(self, t)

        return State(
            N, next_S, next_E, next_A, next_I, next_R, next_D, next_V, next_loss
        )

    def policy(self):
        return self.alpha
