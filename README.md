# Listat
Приложение для отображения статистики дебютов в рейтинговых играх на lichess.org.

## Установка

Для скачивания игр необходимо создать токен: https://lichess.org/account/oauth/token/create

```
python3 -m venv env
source env/bin/activate
pip install -r requirements.txt
flask --app listat init-db
flask --app listat --debug run
```

Перейти по адресу http://127.0.0.1:5000/ и ввести токен в форму.

![Listat](listat-preview.png)
