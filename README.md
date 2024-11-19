# Django-Backend-for-a-Book-Review-API

A Django-powered RESTful API for managing books, reviews, and recommendations. This API supports adding books, reviewing them, viewing recommendations, and retrieving books with an average rating.


## Installation

1. Clone the Project

```bash
  https://github.com/kanakamamidiakhil/Django-Book-Review-API.git
  cd Book-Review-System-Backend
```
2. Create Virtual Environment in Windows

```bash
 python -m venv env
 env\Scripts\activate
 ```

3. Install the required packages:

```bash
 pip install -r requirements.txt
 ```

4. Change the credentials of DATABASE in settings.py to your convinience

5. Apply migrations:

```bash
 python manage.py migrate
 ```

6. Run the Project

```bash
 python manage.py runserver
 ```

7. Open your web browser and go to `http://127.0.0.1:8000/` in Postman to test the API.
  
8. Swagger yaml documentation with API description and usage can be found in api_blueprint folder [a relative link](api_blueprint/openapi.yaml).

9. Postman collection JSON file can be found in api_blueprint folder [a relative link](api_blueprint/Books-management-system-backend.postman_collection.json).
