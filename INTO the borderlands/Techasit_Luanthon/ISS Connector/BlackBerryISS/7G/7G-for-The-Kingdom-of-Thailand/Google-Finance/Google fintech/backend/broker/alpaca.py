def sell_stock(symbol, qty):
    return {
        "broker": "Alpaca (Sandbox)",
        "action": "SELL",
        "symbol": symbol,
        "quantity": qty,
        "status": "success"
    }