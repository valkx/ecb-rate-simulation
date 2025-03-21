import streamlit as st
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from taylor_rule_automated import simulate_interest_rates, plot_results
import pandas as pd

# Your code here (simulated rates, inflation, etc.)

def plot_results(rates, inflations, output_gaps, ecb_rates):
    fig = make_subplots(rows=3, cols=1, subplot_titles=("Simulated Interest Rate vs ECB Rate", "Inflation", "Output Gap"))
    time = pd.date_range(start="2000-01", periods=len(rates), freq='ME')
    
    fig.add_trace(go.Scatter(x=time, y=rates, mode='lines', name='Simulated Interest Rate'), row=1, col=1)
    fig.add_trace(go.Scatter(x=time, y=ecb_rates, mode='lines', name='ECB Official Rate', line=dict(dash='dot')), row=1, col=1)
    fig.add_trace(go.Scatter(x=time, y=inflations, mode='lines', name='Inflation'), row=2, col=1)
    fig.add_trace(go.Scatter(x=time, y=output_gaps, mode='lines', name='Output Gap'), row=3, col=1)
    
    fig.update_layout(title_text="ECB Interest Rate Simulation (Since 2000)", height=800, showlegend=True, template="plotly_white")
    fig.update_xaxes(title_text="Time", row=3, col=1)
    fig.update_yaxes(title_text="Interest Rate (%)", row=1, col=1)
    fig.update_yaxes(title_text="Inflation (%)", row=2, col=1)
    fig.update_yaxes(title_text="Output Gap (%)", row=3, col=1)
    
    return fig

# Simulate results (use your actual simulation code)
rates, inflations, output_gaps, ecb_rates = simulate_interest_rates()

# Display results in the app
st.title("ECB Interest Rate Simulation")
st.plotly_chart(plot_results(rates, inflations, output_gaps, ecb_rates))
