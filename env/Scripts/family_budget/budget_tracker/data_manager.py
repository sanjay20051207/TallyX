import os
import json
import uuid
import hashlib

DATA_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'budget_store.json')

def init_db():
    if not os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'w') as f:
            json.dump({
                "users": {},       # username -> {password_hash, primary_name, companion_name}
                "budgets": {},     # username -> {salary, total_limit, limits: {category: limit}}
                "expenses": {}     # username -> [list of expenses]
            }, f, indent=4)

def read_db():
    init_db()
    with open(DATA_FILE, 'r') as f:
        return json.load(f)

def write_db(data):
    with open(DATA_FILE, 'w') as f:
        json.dump(data, f, indent=4)

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# Auth Helpers
def register_user(username, password, primary_name, companion_name):
    db = read_db()
    if username in db["users"]:
        return False
    
    db["users"][username] = {
        "password": hash_password(password),
        "primary_name": primary_name,
        "companion_name": companion_name
    }
    # Initialize default budget values
    db["budgets"][username] = {
        "salary": 0.0,
        "total_limit": 0.0,
        "limits": {
            "Medical Expenses": 0.0,
            "Future Savings": 0.0,
            "Groceries & Food": 0.0,
            "Utilities & Bills": 0.0,
            "Entertainment": 0.0,
            "Others": 0.0
        }
    }
    db["expenses"][username] = []
    write_db(db)
    return True

def authenticate_user(username, password):
    db = read_db()
    user = db["users"].get(username)
    if user and user["password"] == hash_password(password):
        return user
    return None

# Budget Helpers
def get_user_budget(username):
    db = read_db()
    return db["budgets"].get(username, {})

def update_user_budget(username, salary, total_limit, limits):
    db = read_db()
    if username in db["budgets"]:
        db["budgets"][username]["salary"] = float(salary or 0)
        db["budgets"][username]["total_limit"] = float(total_limit or 0)
        for cat, limit in limits.items():
            db["budgets"][username]["limits"][cat] = float(limit or 0)
        write_db(db)

# Expense CRUD Helpers
def get_expenses(username):
    db = read_db()
    return db["expenses"].get(username, [])

def add_expense(username, amount, category, date, spender, description):
    db = read_db()
    expense_id = str(uuid.uuid4())
    expense = {
        "id": expense_id,
        "amount": float(amount),
        "category": category,
        "date": date,
        "spender": spender,
        "description": description
    }
    db["expenses"][username].append(expense)
    write_db(db)
    return expense

def get_expense_by_id(username, expense_id):
    expenses = get_expenses(username)
    for exp in expenses:
        if exp["id"] == expense_id:
            return exp
    return None

def update_expense(username, expense_id, amount, category, date, spender, description):
    db = read_db()
    expenses = db["expenses"].get(username, [])
    for exp in expenses:
        if exp["id"] == expense_id:
            exp["amount"] = float(amount)
            exp["category"] = category
            exp["date"] = date
            exp["spender"] = spender
            exp["description"] = description
            break
    write_db(db)

def delete_expense(username, expense_id):
    db = read_db()
    expenses = db["expenses"].get(username, [])
    db["expenses"][username] = [exp for exp in expenses if exp["id"] != expense_id]
    write_db(db)