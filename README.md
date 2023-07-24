# cerebro

## Configuración

Para poder usar esta aplicación hay que crear un archivo `src/.env`
con las opciones de configuración pertinentes:

```
DEBUG=True
SSL=False
DATABASE_URL=postgresql://usuario:contraseña@servidor:puerto/database
EMAIL_HOST=email_host
EMAIL_PORT=puerto
EMAIL_HOST_USER=usuario
EMAIL_HOST_PASSWORD=
```

Y para usar estas variables en el proyecto se hace así:

```python
To use JSON Environ in a project:
import os

from json_environ import Environ

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
env_path = os.path.join(BASE_DIR, '.my_env.json')
env = Environ(path=env_path)

SECRET_KEY = env('SECRET_KEY', default="PT09PT0KVXNhZ2UKPT09PT0KClRvI")
DEBUG = env("DEBUG")
ALLOWED_HOSTS = env('ALLOWED_HOSTS')
if env('SSL', default=False) is True:
    SECURE_SSL_REDIRECT = False

DATABASES = {
    'default': {
        'NAME': env("DATABASE:NAME", default="test"),
        'USER': env("DATABASE:USER", default="lms"),
        'PASSWORD': env("DATABASE:PASSWORD", default="123456"),
    }
}
```

### Configuración de la base de datos

Parámetros de uso del usuario dueño de la base.

```
ALTER ROLE admin SET client_encoding TO 'utf8';
ALTER ROLE admin SET default_transaction_isolation TO 'read committed';
ALTER ROLE admin SET timezone TO 'Mexico/General';
```

> Versión 201902.1 (27/febrero/2019)
