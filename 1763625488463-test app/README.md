# Flask on AWS Elastic Beanstalk

Production-ready starter template for deploying a Flask + Bootstrap dashboard
backed by an Amazon RDS MySQL database on AWS Elastic Beanstalk.

## Getting Started

1. Create and activate a Python 3.11 virtual environment.
2. Install dependencies with `pip install -r requirements.txt`.
3. Export database environment variables (`DB_HOST`, `DB_USER`, `DB_PASS`, `DB_NAME`, optional `DB_PORT`).
4. Run the app locally with `python application.py`.

A `/health` endpoint is included for load balancer checks.

## Architecture Overview

- **Flask** application factory in `app/__init__.py` keeps the project modular and
	Beanstalk-friendly.
- **SQLAlchemy** models live in `app/models.py` (`User` and `InventoryItem`).
- **Routes** are centralized in `app/routes.py`.
- **Templates** (`base.html`, `dashboard.html`) leverage Bootstrap 5 via CDN.
- **MySQL Connectivity** uses PyMySQL so no extra system packages are needed on
	Amazon Linux.

## Dashboard Features

- Inventory grid renders all `InventoryItem` rows with quantity and price.
- Inline form for adding new records (name, quantity, price).
- Per-row Delete buttons submit POST requests to remove items.
- Flash messages surface validation errors and success notifications.

## Installing the EB CLI (automated scripts)

If you don't have the Elastic Beanstalk CLI installed on Windows, the repo
contains two helper scripts you can run from the project root to install it for
the current user.

- PowerShell (recommended):

	Run in PowerShell:

	```powershell
	.\scripts\install_eb.ps1
	# Optionally add the Scripts folder to your user PATH permanently:
	.\scripts\install_eb.ps1 -AddUserPath
	```

- Command Prompt (cmd.exe):

	Run in cmd.exe:

	```cmd
	scripts\install_eb.cmd
	```

After the script finishes verify the installation with:

```cmd
eb --version
```

If `eb` is still not found, add the printed Scripts folder (e.g. `C:\Users\<you>\AppData\Roaming\Python\Python3x\Scripts`) to your User PATH and reopen the shell.

## AWS Elastic Beanstalk Deployment Checklist

- **Configure environment variables** – In the Elastic Beanstalk console, set the following under Configuration → Software:
	- `DB_HOST=cloudprojectdb.cg3yo8ao4rxa.us-east-1.rds.amazonaws.com`
	- `DB_USER=admin`
	- `DB_PASS=Admin123`
	- `DB_NAME=cld_prj_db`
	- `DB_PORT=3306` (optional if you kept the default)
	Treat these as secrets; rotate them and avoid committing them to source control.
- **Provision Amazon RDS** – Create the MySQL instance (matching the hostname above), configure security groups so the Elastic Beanstalk instances can reach the database, and enforce SSL if required by your compliance posture.
- **Run database migrations** – After deployment (or via `eb ssh`/CI), install Flask-Migrate or your migration tool of choice and run migrations before serving real traffic.
