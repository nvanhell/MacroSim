import numpy as np
from scipy.optimize import minimize
import random


# Number of consumption goods in the economy
# Note: Setting this too high drastically increases the time it takes to optimize a consumer's utility function
# Recommended to keep below ~20 goods
NUMBER_OF_GOODS = 5


class MacroEconomy:
    def __init__(self, id, pop, number_of_goods, number_of_firms, util_func_params,
                 productivity_parameters, ages):
        global NUMBER_OF_GOODS
        NUMBER_OF_GOODS = number_of_goods
        self.id = id  # identification number, mostly used for debugging
        # Any economic variables in this class represent aggregates
        self.gdp = 0  # Nominal GDP
        self.consumption = 0  # Nominal consumption
        self.investment = 0  # Nominal investment
        self.interest_rate = 0  # Savings rate

        self.government = Government()

        # Every good is supplied/demanded in a market, and markets are kept track using this array
        self.markets = np.array([Market(self, number_of_firms) for i in range(NUMBER_OF_GOODS)])
        self.max_firms_in_market = number_of_firms
        self.price_vector = [market.price for market in self.markets]

        # Array to keep track of every worker
        self.workers = [Worker(self, productivity_parameters[i], ages[i], number_of_firms, util_func_params[i]) for i in range(pop)]
        for worker in self.workers:
            for i, market in enumerate(self.markets):
                for j, firm in enumerate(market.firms):
                    worker.stocks_owned[i][j] = firm.NUMBER_OF_SHARES / len(self.workers)
        # Array to keep track of every unemployed worker
        # (where each element is a reference to an unmployed worker object)
        self.unemployed_list = [worker for worker in self.workers]
        self.income_list = []

        self.vacancies = 0  # Number of aggregate vacancies
        self.matching_efficiency = 0.05  # Matching efficiency in the labour market

        #self.b = np.array(utility_func_parameters)  # Parameters used in the consumer utility function

        # Randomly assigning jobs to unemployed workers
        for worker in range(int((len(self.workers) * 0.5))):
            match = self.unemployed_list[random.randint(0, len(self.unemployed_list) - 1)]
            self.worker_match(match)

    def create_worker(self, util_func_params):
        new_worker = Worker(self, np.random.normal(1, 0.5), 0, self.max_firms_in_market, util_func_params)
        self.workers.append(new_worker)
        self.unemployed_list.append(new_worker)

    """
    Replaced by manual utility-maximization solution

    # Methods below are for utility maximization
    def utility_function(self, x, sign):
        # Aggregate Cobb-Douglas utility function
        u = sign * 1
        for i in range(NUMBER_OF_GOODS):
            u *= (x[i])**(self.b[i])
        return u

    def utility_function_derivatives(self, x, sign):
        # Returns an array of first partial derivatives of u with respect to each good [du/dx0, du/dx1, ...]
        du_dx = np.array([float(sign) for i in range(NUMBER_OF_GOODS)])
        for i in range(NUMBER_OF_GOODS):
            for j in range(NUMBER_OF_GOODS):
                du_dx[i] *= self.b[j] * (x[j]) ** (self.b[j] - 1) if i == j else (x[j]) ** self.b[j]
        return du_dx

    def get_budget_constraint(self, x):
        # Returns value of the aggregate budget constraint I - p0x0 - p1x1 - ... - pnxn
        constraint = self.consumption
        for i in range(NUMBER_OF_GOODS):
            constraint -= self.markets[i].price * (1 + self.government.get_good_tax(i)) * x[i]
        return constraint

    def util_max_solution(self):
        # Maximizes the utility function subject to an income constraint
        # Returns an array of the quantities demanded for each good
        self.cons = (
            {
                'type': 'eq',
                'fun': lambda x: np.array([self.get_budget_constraint( [x[i] for i in range(NUMBER_OF_GOODS)] )]),
                'jac': lambda x: np.array([-self.markets[i].price * (1 + self.government.get_good_tax(i))
                                           for i in range(NUMBER_OF_GOODS)])
            }
        )
        return minimize(self.utility_function, [1 for i in range(NUMBER_OF_GOODS)], args=-1,
                        jac=self.utility_function_derivatives,
                        constraints=self.cons, method='SLSQP', options={'disp': False})
    """

    def get_matches(self):
        # Returns the number of aggregate matches in the economy
        if self.vacancies > 0 and len(self.unemployed_list) > 0:
            return int(self.matching_efficiency * self.vacancies**0.5 * (len(self.unemployed_list))**0.5)
        else:
            return 0

    def worker_match(self, match):
        # Provides a simple matching mechanism in which the matched worker accepts the highest paying job offer
        match.wage = -1
        # Start by looking for the highest paying firm
        for market in self.markets:
            for firm in market.firms:
                firm.wage = firm.get_wage()
                if firm.get_vacancies() > 0:
                    if firm.wage >= match.wage:
                        match.wage = firm.wage
                        match.employer = firm
        # Once the highest paying firm is found, then update the relevant variables
        if match.employer is not None:
            match.employer.labour += match.get_productivity()
            match.employer.employee_list.append(match)
            match.employer.vacancies -= 1
            self.vacancies -= 1
            self.unemployed_list.remove(match)


