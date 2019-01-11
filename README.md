# MacroSim

## Description

This project is an attempt at simulating a dynamic multi-period macroeconomy based on microeconomic behaviour and a simple life-cycle model in Python. Two independent economies are simulated side-by-side to allow for comparisons between the two when parameters or policies are changed. The project is intended to be a proof of concept and the economic modeling is largely homemade.

The general idea behind the model is that goods are demanded by workers and then supplied by firms where exactly one good is traded in each market. Firms demand labour and capital to produce goods. Both workers and firms behave in optimizing behaviour. Some government policies are modeled, such as various taxes and a minimum wage. The simulation is generalized and supports any number of consumption goods and any number of firms per market. 

## Roadmap

#### Complete:

- Demand for goods through utility-maximization (solution solved by hand due to Scipy implementation being excessively slow).

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

## Installation

The program should run successfully by simply installing the requirements and running main.py.

## My model

![equation](https://latex.codecogs.com/png.latex?L%20%3D%20%5Cprod_%7Bj%3D1%7D%5E%7Bn%7Dx_j%5Ea%5Ej%20&plus;%20%5Clambda%20%28I%20-%20%5Csum_%7Bj%3D1%7D%5E%7Bn%7Dp_ix_i%29)
