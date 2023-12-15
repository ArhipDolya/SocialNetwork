# Social Network

This is a Django project for a social network application. It includes user authentication, posts, and analytics functionality.

## Getting Started

### Prerequisites

- [Docker](https://www.docker.com/) and [Docker Compose](https://docs.docker.com/compose/) installed on your machine.

### Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/your-username/SocialNetwork.git
   ```
2. Navigate to the project directory:
    ```bash
    cd SocialNetwork
    ```
3. Build and run the Docker containers:
    ```bash
    docker-compose up --build
    ```
    This will set up the Django development server, PostgreSQL database, and Redis.   
4. Run migrations:
    ```bash
   docker-compose run --rm web-app sh -c "python manage.py makemigrations"
   docker-compose run --rm web-app sh -c "python manage.py migrate"
    ```
5. Create superuser:
    ```bash
   docker-compose run --rm web-app sh -c "python manage.py createsuperuser"
   ```
6. Access the Django admin panel:
    ```bash
   URL: http://localhost:8000/admin/
   ```
   
# Project Structure
SocialNetwork/ - Django project root directory.

user_auth/ - App for user authentication.

posts/ - App for managing posts and likes.

requirements.txt - List of Python dependencies.

Dockerfile - Docker configuration file.

docker-compose.yml - Docker Compose configuration file.

# Configuration
Environment Variables
The project uses environment variables for configuration. You can set these in the .env file in the project root.

SECRET_KEY - Django secret key for security.

DB_HOST, DB_NAME, DB_USER, DB_PASS - PostgreSQL database connection details.

# Usage
Access the Django development server:

```bash
http://localhost:8000/
```

Access the PostgreSQL database:

Host: localhost

Port: 5432

Database: dbname

Username: dbuser

Password: pass

Access the Redis server:

Host: localhost

Port: 6379