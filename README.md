# PasswordFilter

## "You should probably change your password"

A Flask web application that implements password hygiene as a service — checking passwords against a database of known compromised credentials and suggesting secure random passwords.

## Overview

PasswordFilter provides a web interface for password hygiene:
- **Banned password checking**: Validates submitted passwords against a list of 1,000,000 most commonly used passwords (sourced from hacked accounts)
- **Password suggestions**: Generates random passwords using Python's `string.printable` character set
- **User management**: Register, view, and edit users with SQLite storage
- **Minimum length enforcement**: Requires passwords of at least 14 characters

The project includes two Flask applications:
1. **Root-level app** (`__init__.py`, `auth.py`, `db.py`) — A Flask blueprint-based app with user registration, login, logout, and session management using Werkzeug password hashing
2. **passwordfilter/app.py** — A standalone Flask app with password banning, random password generation, and CRUD user management

## Prerequisites

- Python 3.6+
- Flask and dependencies (see `passwordfilter/requirements.txt`)

## Setup

### Local Development

```bash
# Clone the repository
git clone https://github.com/biofool/PasswordFilter.git
cd PasswordFilter

# Install dependencies
pip install -r passwordfilter/requirements.txt

# Initialize the database
cd passwordfilter
python init_db.py
cd ..

# Run the standalone password filter app
cd passwordfilter
python app.py
```

### Docker

```bash
docker build -t passwordfilter .
docker run -p 8000:8000 passwordfilter
```

The Docker image runs the app via Gunicorn on port 8000.

### Heroku Deployment

```bash
python herokuize.py
```

The `herokuize.py` script reads a Heroku app URL from `create.log`, sets the git remote, pushes to Heroku, and verifies the deployment.

## How to Run

### Standalone Password Filter App

```bash
cd passwordfilter
export FLASK_APP=app.py
export FLASK_ENV=development
flask run
```

Navigate to `http://127.0.0.1:5000/` to access the web interface.

### Blueprint-based Auth App

```bash
export FLASK_APP=__init__.py
flask --app __init__ init-db
flask --app __init__ run
```

### Docker

```bash
docker build -t passwordfilter .
docker run -p 8000:8000 passwordfilter
```

Navigate to `http://localhost:8000/` to access the app (served via Gunicorn).

## Project Structure

```
PasswordFilter/
├── __init__.py                          # Flask app factory (blueprint-based app)
├── auth.py                              # Auth blueprint: register, login, logout
├── db.py                                # SQLite database helpers (blueprint app)
├── herokuize.py                         # Heroku deployment helper script
├── Dockerfile                           # Docker container definition (Python 3.6, Gunicorn)
├── 10-million-password-list-top-1000000.txt  # Banned password list (1M entries)
├── .github/workflows/                   # GitHub Actions: Bandit security scan
├── passwordfilter/
│   ├── app.py                           # Standalone Flask app: password filtering & CRUD
│   ├── wsgi.py                          # WSGI entry point for Gunicorn
│   ├── gunicorn_config.py               # Gunicorn configuration (2 workers, 4 threads)
│   ├── init_db.py                       # Database initialization script
│   ├── schema.sql                       # SQLite schema (users table)
│   ├── requirements.txt                 # Python dependencies
│   ├── templates/                       # HTML templates (base, index, create, post)
│   ├── static/                          # Static assets (CSS)
│   └── bin/                             # Virtual environment binaries
```

## Security

- The project includes a GitHub Actions workflow running [Bandit](https://github.com/PyCQA/bandit) security scans on every push and pull request to main.
- Passwords in the blueprint-based app are hashed using `werkzeug.security.generate_password_hash`.
- The standalone app stores passwords in plain text in SQLite (for demonstration purposes).
- The banned password list is sourced from the SecLists repository's common credentials (10-million-password-list-top-1000000).

## Notes

- The minimum password length is set to 14 characters (`Minuser_pwLen = 14` in `passwordfilter/app.py`).
- Random password suggestions use `string.printable` (all ASCII printable characters).
- The `SECRET_KEY` in the standalone app is randomly generated on each startup.
- The Dockerfile uses Python 3.6 as the base image.
