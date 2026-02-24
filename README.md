# Zodiac Persona

**Professional grade Vedic Astrology Computation Library for Python**

Zodiac Persona is a high-precision, calculating-intensive Vedic Astrology API built on accurate astronomical planetary physics. Unlike basic lookup-table astrology calculators, this tool leverages industrial-grade NASA-standard calculation libraries (`skyfield`) to compute mathematically perfect Sun, Moon, and Ascendant signs depending on exact moment and radius of birth!

This repository contains the **Backend API** (using FastAPI). It handles complex mathematics and serves the frontend SPA for an accurate personal reading.

> **Note:** This backend is meant to serve the separate Zodiac Persona Frontend React application on port `8000`.

---

## Features

- **Hyper-Accurate Precision:** Uses Python's `skyfield` physics engine and authentic sidereal computations.
- **RESTful API Endpoint:** Handles localized timezones, precise global coordinates, and exact moment of calculation natively.
- **Astronomy Data Localized:** Leverages native JPL DE421 ephemeris data (`hip_main.dat`).
- **Production Ready Daemon:** Integrated to run over PM2 through a native python reverse-process wrapper for extreme uptime.

---

## Directory Structure

```plaintext
zodiac_persona_backend/
│
├── zodiac_persona/                # Core calculation logic directory
│   ├── core/                      # Astrological constants, ephemeris data
│   ├── skyfield_adapter.py        # Interface tying core astronomy math to logic
│   └── main.py                    # Root calculator wrapping engine functions
├── api.py                         # FastAPI webserver that hosts REST API endpoints
├── .github/workflows/
│   └── deploy.yml                 # CI/CD instructions to ZIP, push, and run back server
├── requirements.txt               # Required PIP packages (fastapi, uvicorn, skyfield)
└── hip_main.dat                   # Heavily compiled star map ephemeris required for astronomy
```

---

## Running the Project Locally (Localhost)

This application serves as the computation layer. Ensure you have **Python 3.9+** installed locally before proceeding.

1. Activate a Python virtual environment (Highly Recommended):
   ```bash
   # On Windows
   python -m venv venv
   .\venv\Scripts\activate

   # On Mac/Linux
   python3 -m venv venv
   source venv/bin/activate
   ```

2. Install the required planetary libraries and backend dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Start the interactive Uvicorn development server:
   ```bash
   uvicorn api:app --reload --port 8000
   ```

*Your API is now actively listening for cosmos requests at `http://localhost:8000`. You can now start up your separate React frontend server.*

---

## Automated Deployments (GitHub Actions for EC2)

This repository includes a CI/CD GitHub Actions pipeline (`.github/workflows/deploy.yml`) to automatically push the computation code onto an AWS EC2 or standard VPS server.

> **Important:** Create the following GitHub Secrets in your backend repository under Settings -> Secrets and Variables -> Actions:
> 
> *   `EC2_HOST`: The Public IP or DNS of your target EC2 machine
> *   `EC2_USER`: The SSH user for your server (e.g., `ubuntu` or `ec2-user`)
> *   `SSH_KEY`: The raw private SSH key contents (`.pem` format) authorized to connect to your server.

**How the Pipeline Works:**

1. Compiles the API files (excluding `.git`, logs, tests, etc.) into a tight zipper.
2. Securely SCPs the folder into your EC2's `/tmp/` folder.
3. SSHs into the machine, creates `/var/www/backend`, and unzips the files.
4. Manages the `venv` virtual environment on the server side and auto-installs/syncs requirements via `pip`.
5. Connects Node `pm2` to the exact API interface through Python for ultra-reliable background running (`pm2 start`).
6. Cleans up memory space immediately.
