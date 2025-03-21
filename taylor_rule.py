def calculate_interest_rate(equilibrium_rate, inflation, target_inflation, output_gap):
    """
    Calculate the interest rate based on the modified Taylor Rule.

    Parameters:
    equilibrium_rate (float): The long-term neutral interest rate (%).
    inflation (float): The current inflation rate (%).
    target_inflation (float): The target inflation rate (%).
    output_gap (float): The output gap as a percentage of potential GDP.

    Returns:
    float: The calculated interest rate (%).
    """
    return equilibrium_rate + 1.5 * (inflation - target_inflation) + 0.5 * output_gap

if __name__ == "__main__":
    print("ECB Interest Rate Calculator based on Modified Taylor Rule")
    try:
        equilibrium_rate = float(input("Enter the equilibrium rate (%): "))
        inflation = float(input("Enter the current inflation rate (%): "))
        target_inflation = float(input("Enter the target inflation rate (%): "))
        output_gap = float(input("Enter the output gap (%): "))
        interest_rate = calculate_interest_rate(equilibrium_rate, inflation, target_inflation, output_gap)
        print(f"The calculated interest rate is: {interest_rate:.2f}%")
    except ValueError:
        print("Please enter valid numeric values.")