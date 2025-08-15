import os
from flask import Flask, request, jsonify
from dotenv import load_dotenv
try:
    from importlib.metadata import version
except ImportError:
    from importlib_metadata import version


def get_valid_keys():
    """Get valid keys from environment variable VALID_KEYS
    Format: key1:tenant1,tenant2;key2:tenant3,tenant4
    Returns: dict mapping API keys to list of tenants
    """
    env_keys = os.getenv('VALID_KEYS', '')
    if not env_keys:
        print("WARNING: No VALID_KEYS environment variable found. Using empty key list.")
        return {}

    key_tenant_map = {}
    
    # Split by semicolon to separate different API keys
    key_entries = [entry.strip() for entry in env_keys.split(';') if entry.strip()]
    
    for entry in key_entries:
        if ':' not in entry:
            print(f"WARNING: Invalid key entry format. Expected 'key:tenant1,tenant2'")
            continue
            
        key, tenants_str = entry.split(':', 1)
        key = key.strip()
        
        if not key:
            print(f"WARNING: Empty key in entry")
            continue
            
        # Split tenants by comma and strip whitespace
        tenants = [tenant.strip() for tenant in tenants_str.split(',') if tenant.strip()]
        
        if not tenants:
            print(f"WARNING: No tenants found for a key")
            continue
            
        key_tenant_map[key] = tenants
        print(f"Loaded key with {len(tenants)} tenant(s)")
    
    print(f"Loaded {len(key_tenant_map)} valid keys from environment")
    return key_tenant_map


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
            if header.lower() == 'authorization':
                print(f"{header}: [REDACTED]")
            else:
                print(f"{header}: {value}")

        auth_header = request.headers.get("Authorization", "")
        token = auth_header.replace("Bearer ", "").strip()
        tenant = request.headers.get("tenant", "").strip()

        print("Token validation attempt")
        print(f"Requested tenant: {tenant}")

        if not app.config['VALID_KEYS']:
            print("No valid keys configured")
            return jsonify({"error": "service misconfigured"}), 500

        if not tenant:
            print("Missing tenant header")
            return jsonify({"error": "tenant header required"}), 400

        if token in app.config['VALID_KEYS']:
            allowed_tenants = app.config['VALID_KEYS'][token]
            if tenant in allowed_tenants:
                print("Token and tenant are valid")
                return jsonify({
                    "subject": "authorized-user", 
                    "extra": {
                        "tenant": tenant,
                        "allowed_tenants": allowed_tenants
                    }
                })
            else:
                print(f"Token valid but tenant '{tenant}' not allowed")
                return jsonify({"error": "unauthorized for this tenant"}), 403
        else:
            print("Token is invalid")
            return jsonify({"error": "unauthorized"}), 401

    @app.route('/health', methods=['GET'])
    def health():
        """Health check endpoint"""
        try:
            app_version = version("flask-auth-service")
        except Exception:
            app_version = "unknown"
            
        return jsonify({
            "status": "healthy",
            "keys_configured": len(app.config['VALID_KEYS']) > 0,
            "key_count": len(app.config['VALID_KEYS']),
            "version": app_version
        })

    @app.route('/', methods=['GET'])
    def index():
        """Root endpoint with service information"""
        try:
            app_version = version("flask-auth-service")
        except Exception:
            app_version = "unknown"
            
        return jsonify({
            "service": "Flask Auth Service",
            "version": app_version,
            "endpoints": {
                "/validate": "POST/GET - Validate Bearer token and tenant",
                "/health": "GET - Health check",
                "/": "GET - Service information"
            }
        })

    return app
