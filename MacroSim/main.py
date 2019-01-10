import GUI
import economy

import wx
import threading
import random
import numpy as np
import time


class Simulation(threading.Thread):
    def __init__(self):
        self.simulation_on = False
        self.simulation_speed = 1  # Number of iterations before graphs get updated
        self.timer = 0  # Used to keep track of the time it takes to run a period (for debugging)
        self.period = 0  # Variable for the current time period of the simulation
        self.months_per_period = 1  # Number of months the simulation will advance per period
        self.retirement_age = 65  # Age at which a worker retires
        self.age_to_die = 80  # Age at which a worker gets deleted and replaced with a new worker
        # Lists of the graph labels
        self.macro_labels = ['GDP', 'Consumption', 'Investment', 'Unemployment', 'Population']
        self.good_labels = ['Price', 'Quantity']
        # The following are variables used to store economic variables so that they can be graphed
        self.x = []
        self.y_macro = [[[], []] for i in range(len(self.macro_labels))]
        self.y_price = [[[], []] for i in range(economy.NUMBER_OF_GOODS)]
        self.y_quantity = [[[], []] for i in range(economy.NUMBER_OF_GOODS)]

        self.store_graph_variables()
        self.display_graphs()

    def main_loop(self):
        # Main loop of the program. One iteration of this loop will update one period in each economy
        while self.simulation_on:
            self.period += 1  # Incrementing the period
            # Print out the period in the console for debugging
            print("----------------------------------------"
                  "Period {} - Time: {}"
                  "----------------------------------------"
                  .format(self.period, format(time.time() - self.timer, '.6f') if self.period != 1 else 0))
            self.timer = time.time()

            # Loops over the two economies and updates each one independently
            for econ in economies:

                # 1: Demand side ---------------------------------------------------------------------------------------

                econ.price_vector = [market.get_price() for market in econ.markets]  # Updating price vector
                for worker in econ.workers:
                    worker.age += self.months_per_period / 12  # Each worker ages a few months
                    if worker.age >= self.age_to_die:
                        worker.kill(worker.b)  # Worker dies; passes through the old utility function parameters to the new worker
                    else:
                        # If the worker stays alive, then update his/her individual demand for consumption goods
                        indiv_good_demand = worker.get_good_demand(econ.price_vector)
                        # And aggregate demand for each good is the sum over all workers' demand
                        for i, market in enumerate(econ.markets):
                            market.quantity_demanded += indiv_good_demand[i]

                """
                Replaced by manual utility-maximization solution
                
                # Update demand for consumption goods using last period's output and prices
                for i, quantity in enumerate(econ.util_max_solution().x):
                    econ.markets[i].quantity_demanded = quantity
                """

                # 2: Getting optimal allocation of L, K ----------------------------------------------------------------

                # Currently unfinished. Missing a mechanism in which firms target optimal values of labour and capital
                for market in econ.markets:
                    for firm in market.firms:
                        L, K = firm.cost_min_solution(econ.interest_rate).x
                        firm.target_L = L
                        firm.target_K = K
                        print(str(firm.target_L) + " - " + str(firm.labour))

                # 3: Labour market -------------------------------------------------------------------------------------

                # Re-calculating the number of aggregate vacancies which is used in the matching function
                econ.vacancies = 0
                for market in econ.markets:
                    for firm in market.firms:
                        econ.vacancies += firm.get_vacancies()

                # Matching mechanism: Number of matches in the economy is determined by matching function
                # Unemployed workers are selected at random to be employed by the highest paying firm
                for i in range(econ.get_matches()):
                    match = econ.unemployed_list[random.randint(0, len(econ.unemployed_list) - 1)]
                    econ.worker_match(match)

                # 4: updating variable quantities ----------------------------------------------------------------------

                # Calculating quantity supplied and equilibrium quantity in the market
                for market in econ.markets:
                    market.quantity_supplied = 0
                    for firm in market.firms:
                        market.quantity_supplied += firm.get_output()
                    market.quantity_sold = min(market.quantity_supplied, market.quantity_demanded)
                    # Getting the total income payments being made to labour and capital in each firm
                    for firm in market.firms:
                        firm.update_income_payments()

                # Resetting aggregate variables in order to re-sum them
                econ.gdp = 0
                econ.consumption = 0
                econ.investment = 0
                # re-summing aggregate quantities (gdp, consumption, investment)
                for worker in econ.workers:
                    worker.update_income()
                    econ.consumption += worker.consumption
                    econ.investment += worker.investment
                econ.gdp = econ.consumption + econ.investment

            # Updating graphs
            self.store_graph_variables()
            if self.period % self.simulation_speed == 0:
                self.display_graphs()

    def store_graph_variables(self):
        # Storing initial values of every variable that needs to be graphed
        self.x.append(self.period)
        for econ in economies:
            self.y_macro[0][econ.id].append(econ.gdp)
            self.y_macro[1][econ.id].append(econ.consumption)
            self.y_macro[2][econ.id].append(econ.investment)
            self.y_macro[3][econ.id].append(len(econ.unemployed_list) / len(econ.workers))
            self.y_macro[4][econ.id].append(len(econ.workers))
            for i in range(economy.NUMBER_OF_GOODS):
                self.y_price[i][econ.id].append(econ.markets[i].price)
                self.y_quantity[i][econ.id].append(econ.markets[i].quantity_sold)

    def display_graphs(self):
        # Re-draws the graphs on the GUI for both economies
        # to do: Clean this part up, it's messy
        if frame.tool_bar.graph_type == 0:
            for i, graph in enumerate(frame.two_graph_panel.graphs):
                graph.draw(self.macro_labels[frame.tool_bar.graph_number],
                           self.x, self.y_macro[frame.tool_bar.graph_number][i])
        elif frame.tool_bar.graph_type == 1:
            for i, graph in enumerate(frame.two_graph_panel.graphs):
                y = []
                for j in range(economy.NUMBER_OF_GOODS):
                    if frame.tool_bar.graph_number == 0:
                        y.append(self.y_price[j][i])
                    elif frame.tool_bar.graph_number == 1:
                        y.append(self.y_quantity[j][i])
                graph.draw(self.good_labels[frame.tool_bar.graph_number], self.x, y)


def create_main_frame(pop, number_of_goods, number_of_firms):
    # Initializes both economies and created the main GUI frame
    global frame
    global economies
    global simulation
    frame = GUI.MainFrame(None, number_of_goods)
    frame.Show()
    utility_func_parameters = [[] for i in range(pop)]
    productivity_parameters = [float(-1) for i in range(pop)]
    for i in range(pop):
        utility_func_parameters[i] = [random.uniform(0.1, 0.9) for i in range(number_of_goods)]
        while productivity_parameters[i] < 0:
            productivity_parameters[i] = np.random.normal(1, 0.5)
    ages = [round(random.uniform(0, 80), 1) for i in range(pop)]
    economies = [economy.MacroEconomy(0, pop, number_of_goods, number_of_firms, utility_func_parameters,
                                      productivity_parameters, ages),
                 economy.MacroEconomy(1, pop, number_of_goods, number_of_firms, utility_func_parameters,
                                      productivity_parameters, ages)]
    simulation = Simulation()


"""
def get_config():
    return [
        [simulation.simulation_speed, simulation.months_per_period],
        [[econ.minimum_wage for econ in economies]]
    ]

def save_config():
    pass
"""

if __name__ == '__main__':
    app = wx.App()
    settings_frame = GUI.SettingsFrame(None)
    settings_frame.Show()
    app.MainLoop()
