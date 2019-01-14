# MacroSim

## Description

This Python project is an attempt at simulating a dynamic multi-period macroeconomy based on microeconomic behaviour. Two independent economies are simulated side-by-side to allow for comparisons between the two when parameters or policies are changed. The project is intended to be a proof of concept and the economic modeling is largely homemade.

The general idea behind the model is that goods are demanded by workers and then supplied by firms where exactly one good is traded in each market. Firms demand labour and capital to produce goods. Both workers and firms behave in optimizing behaviour. Some government policies are modeled, such as various taxes and a minimum wage. The simulation is generalized and supports any number of consumption goods, firms, and consumers.

The images below are samples of the GUI which is used to help visualize some of the economic variables in the model. The upper graph displays variables of the first economy while the lower graph displayes the variables in the second.


![untitled2](https://user-images.githubusercontent.com/45185574/51011923-912c8580-1528-11e9-8013-f27fdac51ef3.png)

![untitled](https://user-images.githubusercontent.com/45185574/51011924-925db280-1528-11e9-9bd7-d3e4b6e91950.png)



## Roadmap

#### Complete:

- Demand for goods through utility-maximization (for now, the solution is solved by hand due to Scipy implementation being excessively slow).

- Supply of goods through production by firms.

- Labour market matching mechanism.

#### Partially Complete:

- Cost-minimzation by firms: Computation and optimal input targeting need better implementation.

- Government policies: Consumption tax, tax on individual goods, and income tax are all functional, but no government spending mechanism is implemented.

- Savings, investment and basic stock market are placeholders.

- Randomly generated exogenous variation between worker productivity exists, but no endogenous factors such as education or work experience currently exist. I would also like to construct economy-specific income/wealth distributions imbeded in wxPython in order to visualize inequality in the model.

- wxPython GUI: Mostly functional, but need to clean it up and allow users to edit simulation and economic parameters.

#### To-do:

- Work-leisure optimization by workers.

- Price mechanism.

- Imperfectly competitive behaviour between firms.

- Code optimization. Current code is implemented in a logical order rather than in an efficient order.

- Allowing simulation data to be saved into a spreadsheet format.

## Installation

The program should run successfully by simply installing the requirements and running main.py.
