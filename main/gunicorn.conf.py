bind = "0.0.0.0:8000"
workers = 4
keepalive = 5
wsgi_app = "main.wsgi"
capture_output = True
accesslog = "/data/access.log"
errorlog = "/data/error.log"
loglevel = "debug"
