# Test task. Part 1

## To run project please follow:
    - copy project to machine
    - create your local env/venv
    - pip install -r dev.txt
    - python manage.py migrate
    - python manage.py runserver
    
    If it's still not working then I forget to put something.
     Please contact me :)
    
## Some APIs endpoint explaining
    - sign-up/ -- Sign up. POST request. Data: name, password, email,
     sex(for custom user model, not required).
     
    - api-token-auth/ -- Log in. POST request.
     Username(name from previous example) and password required.
     
    - create-post/ -- Post creation. Titel and body required.
    
    - like-post/ -- Post like. Post id required.


## To run tests
    - pytest
