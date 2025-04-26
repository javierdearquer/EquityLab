import yfinance as yf
import numpy as np

def get_risk_free_rate():
    """Fetches the US 10-Year Treasury yield from yfinance."""
    try:
        treasury = yf.Ticker("^TNX")  # ^TNX = CBOE 10-Year Treasury Note Yield
        yield_percent = treasury.history(period="1d")["Close"].iloc[-1]
        return yield_percent / 100  # Convert from % to decimal
    except:
        return 0.04  # fallback default

def calculate_wacc(ticker, ERP=0.04):
    stock = yf.Ticker(ticker)
    info = stock.info
    beta = info.get("beta", None)

    if beta is None:
        raise ValueError("Missing market cap or beta from yfinance.")

    # Get Total Debt (Short + Long Term) from balance sheet
    bs = stock.balance_sheet
    try:
        latest_period = bs.columns[0]
        short_term_debt = bs.loc["Current Debt"].iloc[0] if "Current Debt" in bs.index else 0
        long_term_debt = bs.loc["Long Term Debt"].iloc[0] if "Long Term Debt" in bs.index else 0
        total_debt = short_term_debt + long_term_debt
    except:
        total_debt = 0

    # Get Interest Expense from income statement
    fin = stock.financials
    try:
        interest_expense = abs(fin.loc["Interest Expense"].iloc[0]) if "Interest Expense" in fin.index else 0
        if np.isnan(interest_expense):
            interest_expense = 0
    except:
        interest_expense = 0

    # Cost of Equity using CAPM
    risk_free_rate = get_risk_free_rate()
    cost_of_equity = risk_free_rate + beta * ERP #(market_return - risk_free_rate)

    # Cost of Debt
    cost_of_debt = (interest_expense / total_debt) if total_debt > 0 else 0

    try:
        tax_rate = fin.T['Tax Provision']/fin.T['Pretax Income']
        tax_rate = tax_rate.mean()
    except:
        tax_rate = 0.21 # Tax Rate (assumed to be 21% for US companies)

    # WACC
    E = bs.T.sort_index()['Stockholders Equity'].iloc[-1]
    D = total_debt
    V = E + D
    wacc = (E / V) * cost_of_equity + (D / V) * cost_of_debt * (1 - tax_rate)

    return {
        "Market Cap": E,
        "Beta": beta,
        "Risk-Free Rate": risk_free_rate,
        "Cost of Equity": cost_of_equity,
        "Total Debt": D,
        "Interest Expense": interest_expense,
        "Cost of Debt": cost_of_debt,
        "WACC": wacc
    }

# Example usage
ticker = "BABA"
#WACC using anual reports 10K
results = calculate_wacc(ticker)

#TODO create a version using the quarterly reports (therefore more relevan/recent)

for key, value in results.items():
    print(f"{key}: {value:.4f}" if isinstance(value, float) else f"{key}: {value}")
