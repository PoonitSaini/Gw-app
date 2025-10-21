import streamlit as st
import pandas as pd
import numpy as np
from matplotlib import pyplot as plt
import seaborn as sns
import plotly.express as px
from plotly.subplots import make_subplots
import warnings
from PIL import Image

warnings.filterwarnings("ignore")


tab1, tab2, tab3, tab4 = st.tabs([
    "Management", "Academics", "Other Expenses", "Calculation"
])

# ----------- TAB 1: MANAGEMENT COSTING -----------
with tab1:
    st.header("Management Costing")

    # Roles and default values
    roles = ["Academic Manager", "Manager", "Accountant", "Operator", "Receptionist", "Guard", "Peon"]
    default_salary = [50000, 50000, 20000, 15000, 10000, 5000, 12000]
    default_months = [12] * len(roles)

    # Create layout columns and collect inputs
    mgmt_data = []
    for i, role in enumerate(roles):
        st.markdown(f"### {role}")
        col1, col2, col3 = st.columns([5, 5, 3])

        with col1:
            salary = st.number_input(
                f"{role} Salary",
                min_value=0,
                value=default_salary[i],
                step=1000,
                key=f"sal_{i}"
            )

        with col2:
            months = st.number_input(
                f"{role} Months",
                min_value=1,
                value=default_months[i],
                step=1,
                key=f"month_{i}"
            )

        total = salary * months
        with col3:
            st.metric(label="Total", value=total)
        mgmt_data.append([role, salary, months, total])

    # Convert results to a DataFrame
    mgmt_df = pd.DataFrame(mgmt_data, columns=["Designation", "Monthly Salary", "Months", "Total"])
    st.divider()
    st.dataframe(mgmt_df, use_container_width=True, hide_index=True)

    # Display total cost at bottom
    total_mgmt_cost = mgmt_df["Total"].sum()
    st.success(f"Total Management Cost: ₹{total_mgmt_cost:,}")

with tab2:
    st.header("Academics Costing")

    # Role, salary, and months data
    academic_roles = [
        "MT-Nur", "MT-LKG", "MT-UKG", "Hindi LSL", "English LSL", "Maths LSL",
        "EVS LSL", "Activity LSL", "SST AEL+CFL", "Science AEL+CFL", "Maths AEL+CFL",
        "Hindi AEL+CFL", "English AEL+CFL", "Sanskrit AEL+CFL", "Activity AEL+CFL",
        "Coordinator FFL", "Coordinator LSL", "Coordinator AEL"
    ]

    academic_salary = [
        8000, 8000, 8000, 9000, 9000, 9000,
        9000, 9000, 15000, 25000, 20000,
        15000, 20000, 12000, 10000,
        2000, 2000, 2000
    ]

    academic_months = [11,11,11,11,11,11,11,11,11,11,11,11,11,11,11,11,11,11,11]

    academic_data = []
    for i, role in enumerate(academic_roles):
        st.markdown(f"### {role}")
        col1, col2, col3 = st.columns([2, 2, 2])

        with col1:
            asalary = st.number_input(
                f"{role} Salary",
                min_value=0,
                value=academic_salary[i],
                step=500,
                key=f"acad_sal_{i}"
            )

        with col2:
            amonths = st.number_input(
                f"{role} Months",
                min_value=1,
                value=academic_months[i],
                step=1,
                key=f"acad_month_{i}"
            )

        atotal = asalary * amonths
        with col3:
            st.metric(label="Total", value=atotal)

        academic_data.append([role, asalary, amonths, atotal])

    # Convert to DataFrame
    acad_df = pd.DataFrame(academic_data, columns=["Designation", "Monthly Salary", "Months", "Total"])
    st.divider()
    st.dataframe(acad_df, hide_index=True, use_container_width=True)

    # Display total
    total_acad_cost = acad_df["Total"].sum()
    st.success(f"Total Academics Cost: ₹{total_acad_cost:,}")

with tab3:
    st.header("Other / General Expenses")
    other_labels = ["Marketing cost", "Electricity & Water supply", "General Expenses", "Building maintenance"]
    other_defaults = [600000, 150000, 150000, 150000]
    other_fields = []
    for label, default in zip(other_labels, other_defaults):
        value = st.number_input(label, min_value=0, value=default, step=10000, key=f"other_{label}")
        other_fields.append(value)
    total_other = sum(other_fields)
    st.success(f"Total Other Expenses: {total_other}")
    

