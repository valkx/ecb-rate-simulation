import requests
import pandas as pd
import numpy as np
import json

# Constants
TARGET_INFLATION = 2.0  # ECB target
EQUILIBRIUM_RATE = 1.0  # Fixed estimate (update periodically)

# ECB Data URLs (Since 2000)
# https://data-api.ecb.europa.eu/service/data/[dataflow]/[series]?startPeriod=[start_date]&endPeriod=[end_date]
INFLATION_URL = "https://data-api.ecb.europa.eu/service/data/ICP/M.U2.N.000000.4.ANR?startPeriod=2000-01&endPeriod=2024-01"
GDP_URL = "https://data-api.ecb.europa.eu/service/data/MNA/Q.Y.I9.W2.S1.S1.B.B1GQ._Z._Z._Z.EUR.LR.N?startPeriod=2000&endPeriod=2024"
POT_GDP_URL = "https://data-api.ecb.europa.eu/service/data/MNA/Q.Y.I9.W2.S1.S1.B.B1GQ._Z._Z._Z.EUR.LR.N?startPeriod=2000&endPeriod=2024"
ECB_RATE_URL = "https://data-api.ecb.europa.eu/service/data/FM/B.U2.EUR.4F.KR.MRR_FR.LEV?startPeriod=2000-01&endPeriod=2024-01"



def fetch_ecb_data(url, default_value, years=24, monthly=False):
    """Fetch data from ECB SDW and handle SDMX-JSON response."""
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36",
        "Accept": "application/vnd.sdmx.data+json;version=1.0.0-wd"
    }
    
    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()

        # Parse the SDMX-JSON response
        data = response.json()
        
        # Extract the 'observations' section from the SDMX response
        series = data.get("dataSets", [{}])[0].get("series", {})
        observations = next(iter(series.values()), {}).get("observations", {})

        # Extracting values from the observations
        values = [float(obs[0]) for obs in observations.values()]
        
        if not values:
            raise ValueError("No data extracted.")
        
        # Interpolation for monthly data if needed
        if monthly and len(values) < years * 12:
            values = np.interp(np.linspace(0, len(values)-1, years*12), range(len(values)), values)
        
        return values
    except requests.exceptions.HTTPError as e:
        if e.response.status_code == 404:
            print(f"404 Error: Data not found for the URL: {url}. Returning default values.")
        else:
            print(f"HTTP Error: {e}")
    except Exception as e:
        print(f"Error fetching data from {url}: {e}")
    
    # Return default value in case of error
    return [default_value] * (years * 12 if monthly else years)


def fetch_inflation():
    """Fetch HICP inflation rate since 2000."""
    return fetch_ecb_data(INFLATION_URL, 2.5, years=24, monthly=True)


def fetch_output_gap():
    """Fetch GDP and potential GDP, then calculate monthly interpolated output gap."""
    gdp_values = fetch_ecb_data(GDP_URL, 100, years=24, monthly=False)
    pot_gdp_values = fetch_ecb_data(POT_GDP_URL, 102, years=24, monthly=False)
    
    # Interpolate GDP and Potential GDP to monthly values using rolling averages
    gdp_monthly = pd.Series(gdp_values).interpolate(method='linear').rolling(window=12, min_periods=1).mean().values
    pot_gdp_monthly = pd.Series(pot_gdp_values).interpolate(method='linear').rolling(window=12, min_periods=1).mean().values
    
    return ((gdp_monthly - pot_gdp_monthly) / pot_gdp_monthly) * 100


def fetch_ecb_rate():
    """Fetch official ECB interest rate since 2000."""
    return fetch_ecb_data(ECB_RATE_URL, 2.0, years=24, monthly=True)


def calculate_interest_rate(equilibrium_rate, inflation, target_inflation, output_gap):
    """Calculate interest rate using the modified Taylor Rule."""
    return equilibrium_rate + 1.5 * (inflation - target_inflation) + 0.5 * output_gap


def simulate_interest_rates():
    """Simulate interest rates since 2000 using ECB data."""
    inflations = fetch_inflation()
    output_gaps = fetch_output_gap()
    ecb_rates = fetch_ecb_rate()
    
    rates = [calculate_interest_rate(EQUILIBRIUM_RATE, infl, TARGET_INFLATION, gap) for infl, gap in zip(inflations, output_gaps)]
    
    return rates, inflations, output_gaps, ecb_rates


def plot_results(rates, inflations, output_gaps, ecb_rates):
    """Generate and display the interactive plot for data since 2000."""
    import plotly.graph_objects as go
    from plotly.subplots import make_subplots
    
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
    
    fig.show()


if __name__ == "__main__":
    rates, inflations, output_gaps, ecb_rates = simulate_interest_rates()
    plot_results(rates, inflations, output_gaps, ecb_rates)
