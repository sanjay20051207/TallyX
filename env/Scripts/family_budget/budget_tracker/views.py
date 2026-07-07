# Create your views here.
from django.shortcuts import render, redirect
from django.contrib import messages
from . import data_manager

# Middleware simulation decorators
def login_required_custom(view_func):
    def wrapper(request, *args, **kwargs):
        if 'username' not in request.session:
            messages.warning(request, "Please log in to access this page.")
            return redirect('login')
        return view_func(request, *args, **kwargs)
    return wrapper

def login_view(request):
    if request.method == 'POST':
        u = request.POST.get('username')
        p = request.POST.get('password')
        user = data_manager.authenticate_user(u, p)
        if user:
            request.session['username'] = u
            request.session['primary_name'] = user['primary_name']
            request.session['companion_name'] = user['companion_name']
            messages.success(request, f"Welcome back, {user['primary_name']} & {user['companion_name']}!")
            return redirect('dashboard')
        else:
            messages.error(request, "Invalid username or password.")
    return render(request, 'login.html')

def register_view(request):
    if request.method == 'POST':
        u = request.POST.get('username')
        p = request.POST.get('password')
        p_name = request.POST.get('primary_name')
        c_name = request.POST.get('companion_name')
        
        if data_manager.register_user(u, p, p_name, c_name):
            messages.success(request, "Account configured successfully. Please log in.")
            return redirect('login')
        else:
            messages.error(request, "Username is already taken.")
    return render(request, 'register.html')

def logout_view(request):
    request.session.flush()
    messages.info(request, "Logged out successfully.")
    return redirect('login')

@login_required_custom
def dashboard_view(request):
    username = request.session['username']
    budget_data = data_manager.get_user_budget(username)
    expenses = data_manager.get_expenses(username)
    
    # Aggregations
    total_spent = sum(exp['amount'] for exp in expenses)
    remaining_budget = budget_data.get('total_limit', 0.0) - total_spent
    
    category_totals = {cat: 0.0 for cat in budget_data.get('limits', {})}
    for exp in expenses:
        cat = exp['category']
        if cat in category_totals:
            category_totals[cat] += exp['amount']
        else:
            category_totals[cat] = exp['amount']
            
    # Structure progress bars
    categories_progress = []
    for cat, cap in budget_data.get('limits', {}).items():
        spent = category_totals.get(cat, 0.0)
        percentage = (spent / cap * 100) if cap > 0 else 0
        categories_progress.append({
            'name': cat,
            'limit': cap,
            'spent': spent,
            'percentage': min(round(percentage, 1), 100),
            'over_limit': spent > cap
        })

    context = {
        'budget': budget_data,
        'expenses': sorted(expenses, key=lambda x: x['date'], reverse=True),
        'total_spent': total_spent,
        'remaining_budget': remaining_budget,
        'categories_progress': categories_progress,
        'username': username,
        'primary_name': request.session.get('primary_name'),
        'companion_name': request.session.get('companion_name'),
    }
    return render(request, 'dashboard.html', context)

@login_required_custom
def set_budget_view(request):
    username = request.session['username']
    budget_data = data_manager.get_user_budget(username)
    
    if request.method == 'POST':
        salary = request.POST.get('salary')
        total_limit = request.POST.get('total_limit')
        limits = {
            "Medical Expenses": request.POST.get('limit_medical'),
            "Future Savings": request.POST.get('limit_savings'),
            "Groceries & Food": request.POST.get('limit_groceries'),
            "Utilities & Bills": request.POST.get('limit_utilities'),
            "Entertainment": request.POST.get('limit_entertainment'),
            "Others": request.POST.get('limit_others'),
        }
        data_manager.update_user_budget(username, salary, total_limit, limits)
        messages.success(request, "Budget limits updated successfully.")
        return redirect('dashboard')

    budget_view_data = budget_data.copy() if isinstance(budget_data, dict) else {}
    limit_aliases = budget_view_data.get('limits', {}).copy() if isinstance(budget_view_data.get('limits'), dict) else {}
    limit_aliases.update({
        "Medical_Expenses": limit_aliases.get("Medical Expenses", 0.0),
        "Future_Savings": limit_aliases.get("Future Savings", 0.0),
        "Groceries_Food": limit_aliases.get("Groceries & Food", 0.0),
        "Utilities_Bills": limit_aliases.get("Utilities & Bills", 0.0),
    })
    budget_view_data['limits'] = limit_aliases
    return render(request, 'set_budget.html', {'budget': budget_view_data})

@login_required_custom
def add_expense_view(request):
    username = request.session['username']
    budget_data = data_manager.get_user_budget(username)
    categories = budget_data.get('limits', {}).keys()
    spenders = [request.session.get('primary_name'), request.session.get('companion_name')]
    
    if request.method == 'POST':
        amount = request.POST.get('amount')
        category = request.POST.get('category')
        date = request.POST.get('date')
        spender = request.POST.get('spender')
        description = request.POST.get('description')
        
        data_manager.add_expense(username, amount, category, date, spender, description)
        messages.success(request, "Expense added successfully.")
        return redirect('dashboard')
        
    return render(request, 'expense_form.html', {
        'categories': categories, 
        'spenders': spenders, 
        'action': 'Add'
    })

@login_required_custom
def edit_expense_view(request, expense_id):
    username = request.session['username']
    expense = data_manager.get_expense_by_id(username, expense_id)
    if not expense:
        messages.error(request, "Expense record not found.")
        return redirect('dashboard')
        
    budget_data = data_manager.get_user_budget(username)
    categories = budget_data.get('limits', {}).keys()
    spenders = [request.session.get('primary_name'), request.session.get('companion_name')]
    
    if request.method == 'POST':
        amount = request.POST.get('amount')
        category = request.POST.get('category')
        date = request.POST.get('date')
        spender = request.POST.get('spender')
        description = request.POST.get('description')
        
        data_manager.update_expense(username, expense_id, amount, category, date, spender, description)
        messages.success(request, "Expense updated successfully.")
        return redirect('dashboard')
        
    return render(request, 'expense_form.html', {
        'expense': expense,
        'categories': categories,
        'spenders': spenders,
        'action': 'Edit'
    })

@login_required_custom
def delete_expense_view(request, expense_id):
    username = request.session['username']
    data_manager.delete_expense(username, expense_id)
    messages.success(request, "Expense deleted successfully.")
    return redirect('dashboard')