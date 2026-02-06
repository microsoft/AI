from fastapi import FastAPI
from app.finance import sheets_client, alphavantage
app=FastAPI()
@app.get('/')
def root(): return {'status':'ok'}
@app.get('/finance/google/{symbol}')
def g(symbol:str): return sheets_client.get_stock_price(symbol)
@app.get('/finance/api/{symbol}')
def a(symbol:str): return alphavantage.get_stock_price(symbol)
