# Portfolio Allocation (SensibleT)

## 🛠️ Overview
This project demonstrates a **portfolio allocation** strategy based on different investment amounts and time horizons. It uses Python with `numpy` and `pandas` for efficient data handling.

## 📊 Files Included
- `Final_Project.py`: The main script that contains the portfolio allocation logic.
- `Rate_of_returns_fund.csv`: Contains the historical rate of returns for various funds.
- `Std_deviation.csv`: Contains the standard deviation values for different portfolios (15 years of data).

## 🔥 Features
- **Dynamic Goal Matching:** The project can match **any number of goals** (2–10 or more) and provides the final allocation that yields the **maximum returns**.
- **Fallback Mechanism:** 
    - If the desired goal (e.g., long-term) is not fully achieved due to a lack of available funds, the program **automatically falls back** to mid-term or short-term portfolios.
    - This ensures that no investment is left out and the goal is achieved with the next best-matching funds.
- **Real-World Data:** 
    - Uses actual **rate of returns** and **standard deviation** data over 15 years, making the model realistic and reliable.
- **Scenario & Risk Analysis:** 
    - Incorporates **scenario analysis** and **Value at Risk (VaR)** by considering real return rates and 15 years of deviation data.
- **Scalable for Large-Scale Implementation:** 
    - This is a **demo version**, and the same logic will be implemented at a larger scale with **optimization and improved time complexity**.

## 🚀 How to Run
1. Clone the repository:
```bash
git clone <[https://github.com/Piikachu07/Portfolio_Allocation.git]>
