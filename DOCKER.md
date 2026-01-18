# Docker Setup

## Local Development

```bash
# Start (builds if needed)
docker compose up

# Rebuild after code changes
docker compose up --build

# Stop
docker compose down

# Reset database (loads from docker/init-db/*.sql)
docker compose down -v && docker compose up
```

App runs at http://localhost:5001

### Database

Place SQL dump at `docker/init-db/fachme.sql` before first run.

## Production Deployment

On VPS (jordaneldredge.com):

```bash
cd ~/projects/fachme
git pull
docker compose -f docker-compose.yml -f docker-compose.prod.yml up -d --build
```

Apache proxies fachme.com to 127.0.0.1:5001.

### First-time setup

1. Install Docker
2. Clone repo to ~/projects/fachme
3. Copy database dump to docker/init-db/fachme.sql
4. Add user to docker group: `sudo usermod -aG docker $USER`
5. Start containers with prod compose files
6. Configure Apache reverse proxy
