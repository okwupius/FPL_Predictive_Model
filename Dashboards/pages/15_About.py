import streamlit as st

st.set_page_config(
    page_title="About",
    layout="wide"
)

st.title("ℹ️ About")

st.markdown("""
## FPL Analytics Platform

### Model
V11 Prediction Model

### Current Features

✅ Team Sheet

✅ Best XI Optimizer

✅ Transfer Command Center

✅ Smart Transfer Planner

✅ Fixture Runs

✅ Watchlist

✅ Team Insights

✅ Rankings

✅ Player Comparison

### Workflow

1. Run update_everything.py
2. Review Assistant page
3. Review Command Center
4. Confirm Team Sheet
5. Make transfers

### Model Performance

MAE: 1.00
""")