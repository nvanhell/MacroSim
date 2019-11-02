# MacroSim

## Description

This Python project is an attempt at simulating a dynamic multi-period macroeconomy based on microeconomic behaviour. Two independent economies are simulated side-by-side to allow for comparisons between the two when parameters or policies are changed. The project is intended to be a proof of concept and the economic modeling is largely homemade.

The general idea behind the program is that goods are both produced and demanded in each market. Prices adjust in response to excess quantity demanded or quantity supplied. Firms demand labour and capital to produce goods which are producedin a labour market and capital market. Both workers and firms behave in optimizing behaviour. Some government policies are modeled, such as various taxes and a minimum wage. The program is not restricted in the number of consumption goods, firms, and consumers.

The images below are samples of the GUI which is used to help visualize some of the economic variables in the model. The upper graph displays variables of the first economy while the lower graph displayes the variables in the second. In this example, unemployment was initialized at some arbitrarily large (50%) value and evolves downwards over time as workers are matched with employers.


![untitled2](https://user-images.githubusercontent.com/45185574/51011923-912c8580-1528-11e9-8013-f27fdac51ef3.png)

![untitled](https://user-images.githubusercontent.com/45185574/51011924-925db280-1528-11e9-9bd7-d3e4b6e91950.png)



## Roadmap

#### Complete:

- Labour market matching mechanism.

#### Partially Complete:

- Price mechanism.

- Demand for goods through utility-maximization (utility function is temporary).

- Supply of goods through production by firms (profit function is temporary).

- Cost-minimzation by firms: Computation and optimal input targeting need better implementation.

- Government policies: Consumption tax, tax on individual goods, and income tax are all functional. Government spending mechanism has not been implemented yet.

- Savings, investment and basic stock market are placeholders.

- Randomly generated exogenous variation between worker productivity exists, but no endogenous factors such as education or work experience are currently implemented.

- wxPython GUI: Mostly functional, but need to clean it up and allow users to edit simulation and economic parameters.

#### To-do:

- Work-leisure optimization by workers.

- Imperfectly competitive behaviour between firms.

- Code optimization. Current code is implemented in a logical order rather than in an efficient order.

- Allowing simulation data to be saved into a spreadsheet format.

## Installation

The program should run successfully by simply installing the requirements and running main.py.
