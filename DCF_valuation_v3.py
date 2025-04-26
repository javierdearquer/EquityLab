import yfinance as yf
import pandas as pd
import numpy as np

pd.set_option('future.no_silent_downcasting', True)

'''
Parameters:
1. Periods of growth
2. Periods of transition
3. Initial growth
4. Terminal growth
5. WC as % of revenue
'''
ticker_str = ""

n_periods_growth = 2
n_periods_transition = 8

growth_initial = 0.065 #TODO estimate from the historical data
growth_terminal = 0.025 #TODO potentially could be LLM generated based on news and internet research on the field

start_year = 2025 # TODO take the next year after the last of financials

def dcf(cash_flows, discount_rate):
    # Calculate the present value using: PV = CF / (1 + r)^t + TV/(1 + r)^T
    present_values_cf = [cf / (1 + discount_rate) ** t for t, cf in enumerate(cash_flows, start=1)]
    return present_values_cf

def get_risk_free_rate():
    """Fetches the US 10-Year Treasury yield from yfinance."""
    try:
        treasury = yf.Ticker("^TNX")  # ^TNX = CBOE 10-Year Treasury Note Yield
        data = treasury.history()
        last_quote = data['Close'].iloc[-1]
        return last_quote / 100  # Convert from % to decimal
    except:
        return 0.04  # fallback default
    
ticker = yf.Ticker(ticker_str)

info = ticker.info
beta = info.get("beta", None)

# Divided to get all units in millions
fin_is = ticker.quarterly_financials.T/1000000
#fin_is = ticker.financials.T/1000000
fin_is = fin_is.sort_index()

fin_bs = ticker.quarterly_balancesheet.T/1000000
#fin_bs = ticker.balancesheet.T/1000000
fin_bs = fin_bs.sort_index()

fin_cf = ticker.quarterly_cashflow.T/1000000
#fin_cf = ticker.cashflow.T/1000000
fin_cf = fin_cf.sort_index()

# TODO convert all the numerical values to the same format (i.e. float with 2 decimals)
# TODO determine if I want the last value of the mean ...

# Compute the TTM revenue of the firm (based on the 10Q filings)
revenue = fin_is['Total Revenue'][-4:].sum(axis=0)

earnings = fin_is['Net Income'][-4:].sum(axis=0)
#dividends = abs(fin_cf['Cash Dividends Paid'][-4:].sum(axis=0))
try:
    capex = abs(fin_bs['Gross PPE'].diff().fillna(0).iloc[-1]) # Gross - Depreciation = Net PPE -> investment is Delta on Gross
except:
    capex = abs(fin_bs['Net PPE'].diff().fillna(0).iloc[-1]) # Gross - Depreciation = Net PPE -> investment is Delta on Gross

depreciation = abs(fin_cf['Depreciation And Amortization'][-4:].sum(axis=0))

try:
    wc = fin_bs['Working Capital']
except:
    try:
        wc = fin_bs['Current Assets'] - fin_bs['Current Liabilities'] 
    except:
        wc = fin_bs.iloc[:,0]-fin_bs.iloc[:,0]

dwc = wc.diff().fillna(0) # change in working capital    

wc_of_revenue = (wc)/fin_is['Total Revenue'] # Get latest WC values and divide by the Total Revenue
wc_of_revenue = wc_of_revenue.mean() # make the average of all of them

debt_to_equity = fin_bs['Total Debt'] / fin_bs['Stockholders Equity'] # debt to equity ratio
debt_to_equity = debt_to_equity.mean()

cost_of_equity = get_risk_free_rate() + beta * 0.04 # TODO instead of using ERP, take the Rm from comparables

# Create the list of years
years = list(range(start_year, start_year + n_periods_growth + n_periods_transition))

# Create an empty DataFrame with rows for each year
df = pd.DataFrame({'Year': years})

# TODO add a different growth for the different items
# I'm keeping the model simple in purpose to make it easier to understand
df['growth'] = [growth_initial] * n_periods_growth + list(np.linspace(growth_initial, growth_terminal, n_periods_transition))

df.loc[0, 'revenue'] = revenue * (1 + df.loc[0, 'growth'])  # First value of Calculation1
for i in range(1, len(df)):
    df.loc[i, 'revenue'] = df.loc[i - 1, 'revenue'] * (1+ df.loc[i, 'growth'])

df.loc[0, 'earnings'] = earnings * (1 + df.loc[0, 'growth'])  # First value of Calculation1
for i in range(1, len(df)):
    df.loc[i, 'earnings'] = df.loc[i - 1, 'earnings'] * (1+ df.loc[i, 'growth'])

df.loc[0, 'capex-dpr'] = (capex - depreciation) * (1 + df.loc[0, 'growth'])  # First value of Calculation1
for i in range(1, len(df)):
    df.loc[i, 'capex-dpr'] = df.loc[i - 1, 'capex-dpr'] * (1+ df.loc[i, 'growth'])
df['capex-dpr'] = df['capex-dpr'] * debt_to_equity / (1 + debt_to_equity) # * D/(D+E)

df.loc[0, 'chg_wc'] = wc_of_revenue * revenue * (df.loc[0, 'growth'])  # First value of Calculation1
for i in range(1, len(df)):
    df.loc[i, 'chg_wc'] = (df.loc[i , 'revenue'] - df.loc[i - 1, 'revenue']) * wc_of_revenue
df['chg_wc'] = df['chg_wc'] * debt_to_equity / (1 + debt_to_equity) # * D/(D+E)

df['FCFE'] = df['earnings'] - df['capex-dpr'] - df['chg_wc'] 

PV_FCFE = sum(dcf(df['FCFE'], cost_of_equity))
TV = df['FCFE'].iloc[-1:]*(1+growth_terminal)/(cost_of_equity-growth_terminal)
PV_TV = TV.iloc[0] / (1+cost_of_equity)**(n_periods_growth+n_periods_transition)

n_shares = fin_bs['Ordinary Shares Number'].iloc[-1] # number of shares outstanding
share_price = ticker.history()["Close"].iloc[-1]
print(f"Share Price: {share_price}")
print(f"Valuation: {(PV_FCFE+PV_TV)/n_shares}")

#print(df)