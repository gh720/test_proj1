# Test project using DRF

### Requirements:

* Python 3

# Installation and running in development mode:

    python -m venv venv 
    git clone https://github.com/gh720/test_proj1.git test_proj1
    # locate `activate` script in venv directory, its location depends on your OS
    activate test_proj1
    cd test_proj1
    pip install -r requirements.txt
    python manage.py migrate
    python manage.py loaddata fixtures/auth.json
    python manage.py loaddata fixtures/tourmarks.json
    python manage.py runserver

# Check the server is running:

    http://localhost:8000/users

# See the available endpoints:
   
    http://localhost:8000/docs

# Check the functionality:
    
    http://localhost:8000/locations/1/ratio
    http://localhost:8000/users/1/ratio

# Run the tests

    python manage.py test
