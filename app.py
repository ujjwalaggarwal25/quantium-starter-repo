import pandas as pd
import dash
from dash import dcc, html
import plotly.express as px

# Load data
df = pd.read_csv("output/processed_sales.csv")
df["Date"] = pd.to_datetime(df["Date"])
df = df.sort_values("Date")

# Create line chart
fig = px.line(
    df,
    x="Date",
    y="Sales",
    title="Pink Morsel Sales Over Time"
)

fig.update_layout(
    xaxis_title="Date",
    yaxis_title="Total Sales"
)

# Initialize Dash app
app = dash.Dash(__name__)

app.layout = html.Div([
    html.H1("Impact of Pink Morsel Price Increase on Sales"),
    dcc.Graph(figure=fig)
])

if __name__ == "__main__":
    app.run(debug=True)
