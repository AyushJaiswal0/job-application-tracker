# Job Application Tracker

A full-stack web application for managing and tracking job applications.

The application provides user authentication, application management, search and filtering, and a dashboard with application statistics.

## Features

- User registration and login
- Password hashing using bcrypt
- JWT-based authentication
- User-specific application management
- Create, view, update, and delete applications
- Search applications by company or job title
- Filter applications by status
- Dashboard with application statistics
- RESTful API using FastAPI
- SQLite database using SQLAlchemy
- Responsive frontend
- Protected API endpoints

## Tech Stack

### Backend

- Python
- FastAPI
- SQLAlchemy
- SQLite
- Pydantic
- JWT
- Passlib
- bcrypt

### Frontend

- HTML
- CSS
- JavaScript

### Tools

- Git
- GitHub
- VS Code

## Application Architecture

```text
Browser
   │
   ▼
HTML / CSS / JavaScript
   │
   │ HTTP Requests
   ▼
FastAPI Backend
   │
   ├── Authentication
   │     ├── Registration
   │     ├── Password Hashing
   │     └── JWT Authentication
   │
   ├── Application Management
   │     ├── Create
   │     ├── Read
   │     ├── Update
   │     └── Delete
   │
   ├── Search & Filtering
   │
   └── Dashboard Statistics
   │
   ▼
SQLAlchemy
   │
   ▼
SQLite Database
```

## Project Structure

```text
job-application-tracker/
│
├── backend/
│   ├── main.py
│   ├── database.py
│   ├── models.py
│   ├── security.py
│   ├── auth.py
│   └── requirements.txt
│
├── frontend/
│   ├── dashboard.html
│   ├── login.html
│   ├── register.html
│   └── style.css
│
├── database/
│
├── .gitignore
└── README.md
```

> `.env`, the virtual environment, and the SQLite database are excluded from Git using `.gitignore`.

## Authentication

The application uses JWT-based authentication.

### Registration

Users provide:

- Username
- Email
- Password

Passwords are hashed using bcrypt before being stored in the database.

### Login

After successful login, the backend generates a JWT access token.

The frontend stores the token and sends it with protected API requests using:

```text
Authorization: Bearer <access_token>
```

The backend verifies the token before allowing access to protected resources.

## Application Management

Authenticated users can manage their own job applications.

Each application contains:

- Company
- Job title
- Location
- Status

Supported application statuses:

```text
Applied
Interview
Rejected
Offer
```

Users can:

- Add applications
- View applications
- Edit applications
- Delete applications
- Search applications
- Filter applications by status

Each application is associated with the authenticated user, preventing users from accessing another user's applications.

## Dashboard

The dashboard displays application statistics including:

- Total applications
- Applied
- Interviews
- Rejected
- Offers

The dashboard also provides the interface for managing applications.

## API Endpoints

### Authentication

| Method | Endpoint | Description |
|---|---|---|
| POST | `/register` | Register a new user |
| POST | `/login` | Authenticate a user |
| GET | `/me` | Get the authenticated user's ID |

### Applications

| Method | Endpoint | Description |
|---|---|---|
| POST | `/applications` | Create an application |
| GET | `/applications` | Get the user's applications |
| GET | `/applications/{id}` | Get a specific application |
| PUT | `/applications/{id}` | Update an application |
| DELETE | `/applications/{id}` | Delete an application |

### Dashboard

| Method | Endpoint | Description |
|---|---|---|
| GET | `/dashboard/stats` | Get application statistics |

## Search and Filtering

Applications can be searched using:

```text
GET /applications?search=Google
```

The search checks:

- Company
- Job title

Applications can also be filtered by status:

```text
GET /applications?status=Interview
```

Search and status filtering can also be combined.

## Running the Project Locally

### 1. Clone the repository

```bash
git clone <repository-url>
cd job-application-tracker
```

### 2. Create a virtual environment

```bash
python -m venv venv
```

### 3. Activate the virtual environment

#### Windows CMD

```cmd
venv\Scripts\activate
```

#### Windows PowerShell

```powershell
.\venv\Scripts\Activate.ps1
```

### 4. Install dependencies

```bash
pip install -r backend/requirements.txt
```

### 5. Configure environment variables

Create a file named:

```text
backend/.env
```

Add:

```env
SECRET_KEY=your-secret-key
```

### 6. Start the backend

Navigate to the backend directory:

```bash
cd backend
```

Run:

```bash
uvicorn main:app --reload
```

The API will be available at:

```text
http://127.0.0.1:8000
```

Interactive API documentation:

```text
http://127.0.0.1:8000/docs
```

### 7. Start the frontend

Open a second terminal and navigate to:

```bash
cd frontend
```

Run:

```bash
python -m http.server 5500
```

Then open:

```text
http://127.0.0.1:5500/login.html
```

## Security

The project includes several basic security practices:

- Passwords are hashed using bcrypt.
- JWT tokens are used for authentication.
- Protected endpoints require authentication.
- Users can only access their own applications.
- The JWT secret is stored in an environment variable.
- `.env` is excluded from Git.
- The virtual environment is excluded from Git.
- The SQLite database is excluded from Git.

## Future Improvements

Possible future improvements include:

- PostgreSQL database for production
- Cloud deployment
- Application deadlines
- Notes and job descriptions
- Resume tracking
- Email reminders
- Analytics and charts
- Pagination
- Password reset functionality
- Improved frontend validation
- Automated testing
- CI/CD pipeline

## Project Status

The core application is complete and functional.

Current functionality includes authentication, CRUD operations, search and filtering, dashboard statistics, and a responsive frontend.

The project is ready for deployment and further production-oriented improvements.