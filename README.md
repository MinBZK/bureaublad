# Bureaublad

Bureaublad is a flexible dashboard that aggregates information from multiple open-source components, providing users with a unified interface to access essential tools and data.

It is a stateless application, so all data stays at the source.

## Integrated Tools

- [CalDav](https://datatracker.ietf.org/doc/html/rfc4791) (calendar protocol)
- [Docs](https://github.com/suitenumerique/docs)
- [Ocs](https://docs.nextcloud.com/server/stable/developer_manual/client_apis/OCS/ocs-api-overview.html) (Nextcloud & OwnCloud protocol)
- [OpenZaak](https://github.com/open-zaak/open-zaak)
- OpenAI Chat Completion API

## Planned Integrations

- [Synapse](https://github.com/element-hq/synapse)
- [Drive](https://github.com/suitenumerique/drive)
- [Meet](https://github.com/suitenumerique/meet)

## Getting Started

To run Bureaublad, ensure you have [Docker](https://docs.docker.com/get-started/get-docker/) installed.

The copy the example.env in the backend to .env

```bash
cp backend/example.env backend/.env
```

Then, build and start the application with:

```sh
docker compose build
docker compose up
```

When the application start you will get 3 urls:

1. <http://localhost:3000>
2. <http://localhost:8081>
3. <http://localhost:8080>

You can use the admin user to login:

```
username: admin
password: admin
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
- **Design System:** [Rijkshuiststyle NL-Design System](https://github.com/nl-design-system/rijkshuisstijl-community)

**Note:** Your identity provider must support Token Exchange for authentication. Verify compatibility before deployment.

