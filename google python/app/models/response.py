from pydantic import BaseModel
class StockResponse(BaseModel): symbol:str; price:str|None
