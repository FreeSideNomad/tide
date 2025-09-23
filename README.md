# Tide - Safety-First DBT AI Assistant

**Tide** is a Python Flet application targeting mobile and web users. This is a safety-first DBT (Dialectical Behavior Therapy) AI assistant designed to guide individuals through DBT skills development using structured decision-tree architecture.

## 🚀 Quick Start

### Docker (Recommended)

The fastest way to get Tide running:

```bash
# Pull latest image
docker pull ghcr.io/freesidenomad/tide:latest

# Run with required environment variables
docker run -p 8080:8080 \
  -e OPENAI_API_KEY=your_openai_key \
  -e GOOGLE_CLIENT_ID=your_google_client_id \
  -e GOOGLE_CLIENT_SECRET=your_google_client_secret \
  ghcr.io/freesidenomad/tide:latest
```

Access the app at: http://localhost:8080

**📚 Full Docker documentation**: [docs/docker.md](docs/docker.md)

### Local Development

#### Using uv (Recommended)

Run as a desktop app:
```bash
uv run flet run
```

Run as a web app:
```bash
uv run flet run --web --port 8080
```

#### Using Poetry

Install dependencies:
```bash
poetry install
```

Run as a desktop app:
```bash
poetry run flet run
```

Run as a web app:
```bash
poetry run flet run --web --port 8080
```

### Environment Variables

Create a `.env` file with:
```bash
OPENAI_API_KEY=your_openai_api_key
GOOGLE_CLIENT_ID=your_google_oauth_client_id
GOOGLE_CLIENT_SECRET=your_google_oauth_client_secret
DATABASE_URL=postgresql://user:password@localhost:5432/tide_db  # optional
```

## Build the app

### Android

```
flet build apk -v
```

For more details on building and signing `.apk` or `.aab`, refer to the [Android Packaging Guide](https://flet.dev/docs/publish/android/).

### iOS

```
flet build ipa -v
```

For more details on building and signing `.ipa`, refer to the [iOS Packaging Guide](https://flet.dev/docs/publish/ios/).

### macOS

```
flet build macos -v
```

For more details on building macOS package, refer to the [macOS Packaging Guide](https://flet.dev/docs/publish/macos/).

### Linux

```
flet build linux -v
```

For more details on building Linux package, refer to the [Linux Packaging Guide](https://flet.dev/docs/publish/linux/).

### Windows

```
flet build windows -v
```

For more details on building Windows package, refer to the [Windows Packaging Guide](https://flet.dev/docs/publish/windows/).