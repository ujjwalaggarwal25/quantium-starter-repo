import pandas as pd
from dash import Dash, dcc, html, Input, Output
import plotly.express as px

# ----------------------------
# Load data
# ----------------------------
df = pd.read_csv("output/processed_sales.csv")  # <-- update filename if needed
df["Date"] = pd.to_datetime(df["Date"])

# ----------------------------
# Initialize app
# ----------------------------
app = Dash(__name__)
app.title = "Pink Morsels Sales Visualiser"

# ----------------------------
# Layout
# ----------------------------
app.layout = html.Div(
    className="app-container",
    children=[
        html.H1("Pink Morsels Sales Dashboard"),

        dcc.RadioItems(
            id="region-filter",
            options=[
                {"label": "All", "value": "all"},
                {"label": "North", "value": "north"},
                {"label": "East", "value": "east"},
                {"label": "South", "value": "south"},
                {"label": "West", "value": "west"},
            ],
            value="all",
            inline=True,
            className="radio-group"
        ),

        dcc.Graph(
            id="sales-line-chart"
        )
    ]
)

# ----------------------------
# Callback
# ----------------------------
@app.callback(
    Output("sales-line-chart", "figure"),
    Input("region-filter", "value")
)
def update_chart(selected_region):
    if selected_region == "all":
        filtered_df = df
    else:
        filtered_df = df[df["Region"].str.lower() == selected_region]

    fig = px.line(
        filtered_df,
        x="Date",
        y="Sales",
        color="Region",
        title="Pink Morsels Sales Over Time"
    )

    fig.update_layout(
        template="plotly_white",
        margin=dict(l=40, r=40, t=60, b=40)
    )

    return fig

# ----------------------------
# Run server
# ----------------------------
if __name__ == "__main__":
    app.run(debug=True)
