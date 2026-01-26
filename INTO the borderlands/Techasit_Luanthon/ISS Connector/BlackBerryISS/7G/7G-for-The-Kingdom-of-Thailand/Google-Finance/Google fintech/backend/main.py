from broker.alpaca import sell_stock
from bank.scb import transfer_to_bank

if __name__ == "__main__":
    trade = sell_stock("AAPL", 1)
    print(trade)

    transfer = transfer_to_bank(5000, "1234567890", "SCB")
    print(transfer)