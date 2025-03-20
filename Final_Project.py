import numpy as np
import pandas as pd

def allocate_portfolio():
    # Define the data structures for portfolios and breakdown
    investment_portfolios = {
        (60000, '1-2 year'): 1, (60000, '3-5 years'): 2, (60000, '5-8 years'): 3, (60000, '8+ years'): 4,
        (100000, '1-2 year'): 5, (100000, '3-5 years'): 6, (100000, '5-8 years'): 7, (100000, '8+ years'): 8,
        (150000, '1-2 year'): 9, (150000, '3-5 years'): 10, (150000, '5-8 years'): 11, (150000, '8+ years'): 12,
        (250000, '1-2 year'): 13, (250000, '3-5 years'): 14, (250000, '5-8 years'): 15, (250000, '8+ years'): 16
    }

    portfolio_details = {
        1: (150000, 140428), 2: (600000, 495201), 3: (1320000, 805471), 4: (2940000, 1624804),
        5: (400000, 374476), 6: (1000000, 825335), 7: (2200000, 1342452), 8: (4900000, 2708006),
        9: (600000, 561714), 10: (1500000, 12380039), 11: (3300000, 2013678), 12: (7350000, 4062010),
        13: (1000000, 936191), 14: (2500000, 2063339), 15: (5500000, 3356131), 16: (12250000, 6770017)
    }

    portfolio_breakdown = {
        "HDFC Top 100 Fund": ("Equity", "Large Cap", "Short term/ Mid term", 20),
        "Kotak Emerging Equity Fund": ("Equity", "Mid Cap", "Mid term/ Long term", 20),
        "Quant Small Cap Fund": ("Equity", "Small Cap", "Long term", 20),
        "HDFC Gold ETF FoF": ("Precious Metals", "Gold", "Short term/ Mid term", 20),
        "Invesco India Credit Risk Fund": ("Debt", "Debt", "Short term", 20)
    }


    try:

        # Input from the user
        income = int(input("Enter your income level (e.g., 60000, 100000, 150000, 250000): "))
        experience = input("Enter your experience in investing (1-2 year, 3-5 years, 5-8 years, 8+ years): ").strip()

        # Get the portfolio number based on user input
        # i.e if user enter 50000 as income and 1-2 years he should get portfolio: 1
        portfolio_num = investment_portfolios.get((income, experience))

        if portfolio_num is None:
            print("No matching portfolio found for the given income and experience.")
            return

        # Fetch the portfolio details
        portfolio_value, invested_amount = portfolio_details[portfolio_num]
        profit = portfolio_value - invested_amount

        # Suggest SIP investment (5% of income)
        sip_investment = 0.05 * income

        print(f"\nAssigned Portfolio: {portfolio_num}")
        print(f"Portfolio Value: {portfolio_value}")
        print(f"Suggested SIP Investment: {sip_investment}\n")

        # Display the breakdown for the assigned portfolio
        print("Breakdown:")
        portfolio_profit = portfolio_value - invested_amount
        for fund, (asset_class, sub_asset_class, Time_horizon, allocation) in portfolio_breakdown.items():
            fund_value = portfolio_value * allocation // 100

            print(f"{fund} ({asset_class} - {sub_asset_class}), {Time_horizon}:\n",
                  f"  Current Value: {fund_value}")


        # Load return rates and standard deviations from CSV files 
        rates_data = pd.read_csv('Rate_of_returns_funds.csv')  # Annually returns
        std_data = pd.read_csv('Std_deviation.csv')  # Standard deviations

        # Collect goals from the user-Details
        num_goals = int(input("\nEnter the number of financial goals you have: "))
        goals = []
        for i in range(num_goals):
            print(f"\nEnter details for Goal {i + 1}:")
            goal_name = input("Goal Name: ")
            goal_amount = float(input("Goal Amount: "))
            goal_category = input("Goal Time Horizon (Short term, Mid term, Long term): ").capitalize()
            goal_priority = input("Goal Priority (High, Medium, Low): ").capitalize()
            goal_time_horizon = int(input("Goal Time Horizon (in months): "))
            goals.append({
                "name": goal_name,
                "amount": goal_amount,
                "category": goal_category,
                "priority": goal_priority,
                "time_horizon": goal_time_horizon
            })


        # First Sort goals by priority (High > Medium > Low)
        priority_order = {"High": 1, "Medium": 2, "Low": 3}
        goals.sort(key=lambda g: priority_order[g["priority"]])

        # Allocate funds to goals
        allocated_funds = {fund: 0 for fund in portfolio_breakdown.keys()}
        portfolio_utilization = {fund: 0 for fund in portfolio_breakdown.keys()}  # Tracker for portfolio utilization in percentages

        num_simulations = 1000

        for goal in goals:
            print(f"\nAllocating funds for goal: {goal['name']}\n")
            remaining_goal_amount = goal["amount"]

            for fund, details in portfolio_breakdown.items():
                asset_class, sub_asset_class, time_horizon, allocation = details

                # Check if the fund matches the goal's time horizon
                if goal["category"] in time_horizon.split("/"):
                    fund_value = portfolio_value * allocation // 100   #>>>>>>>>>>>>
                    sip_growth_simulations = []  # sip growth 
                    fund_value_simulations = []  # fund current value 
                    growth_rate = []          # rate of return 
                    successful_simulations = 0    # to check for the simulation successfull

                    # Extract mean and standard deviation for the fund
                    if fund in rates_data.columns and fund in std_data.columns:
                        if goal["category"] == "Short term":
                            random_indices = np.random.choice(rates_data[fund].index, size=3, replace=True)
                            fund_mean_return = rates_data[fund].loc[random_indices].mean()
                            fund_std_dev = std_data[fund].mean()
                        elif goal["category"] == "Mid term":
                            random_indices = np.random.choice(rates_data[fund].index, size=6, replace=True)
                            fund_mean_return = rates_data[fund].loc[random_indices].mean()
                            fund_std_dev = std_data[fund].mean()
                        elif goal["category"] == "Long term":
                            random_indices = np.random.choice(rates_data[fund].index, size=10, replace=True)
                            fund_mean_return = rates_data[fund].loc[random_indices].mean()
                            fund_std_dev = std_data[fund].mean()
                    else:
                        continue

                    # Run Monte Carlo simulations
                    for _ in range(num_simulations):
                        random_growth_rate = np.random.normal(fund_mean_return, fund_std_dev)
                        time_in_years = goal["time_horizon"] / 12
                        growth_rate.append(random_growth_rate)

                        if random_growth_rate == 0:
                            sip_growth = sip_investment * goal["time_horizon"]
                            sip_growth_simulations.append(sip_growth)
                        else:
                            sip_growth = sip_investment * (((((1 + random_growth_rate/12) ** goal["time_horizon"]) - 1) / random_growth_rate/12))*(1+ random_growth_rate)
                            sip_growth_simulations.append(sip_growth)

                        # Simulate invested amount growth
                        future_investment_value = fund_value * ((1 + random_growth_rate) ** time_in_years)
                        fund_value_simulations.append(future_investment_value)

                        future_investment_value = future_investment_value * (1 - portfolio_utilization[fund])
                        sip_growth = sip_growth * (1 - portfolio_utilization[fund])

                        # checking the successful simulations
                        if future_investment_value + sip_growth >= remaining_goal_amount:
                            successful_simulations += 1


                    # Calculate the mean future value from simulations
                    mean_sip_growth = np.mean(sip_growth_simulations)
                    mean_investment_growth = np.mean(fund_value_simulations)
                    future_value = mean_investment_growth + mean_sip_growth
                    mean_growth_rate = np.mean(growth_rate)

                    # Probability of the achievement of simulation
                    probability_of_achievement = (successful_simulations / num_simulations) * 100

                    # Calculate the available fund considering utilization
                    available_fund = future_value * (1 - portfolio_utilization[fund])

                    # Determine allocation
                    allocation = min(remaining_goal_amount, available_fund - allocated_funds[fund])
                    if allocation < 0:
                        allocation = 0
                        # print(f"Warning: {fund} overutilized beyond 100%!")
                        continue
                    allocated_funds[fund] += allocation
                    remaining_goal_amount -= allocation

                    # Update utilization tracker
                    portfolio_utilization[fund] += allocation / future_value

                    print(f"Allocated {allocation:.2f} to {fund} (Mean Future Value: {future_value:.2f}, "
                          f"Utilization: {portfolio_utilization[fund] * 100:.2f}%, Remaining Goal Amount: {remaining_goal_amount:.2f},"
                          f"Probability of Achievement: {probability_of_achievement:.2f}%, with the rate of return: {mean_growth_rate:.2f})")

                    if portfolio_utilization[fund] > 1:
                        print(f"Warning: {fund} overutilized beyond 100%!")

                    if remaining_goal_amount <= 0:
                        break
                        

            # Fallback mechanism: Allocate from other funds if goal is not fully satisfied
            if remaining_goal_amount > 0:
                print(f"Fallback allocation for goal: {goal['name']}")
                for fund, details in portfolio_breakdown.items():
                    asset_class, sub_asset_class, time_horizon, allocation = details
                    fund_value = portfolio_value * allocation // 100
                    available_fund = fund_value - allocated_funds[fund]
                    sip_growth_simulations = []  # sip growth 
                    fund_value_simulations = []  # fund current value 
                    growth_rate = []          # rate of return 
                    successful_simulations = 0    # to check for the simulation successfull

                    # Extract mean and standard deviation for the fund
                    if fund in rates_data.columns and fund in std_data.columns:
                        if goal["category"] == "Short term":
                            random_indices = np.random.choice(rates_data[fund].index, size=3, replace=True)
                            fund_mean_return = rates_data[fund].loc[random_indices].mean()
                            fund_std_dev = std_data[fund].mean()
                        elif goal["category"] == "Mid term":
                            random_indices = np.random.choice(rates_data[fund].index, size=6, replace=True)
                            fund_mean_return = rates_data[fund].loc[random_indices].mean()
                            fund_std_dev = std_data[fund].mean()
                        elif goal["category"] == "Long term":
                            random_indices = np.random.choice(rates_data[fund].index, size=10, replace=True)
                            fund_mean_return = rates_data[fund].loc[random_indices].mean()
                            fund_std_dev = std_data[fund].mean()
                    else:
                        continue

                    # Run Monte Carlo simulations
                    for _ in range(num_simulations):
                        random_growth_rate = np.random.normal(fund_mean_return, fund_std_dev)
                        time_in_years = goal["time_horizon"] / 12
                        growth_rate.append(random_growth_rate)

                        if random_growth_rate == 0:
                            sip_growth = sip_investment * goal["time_horizon"]
                            sip_growth_simulations.append(sip_growth)
                        else:
                            sip_growth = sip_investment * (((((1 + random_growth_rate/12) ** goal["time_horizon"]) - 1) / random_growth_rate/12))*(1+ random_growth_rate)
                            sip_growth_simulations.append(sip_growth)

                        # Simulate invested amount growth
                        future_investment_value = fund_value * ((1 + random_growth_rate) ** time_in_years)
                        fund_value_simulations.append(future_investment_value)

                        future_investment_value = future_investment_value * (1 - portfolio_utilization[fund])
                        sip_growth = sip_growth * (1 - portfolio_utilization[fund])

                        # checking the successful simulations
                        if future_investment_value + sip_growth >= remaining_goal_amount:
                            successful_simulations += 1

                    # Calculate the mean future value from simulations
                    mean_sip_growth = np.mean(sip_growth_simulations)
                    mean_investment_growth = np.mean(fund_value_simulations)
                    future_value = mean_investment_growth + mean_sip_growth
                    mean_growth_rate = np.mean(growth_rate)

                     # Probability of the achievement of simulation
                    probability_of_achievement = (successful_simulations / num_simulations) * 100

                    # Calculate the available fund considering utilization
                    available_fund = future_value * (1 - portfolio_utilization[fund])

                    # Determine allocation
                    allocation = min(remaining_goal_amount, available_fund - allocated_funds[fund])
                    if allocation < 0:
                        allocation = 0
                        # print(f"Warning: {fund} overutilized beyond 100%!")
                        continue
                    allocated_funds[fund] += allocation
                    remaining_goal_amount -= allocation

                    # Update utilization tracker
                    portfolio_utilization[fund] += allocation / future_value

                    print(f"Allocated {allocation:.2f} to {fund} (Mean Future Value: {future_value:.2f}, "
                          f"Utilization: {portfolio_utilization[fund] * 100:.2f}%, Remaining Goal Amount: {remaining_goal_amount:.2f},"
                          f"Probability of Achievement: {probability_of_achievement:.2f}%, with the rate of return: {mean_growth_rate:.2f})")

                    if portfolio_utilization[fund] > 1:
                        print(f"Warning: {fund} overutilized beyond 100%!")

                    if remaining_goal_amount <= 0:
                        break         
                    

            if remaining_goal_amount > 0:
                print(f"Warning: Could not fully allocate funds for goal: {goal['name']}\n")

    except ValueError:
        print("Invalid input. Please enter numeric values where required.")

if __name__ == "__main__":
    allocate_portfolio()



