# 🏋️ Gym Management API (FastAPI)

This project is a **FastAPI-based backend API** designed to integrate with gym and fitness club management systems.
It provides a clean and scalable API layer for managing members, payments, attendance, and administrative authentication.

The API can be used by desktop-based admin programs, web dashboards, mobile apps, or other external systems that require reliable gym data integration.

---

## ✨ Features

* Member management (create, update, status control)
* Membership plans and payment integration
* Attendance and usage history tracking
* Admin authentication and authorization (JWT)
* RESTful API design
* High-performance asynchronous processing with FastAPI

---

## 🧱 Tech Stack

* **Python 3.10+**
* **FastAPI**
* SQLAlchemy (ORM)
* PostgreSQL or MySQL
* JWT Authentication
* Uvicorn

---


## 🚀 Getting Started

아래는 **Poetry 기반 개발 환경**을 기준으로 한 설치 및 실행 방법입니다.
Python 가상환경을 직접 만들 필요 없이, Poetry가 의존성과 환경을 함께 관리합니다.

### 1. Clone the repository

```bash
git clone https://github.com/humake-dev/gym.git
cd gym
```

### 2. Install Poetry (if not installed)

```bash
pip install poetry
```

> 이미 Poetry를 사용 중이라면 이 단계는 건너뛰어도 됩니다.

---

### 3. Install dependencies

```bash
poetry install
```

Poetry가 자동으로 가상환경을 생성하고 의존성을 설치합니다.

---

### 4. Configure environment variables

```bash
cp .env.example .env
```

DB 정보, SECRET_KEY 등 실행에 필요한 환경 변수를 설정하세요.

---

### 5. Run the server

```bash
poetry run uvicorn main:app --host 0.0.0.0 --reload
```

개발 서버가 실행되면 API를 바로 사용할 수 있습니다.

---

## 📖 API Documentation

FastAPI provides automatic interactive documentation.

* **Swagger UI**
  `http://localhost:8000/docs`

* **ReDoc**
  `http://localhost:8000/redoc`

---

## 🔐 Authentication

* JWT-based authentication
* Access token / refresh token flow
* Role-based access control for administrators and users

---

## 🔗 Integration Use Cases

This API is designed to integrate with:

* Gym or fitness club admin software (desktop or web)
* Mobile apps for members
* Kiosk or access control systems
* External payment gateways

---

## 🛠️ Development Notes

* Business logic is organized under the `domain/model_crud/` layer
* Request and response schemas are separated in `domain/model_schemas/`
* Modular structure for easy maintenance and extension

---

## 📄 License

MIT License
