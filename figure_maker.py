import pandas as pd
import plotly.graph_objects as go

def create_figure(df: pd.DataFrame, x_name: str, y_names: list, title: str):
    # Create the figure using graph_objects
    fig = go.Figure()

    # Add first line
    fig.add_trace(go.Scatter(
        x=df[x_name],
        y=df[y_names[0]],
        mode='lines',
        name=y_names[0],
        hoverinfo='none',  # No default hover information
        hovertemplate='$%{y:.2f}<extra></extra>',  # Custom hover template with only y-value
        hoverlabel=dict(
            bgcolor='rgba(255, 255, 255, 0.01)', 
            font=dict(color='blue')
        )
    ))

    # Add second line
    fig.add_trace(go.Scatter(
        x=df[x_name],
        y=df[y_names[1]],
        mode='lines',
        name=y_names[1],
        hoverinfo='none',  # No default hover information
        hovertemplate='$%{y:.2f}<extra></extra>',  # Custom hover template with only y-value
        hoverlabel=dict(
            bgcolor='rgba(255, 255, 255, 0.01)',  
            font=dict(color='red')
        )
    ))

    # Update layout for the figure
    fig.update_layout(
        title=title,
        hovermode='x',  # Unified hover mode
        template='plotly_white',  # Dark theme
        showlegend=False
    )

    fig.update_yaxes(showspikes=True, spikemode='across', spikesnap='cursor', spikethickness=1)
    fig.update_xaxes(showspikes=True, spikemode='across', spikesnap='cursor', spikethickness=1)

    return fig