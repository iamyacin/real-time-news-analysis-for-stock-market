# Restored React + Spring report UI

This directory contains the original CoreUI/React frontend and Spring Boot API
from the 2020 PFE, restored from git history and adapted to the 2026 data schema.

> **Authorship:** the original 2020 PFE was a pair project by Yassine DAOUJI
> and Mohammed AZZOUZ. Mohammed AZZOUZ built the original React/Spring report
> application preserved here. Yassine DAOUJI led the overall project and carried
> out the 2026 restoration and adaptation in collaboration with the OpenCode AI
> coding agent (DeepSeek V4.1 Flash model). See
> [`docs/AI_ASSISTANCE.md`](../../docs/AI_ASSISTANCE.md).

## Run with Docker Compose

From the repository root:

```bash
docker compose up --build legacy-backend legacy-frontend
```

- Frontend: <http://localhost:3000>
- API: <http://localhost:8081/api/health>
- Login: `admin` / `admin123`

The API reads the same MongoDB `NewsCollection` and `SocietiesInfo` collections
as the Streamlit dashboard.

## Changes made to the legacy code

- Removed unused MySQL/JPA configuration; MongoDB is the only database.
- Added `jaxb-api`/`jaxb-runtime` for jjwt on Java 11.
- Seeded roles, the demo admin user, and societies on startup.
- Changed `News.publishedAt` to `String` to match the ISO strings written by the
  restored pipeline.
- Fixed the `getAllOps` percentage calculation.
- Added `/api/health`.
- Configured the API URL through `REACT_APP_API_URL`.
- Removed the fake backend wrapper and displayed demo credentials on login.
- Added Dockerfiles pinned to Java 11 and Node 14.

## Development

Backend:

```bash
cd apps/legacy-ui/backend
./mvnw spring-boot:run   # requires Java 11 and MongoDB
```

Frontend:

```bash
cd apps/legacy-ui/frontend
npm ci
REACT_APP_API_URL=http://localhost:8081 npm start
```

Node 14 is required because the original frontend uses `node-sass@4.14`.
