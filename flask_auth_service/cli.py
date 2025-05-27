import os
import sys
import argparse
from .app import create_app


def main():
    """Command line interface for Flask Auth Service"""
    parser = argparse.ArgumentParser(description='Flask Auth Service')
    parser.add_argument('--host', default='0.0.0.0', help='Host to bind to (default: 0.0.0.0)')
    parser.add_argument('--port', type=int, default=8081, help='Port to bind to (default: 8081)')
    parser.add_argument('--debug', action='store_true', help='Enable debug mode')
    parser.add_argument('--env-file', help='Path to .env file')

    args = parser.parse_args()

    # Load environment file if specified
    if args.env_file:
        from dotenv import load_dotenv
        load_dotenv(args.env_file)

    # Create the Flask app
    app = create_app()

    # Check if valid keys are configured
    if not app.config['VALID_KEYS']:
        print("ERROR: No valid keys found. Please set the VALID_KEYS environment variable.")
        print("Example: VALID_KEYS='key1,key2,key3'")
        print("Or create a .env file with: VALID_KEYS=key1,key2,key3")
        sys.exit(1)

    print(f"Starting Flask Auth Service on {args.host}:{args.port}")
    print(f"Debug mode: {args.debug}")
    print(f"Valid keys configured: {len(app.config['VALID_KEYS'])}")

    # Run the application
    app.run(host=args.host, port=args.port, debug=args.debug)


if __name__ == '__main__':
    main()