class Government:
    def __init__(self):
        self.collected_taxes = 0  # Numerical quantity of taxes collected
        self.income_tax = 0  # Tax rate on all income
        self.consumption_tax = 0  # Tax rate on all consumption goods
        self.goods_tax = [0 for i in range(NUMBER_OF_GOODS)]  # Tax rate on a particular consumption good

    def get_good_tax(self, i):
        # Returns total tax rate on a particular good
        return self.consumption_tax + self.goods_tax[i]


class Market:
    def __init__(self, econ, number_of_firms):
        self.econ = econ
        self.price = 1  # Single market price for a consumption good
        self.quantity_demanded = 1  # Aggregate quantity demanded for the good
        self.quantity_supplied = 1  # Aggregate quantity supplied for the good
        self.quantity_sold = 1  # Actual output sold (taking the lower quantity between Qs and Qd)
        self.firms = np.array([Firm(self, 10) for i in range(number_of_firms)])  # Array of firms operating in the market

    def get_price(self):
        # TO DO
        # (Temporarily disabled price mechanism)
        return 1


class Firm:
    def __init__(self, market, tfp):
        self.market = market  # Reference to the market in which the firm belongs
        self.money = 1000000
        self.tfp = tfp
        self.labour = 0  # Quantity of homogeneous labour employed by the firm
        self.capital = 1  # Quantity of capital operated by the firm
        self.target_L = 0  # L and K targets minimize the firm's costs
        self.target_K = 0
        self.wage = 0  # Wage rate paid to all employees
        self.employee_list = []  # List of every employee reference employed by the firm
        self.vacancies = 0  # Number of vacancies by the firm
        self.a = [2/3, 1/3]  # Parameters on L and K in the Cobb-Douglas function

        self.NUMBER_OF_SHARES = 1000000  # Each firm has 1 million shares
        self.labour_income = 0
        self.capital_income = 0

    def __str__(self):
        return ("L: " + str(round(self.labour, 2)) + " - K: " + str(round(self.capital, 2)) +
                " - q: " + str(round(self.get_output(), 2)))

    def get_wage(self):
        if self.labour > 0:
            return self.market.price * self.tfp * self.a[0] * self.labour**(self.a[0] - 1) * self.capital**self.a[1]
        else:
            return 1000

    def get_vacancies(self):
        # Returns number of vacancies for a particular period through a matching function
        return max((self.target_L - self.labour) / 10, 100)

    def get_output(self):
        return self.tfp * self.labour**self.a[0] * self.capital**self.a[1]

    def mpl(self):
        # Returns marginal product of labour
        return self.tfp * self.a[0] * self.labour ** (self.a[0] - 1) * self.capital ** self.a[1]

    def mpk(self):
        # Returns marginal product of capital
        return self.tfp * self.a[1] * self.labour ** self.a[0] * self.capital ** (self.a[1] - 1)

    def update_income_payments(self):
        # Splitting the firm's revenue into two parts: One to capital, the other to labour
        # Euler's theorem: F(L, K) = MPL*L + MPK*K
        # Therefore, the shares going to income and labour are MPL*L and MPK*K respectively
        total_income = self.market.price * self.market.quantity_supplied
        self.labour_income = self.market.price * self.mpl() * self.labour
        self.capital_income = self.market.price * self.mpk() * self.capital
        #print(total_income - self.labour_income - self.capital_income)

    # Methods below are for cost-minimization
    def cost_func(self, x, params):
        sign = params[0]
        int_rate = params[1]
        return sign * (self.get_wage() * x[0] + int_rate * x[1])

    def cost_func_derivative(self, x, params):
        sign = params[0]
        int_rate = params[1]
        return np.array([sign * self.wage, sign * int_rate])

    def output_cons(self, L, K):
        return self.market.quantity_sold - self.tfp * L**self.a[0] * K**self.a[1]

    def cost_min_solution(self, int_rate):
        self.cons = (
            {
                'type': 'eq',
                'fun': lambda x: np.array([self.output_cons(x[0], x[1])]),
                'jac': lambda x: np.array([
                    -self.tfp * self.a[0] * x[0] ** (self.a[0]-1) * x[1] ** self.a[1],
                    -self.tfp * self.a[1] * x[0] ** self.a[0] * x[1] ** (self.a[1]-1)])
            }
        )
        return minimize(self.cost_func, [1, 1], args=[1, int_rate], jac=self.cost_func_derivative, constraints=self.cons,
                        method='SLSQP', options={'disp': False})


