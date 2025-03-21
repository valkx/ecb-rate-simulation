# ECB Interest Rate Calculator

This repository contains a Python script to calculate the interest rate based on a modified Taylor Rule, which could be used by the European Central Bank (ECB) to set its main refinancing rate.

## Background

The Taylor Rule is an economic guideline for setting interest rates based on inflation and output conditions. The modified version implemented here is:

\[ \text{Interest rate} = \text{Equilibrium rate} + 1.5 \times (\text{Inflation} - \text{Target inflation}) + 0.5 \times \text{Output gap} \]

Where:
- **Equilibrium rate**: The long-term neutral interest rate (in %).
- **Inflation**: The current inflation rate (in %).
- **Target inflation**: The ECB's inflation target, typically 2% (in %).
- **Output gap**: The difference between actual and potential GDP, expressed as a percentage.

## Usage

Run the script `taylor_rule.py` in a Python environment. When prompted, enter the required values:
- Equilibrium rate
- Current inflation rate
- Target inflation rate
- Output gap

The script will output the calculated interest rate.

### Example

For the following inputs:
- Equilibrium rate: 1%
- Current inflation: 3%
- Target inflation: 2%
- Output gap: -1%

The calculation is:
\[ 1 + 1.5 \times (3 - 2) + 0.5 \times (-1) = 1 + 1.5 - 0.5 = 2.0\% \]

The script outputs: "The calculated interest rate is: 2.00%"

## Assumptions

- The equilibrium rate is provided as an input (in practice, it’s estimated using economic models).
- All inputs must be numeric values.
- The formula allows for negative interest rates, reflecting ECB policy history.

## License

This project is licensed under the MIT License.