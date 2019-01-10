# MacroSim

## Description

This project is an attempt at simulating a dynamic multi-period macroeconomy based on microeconomic behaviour and a simple life-cycle model. Two independent economies are simulated side-by-side to allow for comparisons between the two when parameters or policies are changed. The simulation is generalized and supports any number of consumption goods and any number of firms per market. The general idea behind the economy is simply that goods are demanded by households and then produced by firms. Firms then demand homogeneous labour and capital which allow them to produce goods in the first place. Various governmental policies can be implemented, such as various taxes and/or a minimum wage.

## Roadmap

#### Complete:

- Demand for goods through utility-maximization (solution solved by hand due to Scipy implementation being excessively slow)

- Supply of goods through production by firms

- Labour market matching mechanism

#### Partially Complete:

- Cost-minimzation by firms: Computation and optimal input targeting need better implementation

- Government policies: Consumption tax, tax on individual goods, and income tax are all functional, but no government spending mechanism is implemented. Minmum wage also needs implementation

- Savings, investment and basic stock market are very primitive

- Heterogeneity between workers: Exogenous variation between worker productivity is randomly generated, but no endogenous factors such as education or work experience currently exist. I would also like to construct economy-specific income/wealth distributions imbeded in wxPython in order to visualize inequality in the model

- wxPython GUI: Mostly functional, but need to clean it up and allow users to edit simulation and economic parameters

#### To-do:

- Work-leisure optimization by individuals

- Price mechanism

- Imperfectly competitive behaviour between firms

- Code optimization. Current code is implemented in a logical order rather than in an efficient order.

## Installation

The program should run successfully by simply installing the requirements and running main.py
