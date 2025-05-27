import os
from flask import Flask, request, jsonify
from dotenv import load_dotenv


def get_valid_keys():
    """Get valid keys from environment variable VALID_KEYS"""
    env_keys = os.getenv('VALID_KEYS', '')
    if not env_keys:
        print("WARNING: No VALID_KEYS environment variable found. Using empty key list.")
        return []

    # Split by comma and strip whitespace from each key
    keys = [key.strip() for key in env_keys.split(',') if key.strip()]
    print(f"Loaded {len(keys)} valid keys from environment")
    return keys


def create_app(config=None):
    """Application factory pattern"""
    # Load environment variables from .env file if it exists
    load_dotenv()

    app = Flask(__name__)

    # Load configuration
    if config:
        app.config.update(config)

    # Load valid keys at startup
    valid_keys = get_valid_keys()
    app.config['VALID_KEYS'] = valid_keys

    @app.route('/validate', methods=['GET', 'POST'])
    def validate():
        print("Headers received:")
        for header, value in request.headers.items():
            print(f"{header}: {value}")

        auth_header = request.headers.get("Authorization", "")
        token = auth_header.replace("Bearer ", "").strip()

        print(f"Received token: {token}")

        if not app.config['VALID_KEYS']:
            print("No valid keys configured")
            return jsonify({"error": "service misconfigured"}), 500

        if token in app.config['VALID_KEYS']:
            print("Token is valid")
            return jsonify({"subject": "authorized-user", "extra": {}})
        else:
            print("Token is invalid")
            return jsonify({"error": "unauthorized"}), 401

    @app.route('/health', methods=['GET'])
    def health():
        """Health check endpoint"""
        return jsonify({
            "status": "healthy",
            "keys_configured": len(app.config['VALID_KEYS']) > 0,
            "key_count": len(app.config['VALID_KEYS']),
            "version": "1.0.0"
        })

    @app.route('/', methods=['GET'])
    def index():
        """Root endpoint with service information"""
        return jsonify({
            "service": "Flask Auth Service",
            "version": "1.0.0",
            "endpoints": {
                "/validate": "POST/GET - Validate Bearer token",
                "/health": "GET - Health check",
                "/": "GET - Service information"
            }
        })

    return app
