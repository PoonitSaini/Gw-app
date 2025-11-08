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
st.set_page_config(
    page_title="GW",
    page_icon="Images\logo.png"
)


home_page = st.Page(
    page="Pages/Home.py"
)

profit_loss_calcultion = st.Page(
    page="Pages/Profit_Loss_Calculation.py"
)
Management = st.Page(
    page="Pages/Profit_Loss_Calculation.py"
)
student_issues = st.Page(
    page="Pages/Student_Issue.py"
)
teacher_issues = st.Page(
    page="Pages/Teacher_Issue.py"
)

pg = st.navigation(
    {
        "Main":[home_page],
        "School Calculation":[profit_loss_calcultion],
        "Academic Monitoring":[student_issues,teacher_issues]
    }
)

pg.run()