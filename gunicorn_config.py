import os

# Gunicorn configuration file

# The address to bind to
bind = os.environ.get("BIND", "0.0.0.0")

# The port to bind to
port = os.environ.get("PORT", "5001")
bind = f"{bind}:{port}"

# The number of worker processes
workers = int(os.environ.get("WEB_CONCURRENCY", 4))

# The type of worker to use
worker_class = "gevent"