class Worker:
    def __init__(self, econ, productivity, age, number_of_firms, util_func_params):
        self.econ = econ  # Reference to the economy in which the worker is in
        self.age = age  # Age of the worker
        self.productivity = productivity  # Productivity of the individual
        self.money = 0  # Stock of wealth at a given period
        self.wage = 0  # Hourly wage paid to the worker by the firm
        self.income = 0  # Investment + labour earnings
        self.consumption = 0
        self.investment = 0
        self.savings_rate = 0  # Exogenous savings rate unique to each worker
        self.bargaining_power = 1  # Exogenous bargaining power unique to each worker
        # If worker is employed, job is a reference to the firm that employs the worker
        self.employer = None
        self.hours_worked = 8.0  # Number of hours worked in a 24 hour day

        self.labour_income = 0
        self.capital_income = 0
        self.stocks_owned = [[0 for i in range(number_of_firms)] for i in range(NUMBER_OF_GOODS)]

        self.b = util_func_params  # Parameters used in a worker's utility function for consumption goods

    def kill(self, util_func_params):
        # Kills the particular worker and replaces them with a new one
        # If the worker is employed, then the employer no longer has access to this worker
        if self.employer is not None:
            self.employer.labour -= self.get_productivity()
            self.employer.employee_list.remove(self)
        elif self.employer is None:
            self.econ.unemployed_list.remove(self)
        self.econ.workers.remove(self)
        self.econ.create_worker(util_func_params)  # Creating a new worker to avoid

    def get_productivity(self):
        # Returns the productivity of a worker.
        # The division by 8 is to normalize the productivity in reference to an 8 hour work day
        return self.productivity * self.hours_worked / 8

    def update_income(self):
        # Calculating the worker's labour income received in the period
        if self.employer is not None:
            self.labour_income = (self.get_productivity() / self.employer.labour) * self.employer.labour_income
        # Calculating the worker's capital income received in the period
        self.capital_income = 0
        for i, market in enumerate(self.econ.markets):
            for j, firm in enumerate(market.firms):
                self.capital_income = firm.capital_income * (self.stocks_owned[i][j] / firm.NUMBER_OF_SHARES)
        # Updating the appropriate income, consumption, and investment variables
        self.income = (self.labour_income + self.capital_income) * (1 - self.econ.government.income_tax)
        self.consumption = (1-self.savings_rate) * self.income
        self.investment = self.savings_rate * self.income

    def get_good_demand(self, prices):
        # Manual solution to the utility-maximization problem
        # Returns an array of the quantity demanded of each good by the particular worker
        demand = []
        for i in range(NUMBER_OF_GOODS):
            demand.append(self.consumption * self.b[i] / (prices[i] * sum(self.b)))
        return demand

