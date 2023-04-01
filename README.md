# APZ-CeneoScrapper

## 1. Start kontenera

- ./APZ-CeneoScrapper/flask_app>
    - docker-compose build
    - docker-compose up
    - lub
    - docker-compose up --build (mozna dodać też parametr -d (detach), żeby odpiąć kontener od aktywnego terminala)
- Testowa strona Flaska jest dostępna pod adresem localhost:5001 lub 127.0.0.1:5001
    - Usunięcie tabeli i utworzenie:
        - 'docker-compose exec app python manage.py recreate_db'
    - Dostępne są też inne komendy, wszystkie docelowo będą w pliku manage.py.
     podejrzeć je można uruchamiając 'docker-compose exec app python manage.py'
      - create_admin    Create admin user
      - db              Perform database migrations.
      - populate_Posts
      - recreate_db
      - routes          Show the routes for the app.
      - run             Run a development server.
      - shell           Run a shell in the app context.
      - show
      - show_users
      - test            Runs the unit tests without coverage.

## 2. Endpointy
- http://localhost:5001/ - no wiadomo;
- http://localhost:5001/login - panel logowania. Dostępny jedynie gdy użytkownik pozostaje niezalogowany;
- http://localhost:5001/register - panel rejestracji. Dostępny jedynie gdy użytkownik pozostaje niezalogowany; 
- http://localhost:5001/confirm/<TOKEN_ID> - potwierdzenie konta po rejestracji;
- http://localhost:5001/products/<produkt_id_z_ceneo> - pobiera, wyświetla i zapisuje do bazy danych SQLite 
recenzje pobrane z Ceneo
- http://localhost:5001/products/ - wyświetla wszystkie pobrane do tej pory pobrane recenzje z Ceneo
## 2. Wymagania na zaliczenie:

![alt text](docs/wymagania_na_zjo.png)

