# cerebro

## Configuración

Para poder usar esta aplicación hay que crear un archivo `.env.json` con las opciones de configuración pertinentes:

```json
{
  "SECRET_KEY": "kminvupn=7dbw70e!#njo8qas2bx$tmw$nv1pt$g30&+f4(8c)",
  "DEBUG": true,
  "SSL": false,
  "ALLOWED_HOSTS": [
    "*"
  ],
  "DATABASE": {
    "NAME": "dbname",
    "USER": "dbuser",
    "PASSWORD": "dbsecret"
  }
}
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
