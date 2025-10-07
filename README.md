# Bureaublad

![GitHub Actions Workflow Status](https://img.shields.io/github/actions/workflow/status/minbzk/bureaublad/build-backend.yaml?label=backend)
![GitHub Actions Workflow Status](https://img.shields.io/github/actions/workflow/status/minbzk/bureaublad/build-frontend.yaml.yaml?label=frontend)
[![Coverage](https://sonarcloud.io/api/project_badges/measure?project=MinBZK_bureaublad&metric=coverage)](https://sonarcloud.io/summary/new_code?id=MinBZK_bureaublad)
[![Quality Gate Status](https://sonarcloud.io/api/project_badges/measure?project=MinBZK_bureaublad&metric=alert_status)](https://sonarcloud.io/summary/new_code?id=MinBZK_bureaublad)
![GitHub License](https://img.shields.io/github/license/minbzk/bureaublad)

Bureaublad is a flexible dashboard that aggregates information from multiple open-source components, providing users with a unified interface to access essential tools and data.

It is a stateless application, so all data stays at the source.

## Integrated Tools

- [CalDav protocol](https://datatracker.ietf.org/doc/html/rfc4791) (calendar protocol)
  - calendar
  - tasks
- [Docs](https://github.com/suitenumerique/docs)
- [Ocs](https://docs.nextcloud.com/server/stable/developer_manual/client_apis/OCS/ocs-api-overview.html) (Nextcloud & OwnCloud protocol)
  - activity app
- [Drive](https://github.com/suitenumerique/drive)
- [Meet](https://github.com/suitenumerique/meet)
- [OpenAI interface](https://github.com/openai/openai-python)

## Planned Integrations

- [Synapse](https://github.com/element-hq/synapse)

## Getting Started

To run Bureaublad, ensure you have [Docker](https://docs.docker.com/get-started/get-docker/) installed.

copy the example.env in the backend to .env

```bash
cp backend/example.env backend/.env
```

Then, build and start the application with:

```sh
docker compose build
docker compose up
```

When the application start you will get 4 urls:

- [frontend](http://localhost:3000)
- [backend](http://localhost:8000)
- [keycloak master](http://localhost:8080)
- [keycloak mijnbureau](http://localhost:8080/realms/mijnbureau/account/)

In the master realm you can login with the admin credentials and manage all realm, including mijnbureau

```
username: admin
password: admin
```

in the MijnBureau realm you can login with 4 users:

```
username: jane@mijnbureau.nl password: jane
username: john@mijnbureau.nl password: john
```

## Solution Architecture

Bureaublad consolidates data from various tools into a single platform, making it easier for users to access the information they need, when they need it.

The solution consists of:

- **Backend:** REST API
- **Frontend:** Single Page Application (SPA)
- **Identity Provider:** Supports OpenID Connect authentication with [Token Exchange](https://datatracker.ietf.org/doc/html/rfc8693)

In the future we plan to add a advanced search feature and make the page more configurable to the users wishes.

## Technical Overview

- **Frontend:** [React](https://react.dev/)
- **Backend:** [FastAPI](https://fastapi.tiangolo.com/)

**Note:** Your identity provider must support Token Exchange for authentication. Verify compatibility before deployment.

