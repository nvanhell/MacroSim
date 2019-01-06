# MacroSim

## Description

This project is an attempt at simulating a dynamic multi-period macroeconomy based on microeconomic behaviour and a simple life-cycle model. Two independent economies are simulated side-by-side to allow for comparisons between the two economies when parameters or policies are changed. There are many goods (the specific number of goods may be set during initialization) where one market exists per good. Consumers demand goods, and firms supply them. Firms demand labour (supplied by households) and capital (not currently implemented). Moreover, a government exists which can implement various policies.

## Roadmap

#### Complete:

- Demand for goods through utility-maximization (solution solved by hand due to Scipy implementation being excessively slow)

- Supply of goods through production by firms

- Labour market matching mechanism

#### Partially Complete:

- Cost-minimzation by firms: Computation and optimal input targeting need better implementation

- Government policies: Consumption tax, tax on individual goods, and income tax are all functional, but governmending is not. Minmum wage needs implementation

- Savings and investment decisions: Currently only a basic dividend payout from firm profits

- Heterogeneity between workers: Exogenous variation between workers exists, but no endogenous factors such as education or work experience

- GUI: Mostly functional, but need to clean it up and allow users to edit simulation and economic parameters

#### To-do:

- work-leisure optimization by individuals

- Price mechanism

- Code optimization (if needed). Current code is implemented in a logical order rather than in an efficient order.

## Installation

The program should run successfully by simply installing the requirements and running main.py
