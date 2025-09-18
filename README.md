# Product Management API with MongoDB

A RESTful API for managing products and categories with token-based authentication, built with FastAPI and MongoDB.

## Features

- User authentication with JWT tokens
- CRUD operations for products and categories
- Product filtering and search
- Data export in JSON and CSV formats
- MongoDB database for scalable and flexible data storage

## Requirements

- Python 3.11+
- MongoDB 7.0+
- Docker and Docker Compose (for containerized deployment)

## Setup and Installation

1. Clone the repository:
```bash
git clone https://github.com/vitorgv/product-python-mongodb-api.git
cd product-python-mongodb-api
```

2. Create a `.env` file with the following configuration:
```env
MONGODB_URL=mongodb://mongodb:27017
MONGODB_DB=productdb
SECRET_KEY=your-secret-key-for-jwt
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=10
```

3. Run with Docker Compose:
```bash
docker-compose up -d
```

The API will be available at http://localhost:8000

## API Documentation

Once the application is running, you can access:
- API documentation: http://localhost:8000/docs
- Alternative API documentation: http://localhost:8000/redoc

## Testing

The repository includes several test scripts to verify the API functionality:
- test_api.py - Basic API testing
- test_api_endpoints.py - Comprehensive endpoint testing
- comprehensive_test.py - End-to-end testing

To run tests:
```bash
python -m pytest
```

## Default Test User

Email: admin@example.com
Password: testpass123