# TallyX

A sleek, minimalist expense tracker and planner built to visualize financial outflow and simplify budget planning.

TallyX is a Django-powered web application that helps individuals and families track expenses, manage budgets, and gain clarity over their spending habits — all through a clean, no-frills interface.

## Features

- Track and categorize personal or family expenses
- Simplified budget planning workflow
- Lightweight, minimalist UI focused on clarity over clutter
- Built on Django's admin panel for quick data management
- SQLite database for easy local setup with no external dependencies

## Tech Stack

- **Backend:** Python, Django
- **Database:** SQLite (default, configurable)
- **Environment:** Python virtual environment (`venv`)

## Project Structure

```
TallyX/
├── family_budget/       # Django project (settings, URLs, WSGI/ASGI config)
├── budget_tracker/       # Core app handling expense/budget logic
├── manage.py
├── requirements.txt
└── .gitignore
```

## Getting Started

### Prerequisites

- Python 3.x installed on your system
- pip (Python package manager)

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/sanjay20051207/TallyX.git
   cd TallyX
   ```

2. **Create and activate a virtual environment**
   ```bash
   python -m venv env
   ```
   - On Windows (PowerShell):
     ```powershell
     .\env\Scripts\Activate.ps1
     ```
   - On macOS/Linux:
     ```bash
     source env/bin/activate
     ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Apply database migrations**
   ```bash
   python manage.py migrate
   ```

5. **Create an admin (superuser) account**
   ```bash
   python manage.py createsuperuser
   ```

6. **Run the development server**
   ```bash
   python manage.py runserver 0.0.0.0:8000
   ```

7. **Access the application**

   Open your browser and navigate to:
   ```
   http://127.0.0.1:8000/
   ```

   The Django admin panel is available at:
   ```
   http://127.0.0.1:8000/admin/
   ```

### Verifying the Server

You can confirm the server is running with:
```bash
curl http://127.0.0.1:8000/
```

## Configuration

Key settings are defined in `family_budget/settings.py`:

```python
DEBUG = True
ALLOWED_HOSTS = []
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'budget_tracker',
]
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}
```

> ⚠️ **Note:** `DEBUG = True` and an empty `ALLOWED_HOSTS` are suitable for local development only. Before deploying to production, set `DEBUG = False`, populate `ALLOWED_HOSTS` with your domain(s), and move sensitive values (like `SECRET_KEY`) into environment variables.

## Roadmap

- [ ] User authentication and multi-user support
- [ ] Expense categorization and tagging
- [ ] Visual dashboards (charts/graphs) for spending trends
- [ ] Monthly/annual budget goal tracking
- [ ] Export reports (CSV/PDF)
- [ ] REST API for mobile/front-end integration

## Contributing

Contributions are welcome. To contribute:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/your-feature`)
3. Commit your changes (`git commit -m "Add your feature"`)
4. Push to the branch (`git push origin feature/your-feature`)
5. Open a Pull Request

## License

This project currently has no license specified. Consider adding one (e.g., MIT, Apache 2.0) to clarify how others can use, modify, or distribute this code.

## Author

**Sanjay** — [@sanjay20051207](https://github.com/sanjay20051207)
