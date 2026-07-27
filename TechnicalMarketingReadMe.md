# PasswordFilter — Technical Marketing Summary

## One-Line Positioning

A Flask-based password hygiene service that checks passwords against a database of one million compromised credentials and suggests secure random alternatives.

## Target Users / Personas

- **Application developers** who need a reference implementation for password hygiene checks (banned passwords, minimum length, random generation) in their own Flask applications.
- **Security-conscious organizations** that want to prevent users from choosing commonly compromised passwords sourced from real breach data.
- **DevOps engineers** looking for a containerizable password validation service deployable via Docker or Heroku.

## Key Features (Grounded in Code)

- **Banned password checking**: Loads 1,000,000 commonly used passwords from a breach-derived list into a set and rejects any submitted password that appears in it (`passwordfilter/app.py`, `init()` function and `compromised` set).
- **Random password generation**: Generates random passwords using all printable ASCII characters with a configurable length (`passwordfilter/app.py`, `get_random_string()` using `string.printable`).
- **Minimum password length enforcement**: Enforces a minimum password length of 14 characters (`passwordfilter/app.py`, `Minuser_pwLen = 14`).
- **User CRUD operations**: Web interface for creating, viewing, and editing users stored in SQLite (`passwordfilter/app.py`, `/create`, `/<int:post_id>`, `/<int:id>/edit` routes).
- **Blueprint-based authentication**: Separate Flask app with user registration, login, logout, session management, and login-required decorator using Werkzeug password hashing (`auth.py`, `Blueprint` with `/auth` prefix).
- **SQLite database**: Persistent storage with a `users` table schema including user ID, password, and hashed password fields (`passwordfilter/schema.sql`).
- **Docker deployment**: Dockerfile using Python 3.6 base image with Gunicorn serving on port 8000 (`Dockerfile`, `passwordfilter/gunicorn_config.py`).
- **Heroku deployment helper**: Script that reads a Heroku app URL, sets the git remote, pushes to Heroku, and verifies deployment (`herokuize.py`).
- **Automated security scanning**: GitHub Actions workflow running Bandit security linter on every push and pull request (`/.github/workflows/`).
- **Gunicorn production configuration**: Configured with 2 workers, 4 threads, gthread worker class, and 30-second timeout (`passwordfilter/gunicorn_config.py`).

## Technical Differentiators

- **Real breach data**: Uses the SecLists 10-million-password-list (top 1M) sourced from actual hacked accounts, not synthetic or guessed common passwords.
- **Dual app architecture**: Includes both a standalone password filter app and a blueprint-based authentication app, demonstrating different integration approaches.
- **Container-ready**: Ships with a Dockerfile and Gunicorn configuration for immediate containerized deployment.
- **CI security scanning**: Integrated Bandit security scanning via GitHub Actions provides continuous security validation of the codebase.
- **14-character minimum**: Enforces a stronger minimum password length than the typical 8-character standard.

## Use Cases

- Adding password hygiene validation to a Flask web application's registration flow.
- Deploying a standalone password checking service in a microservices architecture.
- Learning Flask authentication patterns (blueprints, session management, password hashing) from a working example.
- Demonstrating Docker and Heroku deployment patterns for Flask applications.

## Benefits / Value Proposition

- Prevents users from choosing passwords that appear in known breach databases, directly reducing account compromise risk.
- Suggests strong random passwords that work well with password managers.
- Provides a complete, deployable reference implementation — from local development to Docker to Heroku.
- Automated security scanning ensures the codebase itself is checked for common Python security issues.

## Tech Stack

- **Web framework**: Flask 2.3+
- **Database**: SQLite
- **Password hashing**: Werkzeug (`generate_password_hash`, `check_password_hash`)
- **WSGI server**: Gunicorn 23.0 (gthread worker, 2 workers, 4 threads)
- **Containerization**: Docker (Python 3.6 base image)
- **Deployment**: Heroku (via `herokuize.py`)
- **Security scanning**: Bandit (via GitHub Actions)
- **Password data**: SecLists 10-million-password-list-top-1000000

## Known Limitations

- The standalone app (`passwordfilter/app.py`) stores passwords in plain text in SQLite — it is a demonstration app, not production-ready for password storage.
- The Dockerfile uses Python 3.6, which is end-of-life; should be updated to a supported Python version.
- The `SECRET_KEY` in the standalone app is randomly generated on each restart, which invalidates all sessions on restart.
- The banned password list (1M entries, ~8.5 MB) is loaded into memory as a set on each app startup.
- The `herokuize.py` script reads from a hardcoded file (`create.log`) and has limited error handling.
- No HTTPS enforcement or CSRF protection in the standalone app.
- Random password generation uses `random.choice` (not `secrets`), which is not cryptographically secure.
- The root-level `__init__.py` app uses a hardcoded `SECRET_KEY='dev'` in development mode.
