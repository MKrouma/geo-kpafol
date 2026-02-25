# geo-kpafol

## Dev
```
pip freeze > requirements.txt
flask run --debug
```

## Database 
Design
```
Tables 
- users : user_id; email, password, created_at, updated_at, avatar_hash
```


PROD Migration
```
flask --app=main.py db init
flask --app=main.py db migrate -m "on prod"
flask --app=main.py db upgrade
flask --app=main.py db stamp head
```

DEV Migraton
```
flask --app=main.py db init --directory mig_dev
flask --app=main.py db migrate -m "avatar from has" --directory mig_dev
flask --app=main.py db upgrade --directory mig_dev
flask --app=main.py db stamp head --directory mig_dev


Shell 
```
flask --app=main.py shell
```