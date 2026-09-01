# WSGI Entrypoint for Gunicorn, uWSGI, ATS Deploy and PaaS runners
from main import app as application, app

if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 1051))
    host = os.environ.get("HOST", "0.0.0.0")
    app.run(host=host, port=port)
