import pandas as pd
import plotly.graph_objects as go

def plotter(df: pd.DataFrame, x: str, y: list[str], title: str):
    fig = go.Figure()

    for i, y_col in enumerate(y):
        fig.add_trace(go.Scatter(
            x=df[x],
            y=df[y_col],
            mode='lines',
            name=y_col,
            hoverinfo='none', 
            line=dict(width=2)
            ))
    
    fig.update_layout(
        title=title,
        showlegend=False,
        hovermode='x',
        template='plotly_white',
        xaxis=dict(tickformat='%Y-%m-%d')
    )

    fig.update_yaxes(showspikes=True, spikemode='across', spikesnap='cursor', spikethickness=1)
    fig.update_xaxes(showspikes=True, spikemode='across', spikesnap='cursor', spikethickness=1)

    return fig
