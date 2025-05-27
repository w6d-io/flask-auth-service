# Flask Auth Service

A simple Flask authentication service that validates Bearer tokens against a configurable list of valid keys.

## Features

- Bearer token validation
- Environment variable configuration
- Health check endpoint
- Command-line interface
- Easy pip installation
- Docker support ready

## Installation

```bash
pip install flask-auth-service
```

## Quick Start

### 1. Set Environment Variables

```bash
export VALID_KEYS="your-secret-key-1,your-secret-key-2,your-secret-key-3"
```

### 2. Run the Service

```bash
flask-auth-service
```

Or with custom options:

```bash
flask-auth-service --host 127.0.0.1 --port 8080 --debug
```

### 3. Test the Service

```bash
# Health check
curl http://localhost:8081/health

# Valid token
curl -H "Authorization: Bearer your-secret-key-1" http://localhost:8081/validate

# Invalid token
curl -H "Authorization: Bearer invalid-key" http://localhost:8081/validate
```

## Configuration

### Environment Variables

- `VALID_KEYS`: Comma-separated list of valid bearer tokens (required)

### Using .env File

Create a `.env` file:

```
VALID_KEYS=key1,key2,key3
```

Then run:

```bash
flask-auth-service --env-file .env
```

## API Endpoints

### POST/GET /validate

Validates the Bearer token in the Authorization header.

**Request:**
```
Authorization: Bearer <your-token>
```

**Success Response (200):**
```json
{
  "subject": "authorized-user",
  "extra": {}
}
```

**Error Response (401):**
```json
{
  "error": "unauthorized"
}
```

### GET /health

Health check endpoint.

**Response (200):**
```json
{
  "status": "healthy",
  "keys_configured": true,
  "key_count": 3,
  "version": "1.0.0"
}
```

### GET /

Service information endpoint.

## Development

### Local Development

```bash
git clone https://github.com/w6d-io/flask-auth-service
cd flask-auth-service
pip install -e .
```

### Building the Package

```bash
python -m build
```

### Publishing to PyPI

```bash
python -m twine upload dist/*
```

## Docker Usage

```dockerfile
FROM python:3.11-slim

WORKDIR /app

RUN pip install flask-auth-service

ENV VALID_KEYS="your-keys-here"

EXPOSE 8081

CMD ["flask-auth-service"]
```

## License

MIT License - see LICENSE file for details.

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request