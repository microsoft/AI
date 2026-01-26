def transfer_to_bank(amount, account_number, bank_code):
    return {
        "bank": "SCB Sandbox",
        "amount": amount,
        "to_account": account_number,
        "status": "transfer_success"
    }