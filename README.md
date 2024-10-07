# Django API Key Generator
### This project is a Django-based API Key Generator designed to integrate with multiple front-end websites to authenticate access via dynamically generated API keys. It provides a mechanism to generate, retrieve, and validate API keys for different sites. The project also includes an administrative interface for managing these keys.

- Table of Contents
- Features
- Project Structure
- Getting Started
- Installation
- Environment Variables
- Running the Application
- Deployment
- API Endpoints
- Frontend Integration
- Troubleshooting
- License
- Features

 Generate unique API keys for multiple websites.
Store and manage the API keys with expiration timestamps.
Retrieve and validate keys for site-specific access.
Provide a Django Admin interface for managing keys and site configurations.
Serve as a backend for front-end applications using RESTful API endpoints.
## Project Structure
```apikeygen/
├── apikeygen/
│   ├── settings.py      # Django project settings
│   ├── urls.py          # Project URL configuration
│   └── wsgi.py          # WSGI application
├── keygen/
│   ├── models.py        # Database models for API keys
│   ├── views.py         # View logic for API operations
│   ├── urls.py          # Key management routes
│   └── templates/       # HTML templates (if applicable)
├── static/              # Static files (CSS, JS, images)
├── templates/           # HTML templates for the application
└── manage.py            # Django management script
```
## Getting Started
Follow these instructions to get the project up and running on your local machine for development and testing purposes.

- Prerequisites
- Python 3.8+
- Django 5.x
- SQLite (for development)
## 1. Installation
- Clone the repository:
```bash
git clone https://github.com/ivanmarinoff/API-key-GEN.git
cd apikeygen
```
## 2. Create a virtual environment and activate it:
```bash
python -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`
```
## 3. Install the dependencies:
```bash
pip install -r requirements.txt
```
## 4. Apply the initial database migrations:
```bash
python manage.py makemigrations
python manage.py migrate
```
## 5. Environment Variables:
Create a .env file in the project root to manage your environment variables. Set the following values:
```bash
SECRET_KEY=your_secret_key
DEBUG=True  # Set to False in production
ALLOWED_HOSTS=127.0.0.1 localhost yourdomain.com
```
## Running the Application
## 1. Start the Django development server:
```bash
python manage.py runserver
```
Visit the application at: http://127.0.0.1:8000

Access the Django Admin panel at: http://127.0.0.1:8000/admin

## API Endpoints
## 1. Get API Key
- URL: /api/get-key/
- Method: GET

Response:
```json
{
  "key": "abcd1234",
  "expires_at": "2024-10-07 12:00:00"
}
```

## 2. Validate API Key
- URL: /api/validate-key/
- Method: POST 

Request Body:
```json
{
  "key": "abcd1234",
  "site_url": "https://example.com"
}
```
## 3. Django Admin Panel
- Use the Django admin panel at /admin to create, update, and delete API keys.
## Frontend Integration
The frontend application should use the following approach to interact with the API:

- Check if an API key is stored in sessionStorage.
- If not, request a new key using the /api/get-key/ endpoint.
- Validate the key using the /api/validate-key/ endpoint before proceeding with any other operations.

Example JavaScript Integration:

```javascript
function fetchNewApiKey() {
    fetch(`http://127.0.0.1:8000/api/get-key/`)
        .then(response => response.json())
        .then(data => {
            if (data && data.key) {
                sessionStorage.setItem('api_key', data.key);
                console.log('New API Key:', data.key);
            } else {
                console.error('Failed to fetch API Key');
            }
        });
}
```
## CORS Issues:
- Configure CORS_ALLOWED_ORIGINS and CSRF_TRUSTED_ORIGINS correctly in the settings.py file.
## License
- This project is licensed under the MIT License - see the LICENSE file for details.