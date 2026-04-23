# 🏥 Healthcare Backend API

A robust and secure REST API designed for hospital staff, patient management, and doctor-patient relationship tracking.

---

## 🏗️ System Architecture

```mermaid
graph TD
    User((👤 Client/User)) -->|REST API| API[Django REST Framework]
    API -->|Auth| JWT[🔒 SimpleJWT Auth]
    API -->|Validation| Serializers[📝 DRF Serializers]
    Serializers -->|CRUD| ORM[🐍 Django ORM]
    ORM -->|Persistence| DB[(🗄️ PostgreSQL)]

    subgraph "Core Backend Services"
    API
    JWT
    Serializers
    ORM
    end
```


## Tech Stack
- Django
- Django REST Framework (DRF)
- PostgreSQL
- JWT (SimpleJWT)

## Project Structure
healthcare_backend/
├── api/
│   ├── models.py
│   ├── views.py
│   ├── serializers.py
│   ├── urls.py
├── healthcare_backend/
│   ├── settings.py
│   ├── urls.py
├── .env.example
├── requirements.txt
└── manage.py


---

## 📊 Database Schema

```mermaid
erDiagram
    USER ||--o{ PATIENT : "manages"
    PATIENT ||--o{ MAPPING : "assigned_to"
    DOCTOR ||--o{ MAPPING : "attends"
    
    USER {
        string email PK
        string name
        boolean is_active
        boolean is_staff
    }
    PATIENT {
        int id PK
        string name
        int age
        string gender
        string contact
    }
    DOCTOR {
        int id PK
        string name
        string specialization
        string phone
        string email
    }
    MAPPING {
        int id PK
        datetime assigned_date
    }
```


## Getting Started

### 1. Clone the repo
```bash
git clone <your-repo-url>
cd healthcare_backend
```

### 2. Create virtual environment
```bash
python -m venv venv
venv\Scripts\activate         # Windows
# source venv/bin/activate    # Mac/Linux
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Set up environment variables
Create a `.env` file in the root directory (tip: copy `.env.example`):
```text
SECRET_KEY=your_secret_key
DB_NAME=hospital_db
DB_USER=postgres
DB_PASSWORD=your_password
DB_HOST=localhost
DB_PORT=5432
```

### 5. Run migrations
```bash
python manage.py makemigrations
python manage.py migrate
```

### 6. Start the server
```bash
python manage.py runserver
```

## API Endpoints

### Auth
| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| POST | /api/auth/register/ | Register new user | No |
| POST | /api/auth/login/ | Login, returns JWT | No |

### Patients
| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| POST | /api/patients/ | Add a patient | Yes |
| GET | /api/patients/ | Get your patients | Yes |
| GET | /api/patients/<id>/ | Get one patient | Yes |
| PUT | /api/patients/<id>/ | Update patient | Yes |
| DELETE | /api/patients/<id>/ | Delete patient | Yes |

### Doctors
| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| POST | /api/doctors/ | Add a doctor | Yes |
| GET | /api/doctors/ | Get all doctors | Yes |
| GET | /api/doctors/<id>/ | Get one doctor | Yes |
| PUT | /api/doctors/<id>/ | Update doctor | Yes |
| DELETE | /api/doctors/<id>/ | Delete doctor | Yes |

### Patient-Doctor Mappings
| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| POST | /api/mappings/ | Assign doctor to patient | Yes |
| GET | /api/mappings/ | All mappings | Yes |
| GET | /api/mappings/patient/<patient_id>/ | Doctors for a patient | Yes |
| DELETE | /api/mappings/<id>/ | Remove mapping | Yes |

## Authentication

This project uses JWT for stateless auth. After logging in, include the token in your headers:
`Authorization: Bearer <your_access_token>`
---

### 🔄 Request Lifecycle

```mermaid
sequenceDiagram
    participant C as Client
    participant M as Middleware (Auth)
    participant V as View (Logic)
    participant D as Database

    C->>M: HTTP Request + JWT
    M->>M: Validate Token
    alt Token Valid
        M->>V: Pass Request
        V->>D: Query/Save Data
        D-->>V: Result
        V-->>C: JSON Response (200/201)
    else Token Invalid
        M-->>C: Error Response (401 Unauthorized)
    end
```

---

## 🧪 Testing

The project includes a robust testing suite.

### Standard Django Tests (Recommended)
Run these to verify the backend logic using isolated test databases:
```bash
python manage.py test api
```




## Notes
- Used a custom User model with `email` as the primary identifier.
- Patients are scoped to the user who created them (privacy first).
- Using a bridge table for mappings to keep the patient/doctor relationship clean.
