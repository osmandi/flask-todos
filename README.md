# Práctica del proyecto del curso de Flask de Platzi

### Instalacion de entorno

```
virtualenv venv --python=python3
source venv/bin/activate
pip install -r requirements.txt

export FLASK_APP=main.py

# Para entorno de desarrollo
export FLASK_DEBUG=1
export FLASK_ENV=development

```

### Correr servidor

```
# Correr servidor
flask run

# Correr tests
flask test
```


> Nota: La app funciona con SQLite, la estructura del la base de datos está dentro del repositorio :)
