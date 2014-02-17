#!python
from gevent import monkey

monkey.patch_all()

bind = "0.0.0.0:8000"
workers = 1
worker_class = "gunicorn.workers.ggevent.GeventWorker"
