# AI-Powered Employee Task & Productivity Platform

A modern, scalable enterprise full-stack web application designed for companies to manage employees, tasks, attendance, and productivity using AI-assisted automation, real-time communication, and detailed analytics. 

## Features

- **Authentication System**: Secure JWT-based role-based access control (Admin, Manager, Employee).
- **Admin Dashboard**: Comprehensive overview of employees, tasks, productivity metrics, and AI predictive analytics.
- **Employee Dashboard**: Manage assigned tasks, track personal productivity, and view AI-generated suggestions.
- **Task Management**: Create, assign, and track tasks with priorities, statuses, and due dates.
- **Real-Time Communication**: WebSocket-powered team chat and real-time updates.
- **AI/ML Productivity Engine**: Built-in predictive models for employee productivity scoring and efficiency trends using Scikit-Learn.
- **Attendance Management**: Daily check-ins, check-outs, and attendance analytics.
- **Reporting System**: Automated PDF report generation using ReportLab.

## Tech Stack

- **Frontend**: React 19, Tailwind CSS v4, Framer Motion, Recharts, Vite
- **Backend**: Python 3.11, FastAPI, SQLAlchemy, WebSockets, PyJWT
- **Database**: PostgreSQL (Production/Docker), SQLite (Local Dev)
- **AI/ML**: Scikit-Learn, Pandas, NumPy
- **Deployment**: Docker, Docker Compose, Nginx

## Project Structure

```
.
├── backend/            # FastAPI Backend, ML models, and Database Migrations (Alembic)
├── frontend/           # React 19 + Tailwind CSS v4 Vite App
├── database/           # Database schema and initial seeds
├── docker/             # Docker configurations
├── docs/               # Architecture and project documentation
├── ml_models/          # Saved Scikit-Learn models and training data
├── docker-compose.yml  # Docker Compose orchestration
└── README.md           # This documentation
```

## Installation & Setup Guide (Local Development)

### Prerequisites
- Node.js (v18+)
- Python (3.10+)
- PostgreSQL (Optional for local, required for production)
- Docker & Docker Compose (Optional but recommended)

### 1. Backend Setup

```bash
cd backend

# Create and activate virtual environment
python -m venv venv
# On Windows
.\venv\Scripts\activate
# On Mac/Linux
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run migrations (if using SQLite, app.db will be created automatically)
alembic upgrade head

# Start the development server
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```
The backend will be available at `http://localhost:8000`. API docs are at `http://localhost:8000/docs`.

### 2. Frontend Setup

```bash
cd frontend

# Install dependencies
npm install

# Start development server
npm run dev
```
The frontend will be available at `http://localhost:5173`.

## Deployment Guide (Docker)

The easiest way to run the entire stack (PostgreSQL, Redis, Backend, Frontend with Nginx) is via Docker Compose.

```bash
# Build and start all services in detached mode
docker-compose up -d --build
```

### Services Started:
- **Frontend**: `http://localhost` (Port 80)
- **Backend API**: `http://localhost:8000` (Port 8000)
- **Database**: PostgreSQL on port 5432
- **Cache**: Redis on port 6379

To stop the services:
```bash
docker-compose down
```

## API Documentation

The backend exposes a fully documented REST API. When running the backend locally or via Docker, you can view the interactive Swagger documentation at:

**URL**: `http://localhost:8000/docs`

### Key Endpoints

- `POST /api/v1/auth/login` - Authenticate user and get JWT token
- `POST /api/v1/users/` - Create a new user/employee
- `GET /api/v1/tasks/` - List all tasks (filtered by user role)
- `POST /api/v1/tasks/` - Create a task
- `GET /api/v1/analytics/dashboard-stats` - Get aggregated dashboard statistics
- `POST /api/v1/analytics/predict-productivity` - AI prediction endpoint
- `GET /api/v1/reports/productivity-report` - Generate PDF report
- `WS /api/v1/ws/chat` - WebSocket endpoint for real-time team communication

## Code Quality & Architecture

- **Clean Architecture**: Backend follows a layered architecture (API routes -> Services/CRUD -> Database Models).
- **Security**: Password hashing with bcrypt, JWT token validation, CORS configuration.
- **UI/UX**: Modern glassmorphism UI with smooth Framer Motion animations and responsive layouts.

## Default Seeded Credentials

| Role | Email | Password | Description |
| :--- | :--- | :--- | :--- |
| **Admin** | `admin@example.com` | `password123` | Full administrator overview, analytics & management |
| **Manager** | `manager@example.com` | `password123` | Team task assignment and productivity monitoring |
| **Employee** | `employee@example.com` | `password123` | Employee task execution & attendance check-ins |
| **Employee** | `mehthab@gmail.com` | `12345678` | Personal task board and tracking |

## GitHub Actions & GitHub Pages Deployment

This repository includes an automated GitHub Actions CI/CD workflow (`.github/workflows/deploy.yml`) to build and deploy the React frontend directly to **GitHub Pages**.

### Enabling GitHub Pages in Repository Settings:
1. Navigate to your repository on GitHub: `https://github.com/MEHTHAB7/QUICK_TASK`
2. Click on **Settings** -> **Pages** (in the left sidebar under Code and automation).
3. Under **Build and deployment** -> **Source**, select **GitHub Actions**.
4. Push to the `main` branch or trigger the workflow manually from the **Actions** tab.
5. Once deployed, the frontend will be live at:
   `https://mehthab7.github.io/QUICK_TASK/`

### Connecting the Frontend to a Production Backend:
If hosting the FastAPI backend on a cloud provider (e.g. Render, Railway, Fly.io, or VPS):
1. In repository **Settings** -> **Secrets and variables** -> **Actions**:
   - Add variable/secret `VITE_API_BASE_URL` (e.g., `https://your-api.onrender.com/api/v1`)
   - Add variable/secret `VITE_WS_BASE_URL` (e.g., `wss://your-api.onrender.com/api/v1/ws/chat`)
2. The deployment workflow will automatically use these endpoints when building the application.
