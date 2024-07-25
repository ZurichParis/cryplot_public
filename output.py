from dash import html


def output_content_list(
        info_pred, 
        log2_info_pred, 
        log2_info_price=None, 
        info_price=None
        ) -> list:
    output_content = [
    html.P(f"Actual BTC/USD: {info_price}"),
    html.P(f"Predicted BTC/USD: {info_pred}"),
    html.P(f"Log2 Actual BTC/USD: {log2_info_price}"),
    html.P(f"Log2 Predict BTC/USD: {log2_info_pred}")
    ]
    return output_content