with tab4:
    st.header("Calculation & Breakeven Analysis")

    col1, col2, col3 = st.columns(3)

    with col1:
    # Student and fee structure inputs
        st.markdown(f"#### GW Parameters")
        divisions = ["FFL (Nur-UKG)", "LSL (1st-5th)", "AEL+CFL (6th-10th)"]
        default_students = {"FFL (Nur-UKG)": 75, "LSL (1st-5th)": 175, "AEL+CFL (6th-10th)": 175}
        default_fees = {"FFL (Nur-UKG)": 15000, "LSL (1st-5th)": 20000, "AEL+CFL (6th-10th)": 25000}
        
        student_counts = {}
        fees_structure = {}

        for div in divisions:
            student_counts[div] = st.number_input(
                f"Student in {div}",
                min_value=0,
                value=default_students[div],
                step=1,
                key=f"calc_stu_{div}",
                width=200
            )
            fees_structure[div] = st.number_input(
                f"fees for {div}",
                min_value=0,
                value=default_fees[div],
                step=500,
                key=f"calc_fee_{div}",
                width=200
            )
            # st.divider()
    
    with col3:
        st.markdown(f"#### Existing School")
        Existing_School_divisions = ["Nur-UKG", "1st-5th", "6th-12th"]
        
        existing_student_counts = {}
        existing_fees_structure = {}

        for div in Existing_School_divisions:
            existing_student_counts[div] = st.number_input(
                f"Student count in {div}",
                min_value=0,
                # value=default_students[div],
                step=1,
                key=f"calc_stu_{div}",
                width=200
            )
            # existing_fees_structure[div] = st.number_input(
            #     f"Annual fees for {div}",
            #     min_value=0,
            #     # value=default_fees[div],
            #     step=500,
            #     key=f"calc_fee_{div}",
            #     width=200
            # )
            # st.divider()
        total_students_in_existing_school = sum(existing_student_counts.values())
   

        ex_student_count = st.number_input("Total Student", value=total_students_in_existing_school, width=200)
        ex_total_revenue = st.number_input("Existing School Total Revenue", min_value=0, step=1000, value=0, key="calc_exist_rev", width=200)
        ex_total_costing = st.number_input("Existing School Total Costing", min_value=0, step=1000, value=0, key="calc_exist_cost", width=200)

        ex_rev_stu = ex_total_revenue / ex_student_count if ex_student_count else 0
        ex_cost_stu = ex_total_costing / ex_student_count if ex_student_count else 0
        ex_profit_stu = ex_rev_stu - ex_cost_stu
        ex_total_profit = ex_total_revenue - ex_total_costing
        
    
    total_students = sum(student_counts.values())
    total_revenue = sum(fees_structure[div] * student_counts[div] for div in divisions)
    
    # Assume these totals are calculated and available from previous tabs or models
    grand_total_cost = total_mgmt_cost + total_acad_cost + total_other  # Use stored globals or pass them here
    
    per_student_cost = grand_total_cost / total_students if total_students else 0
    revenue_per_student = total_revenue / total_students if total_students else 0
    profit_per_student = revenue_per_student - per_student_cost
    total_profit = total_revenue - grand_total_cost
    fees_avg = sum(fees_structure[div] for div in divisions)/3
      

    data = {
        "": ["Per Student Revenue", "Per Student Costing", "Per Student Profit", "Total Profit"],
        "Your Model": [revenue_per_student, per_student_cost, profit_per_student, total_profit],
        "Existing School": [ex_rev_stu, ex_cost_stu, ex_profit_stu, ex_total_profit],
    }
    comp_df = pd.DataFrame(data)
    st.dataframe(comp_df, use_container_width=True, hide_index=True)

    st.subheader("Breakeven Analysis After Paying Existing Owner Profit")
    ex_profit_payable = ex_total_profit
    if profit_per_student > 0:
        min_students_needed = int((((total_revenue-total_profit)+ex_total_profit)/fees_avg)) + 1
        max_students_can_leave = ex_student_count - min_students_needed
        st.write(f"You need at least **{min_students_needed}** students to cover payout to owner ({ex_profit_payable:,.0f}).")
        st.write(f"Maximum students that can leave before you start making a loss: **{max_students_can_leave}**")
        if min_students_needed > ex_student_count:
            st.error(
                f"Breakeven students required ({min_students_needed}) are more than existing school students ({ex_student_count})."
            )
            st.warning("Consider strategies to increase enrollment or reduce costs.")
        else:
            st.success(
                f"Breakeven students ({min_students_needed}) are less than or equal to existing school students ({ex_student_count})."
            )


        total_profit = total_revenue - grand_total_cost
        Total_Cost_With_Payable_Amount =((total_revenue-total_profit)+ex_total_profit)
        students_remaining = st.slider("Adjust students remaining after attrition", 0, total_students, ex_student_count)
        profit_after_payout = ((students_remaining * fees_avg) - Total_Cost_With_Payable_Amount)
        st.write(f"Profit after payout with {students_remaining} students: **{profit_after_payout:,.2f}**")
        if profit_after_payout >= 0:
            st.success("Still profitable.")
        else:
            st.error("At a loss.")
    else:
        st.error("Your model is not profitable per student, cannot cover owner payout.")

    st.caption("Adjust the numbers in any tab to recalculate automatically.")

    col1,col2,col3 = st.columns(3)
    Profit_Per_Student_After_All_Cost = int(profit_per_student-ex_profit_stu)
    Total_Cost = int(per_student_cost*425 + ex_total_profit)
    with col1:
        st.metric(label="Total Cost", value=Total_Cost)
    with col3:
        st.metric(label="Profit Per Student After All Cost", value=Profit_Per_Student_After_All_Cost)
 

   