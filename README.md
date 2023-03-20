# APZ-CeneoScrapper
## 1. Start kontenera
- ./APZ-CeneoScrapper/flask_app>
  - docker-compose build
  - docker-compose up
- Testowa strona Flaska jest dostępna pod adresem localhost:5001 lub 127.0.0.1:5001
- Usunięcie tabeli i utworzenie:
  - docker-compose run --rm app python manage.py recreate_db
  - (parametr --rm usuwa kontener tworzony na potrzebę 'migracji' - nie zaśmieci docker machine)


## 2. Wymagania na zaliczenie:
![alt text](docs/wymagania_na_zjo.png)

