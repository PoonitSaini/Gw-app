import streamlit as st
import pandas as pd

st.header("Management Costing")
management_roles = ["Academic Manager", "Manager", "Accountant", "Operator", "Receptionist", "Guard", "Peon"]
management_salary = [50000, 50000, 20000, 15000, 10000, 5000, 12000]
management_months = [12]*7
mgmt_data = []
for i, role in enumerate(management_roles):
    msal = st.number_input(f"{role} Monthly Salary", min_value=0, value=management_salary[i], step=1000, key=f"mgmt_sal_{role}")
    mmonths = st.number_input(f"{role} Months", min_value=1, value=management_months[i], step=1, key=f"mgmt_month_{role}")
    mtotal = msal * mmonths
    mgmt_data.append([role, msal, mmonths, mtotal])
mgmt_df = pd.DataFrame(mgmt_data, columns=["Designation", "Monthly Salary", "Months", "Total"])
st.dataframe(mgmt_df, hide_index=True)
total_mgmt_cost = mgmt_df["Total"].sum()
st.success(f"Total Management Cost: {total_mgmt_cost}")