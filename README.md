# Books 2.0

## Baza książek - Zadanie testowe. 
##### ( Widoki wykonano bez użycia ***JavaScript*** ).

Aby uruchomić aplikację należy:
* sklonować pliki do folderu aplikacji
```
mkdir [app_folder_name]
cd [app_folder_name]

git clone https://github.com/TomDom80/booqs2.0.git .
```

* uworzyć plik ***.env*** w tym samym katalogu, w którym znajduje się plik ***manage.py***
* lub zmienić nazwę  pliku ***_env***

```
 mv _env .env
```

przykładowy plik wygląda tak:

### .env
```
SECRET_KEY=valule_of_SECRET_KEY 
GOOGLE_API_KEY=valule_of_GOOGLE_API_KEY
```

oczywiście należy podstawić odpowiednie wartości do zmiennych

#### plik .env trzeba dodać do .gitignore

## Uruchomienie:

Gdy mamy gotowy plik z kluczami. W katalogu, w którym znajduje się plik ***docker-compose.yml*** 
wykonujemy następujące polecenia:

```
docker-compose build
docker-compose up
```

następnie wyświetlamy nazwę utworzonego obrazu docker za pomocą polecenia:

```
docker ps 
```

po czym uruchamiamy wiersz poleceń wewnątrz powłoki za pomocą:

```
docker exec -it [nazwa obrazu] /bin/sh
```
teraz należy wykonać migracje:

```
python manage.py makemigrations books
python manage.py makemigrations 
python manage.py migrate

```

#### po tym wszystkim aplikacja powinna działać prawidłowo na odpowiednich portach wynikających z ustawień.

