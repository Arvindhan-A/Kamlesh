# Flask Application Alias for Deployment Platforms
import os
from main import app, application

if __name__ == "__main__":
    port_str = os.environ.get("PORT", "1051")
    try:
        port = int(port_str)
    except ValueError:
        port = 1051
    host = os.environ.get("HOST", "0.0.0.0")
    debug = os.environ.get("FLASK_DEBUG", "false").lower() in ("true", "1", "yes")
    app.run(host=host, port=port, debug=debug)
