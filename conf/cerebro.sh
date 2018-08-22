#!/bin/env sh

NAME="cerebro"
DJANGODIR=/home/javier/proyectos/cerebro/src
SOCKFILE=/home/javier/proyectos/goals/run/cerebro.sock
USER=javier
GROUP=javier
NUM_WORKERS=5
DJANGO_SETTINGS_MODULE=core.settings
DJANGO_WSGI_MODULE=core.wsgi

echo "Iniciando $NAME como `whoami`"

cd $DJANGODIR
source /home/javier/.pyenv/shims/activate cerebro

export DJANGO_SETTINGS_MODULE=$DJANGO_SETTINGS_MODULE
export PYTHONPATH=$DJANGODIR:$PYTHONPATH

exec /home/javier/.pyenv/versions/goals/bin/gunicorn \
  ${DJANGO_WSGI_MODULE}:application \
  --name $NAME \
  --workers $NUM_WORKERS \
  --user=$USER --group=$GROUP \
  --log-level=debug #\
  --bind=unix:$SOCKFILE


