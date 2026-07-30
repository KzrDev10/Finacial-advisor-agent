import numpy as np

def project_fixed_savings(current_savings,monthly_contribution,annual_interest_rate,months):
    monthly_rate = annual_interest_rate/12
    periods = np.arange(1,months+1)
    
    principal_growth = current_savings * (1+monthly_rate)**periods

    if monthly_rate > 0:
        contribution_growth = monthly_contribution * (((1 + monthly_rate) ** periods - 1) / monthly_rate)
    else:
        contribution_growth = monthly_contribution * periods
    
    total_balances = principal_growth + contribution_growth
    
 
    return np.round(total_balances, 2)

if "__main__" == __name__:
    print(project_fixed_savings(5000,2000,0.06,12))