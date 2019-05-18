from .primitives import Str, Int, Enum
from time import time

LedgerAction = Enum(["credit", "debit"])

now = lambda: int(round(time() * 1000)),

CreditBalance = {
    "ledger_balance": Int(100, 10000),
    "hold_balance": Int(100, 10000),
    "available_balance": Int(900, 10000),
    "soonest_expiry": {
        "amount": Int(100, 10000),
        "date": now,
    }
}

CreditBundle = {
    "trandsaction_id": Str(),
    "credit_transaction_id": Str(),
    "expired_at": now,
    "amount": Str(pattern=r"[0-9]{1-3}"),
    "bundle_price": Int(lower=10, upper=100),
    "price_currency": "coin",
    "referrals": {
        "salesperson": Str(),
        "quest_id": Str(),
    }
}

CreditTransaction = {
    "agent_number": Str(),
    "ledget_action": LedgerAction,
    "balance": Int(lower=100, upper=1000),
    "hold": Int(lower=-100, upper=100),
    "meta_data": {
        "notes": Str(),
    },
    "description": Str(),
    "comment": Str(),
    "references": {
        "credit_package_id": Str(pattern=r"[a-z][1-9]{3}"),
        "campaign_id": Str(pattern=r"[a-z][1-9]{3}"),
        "credit_bundle_id": Str(),
        "transaction_id": Str(),
        "invoice_id": Str(),
    }
}

CreditLedger = {
    "ledger_action": LedgerAction,
    "balance": Int(lower=100, upper=1000),
    "hold": Int(lower=-100, upper=100),
    "credit_transaction_id": Str(),
    "credit_bundle_id": Str(),
    "agent_number": Str(),
}

CreditTransfer = {
    "from_agent_number": Str(),
    "to_agent_number": Str(),
    "transfer_from_credit_transaction_id": Str(),
    "transfer_to_credit_transaction_id": Str(),
    "status": Enum(["incomplete", "complete", "error"])
}

CreditResult = {
    "result": "success",
    "credit_transaction": CreditTransaction,
}
