# Bureaublad

![GitHub Actions Workflow Status](https://img.shields.io/github/actions/workflow/status/minbzk/bureaublad/backend-ci.yaml?label=backend)
![GitHub Actions Workflow Status](https://img.shields.io/github/actions/workflow/status/minbzk/bureaublad/frontend-ci.yaml?label=frontend)
[![Coverage](https://sonarcloud.io/api/project_badges/measure?project=MinBZK_bureaublad&metric=coverage)](https://sonarcloud.io/summary/new_code?id=MinBZK_bureaublad)
[![Quality Gate Status](https://sonarcloud.io/api/project_badges/measure?project=MinBZK_bureaublad&metric=alert_status)](https://sonarcloud.io/summary/new_code?id=MinBZK_bureaublad)
![GitHub License](https://img.shields.io/github/license/minbzk/bureaublad)

## Overview

Bureaublad is a flexible dashboard application that aggregates information from multiple open-source components into a unified interface. Users can access essential tools and data from a single location without needing to switch between different applications.

**Key Features:**

- 🔄 **Stateless Design** - All data remains at the source
- 🔌 **Multiple Integrations** - Connects to various productivity tools
- 🔐 **Secure Authentication** - OpenID Connect with Token Exchange support
- 📱 **Modern Interface** - React-based responsive frontend

## Architecture

Bureaublad follows a modern microservices architecture:

- **Frontend:** React SPA (Single Page Application)
- **Backend:** FastAPI REST API
- **Authentication:** OpenID Connect with Token Exchange support

## Integrations

### Currently Supported

| Tool                   | Protocol                                                                                                   | Features                         |
| ---------------------- | ---------------------------------------------------------------------------------------------------------- | -------------------------------- |
| **Calendar & Tasks**   | [CalDav](https://datatracker.ietf.org/doc/html/rfc4791)                                                    | Calendar events, task management |
| **Docs**               | [Docs API](https://github.com/suitenumerique/docs)                                                         | Document management              |
| **Nextcloud/OwnCloud** | [OCS API](https://docs.nextcloud.com/server/stable/developer_manual/client_apis/OCS/ocs-api-overview.html) | Activity feeds                   |
| **Drive**              | [Drive API](https://github.com/suitenumerique/drive)                                                       | File storage and sharing         |
| **Meet**               | [Meet API](https://github.com/suitenumerique/meet)                                                         | Video conferencing               |
| **AI Assistant**       | [OpenAI API](https://github.com/openai/openai-python)                                                      | AI-powered assistance            |

### Planned Integrations

- **Matrix Chat** via [Synapse](https://github.com/element-hq/synapse)

## Quick Start

### Prerequisites

- [Docker](https://docs.docker.com/get-started/get-docker/) installed on your system

### Setup

1. **Clone the repository**

   ```bash
   git clone https://github.com/minbzk/bureaublad.git
   cd bureaublad
   ```

2. **Configure environment**

   ```bash
   cp backend/example.env backend/.env
   ```

3. **Start the application**

   ```bash
   docker compose build
   docker compose up
   ```

### Access the Application

Once started, you can access the following services:

| Service            | URL                                                | Description                     |
| ------------------ | -------------------------------------------------- | ------------------------------- |
| **Frontend**       | <http://localhost:3000>                            | Main application interface      |
| **Backend API**    | <http://localhost:8000>                            | REST API documentation          |
| **Keycloak Admin** | <http://localhost:8080>                            | Identity provider admin console |
| **User Account**   | <http://localhost:8080/realms/mijnbureau/account/> | User account management         |

### Default Credentials

#### Admin Access (Keycloak Master Realm)

```
Username: admin
Password: admin
```

#### User Accounts (MijnBureau Realm)

```
jane@mijnbureau.nl / jane
john@mijnbureau.nl / john
```

## Development

### Technology Stack

- **Frontend:** React with TypeScript, modern hooks and functional components
- **Backend:** FastAPI with Python 3.13, Pydantic v2 for data validation
- **Authentication:** Keycloak with OpenID Connect
- **Containerization:** Docker with multi-service orchestration

### Project Structure

```
bureaublad/
├── backend/          # FastAPI application
├── frontend/         # React application
|-- keycloak/         # Keycloak config
|-- mocks/            # Mocks of integrated tools
|-- scripts/          # Helper scripts
├── compose.yaml      # Docker orchestration
└── README.md         # This file
```

## Requirements

> **Important:** Your identity provider must support [Token Exchange (RFC 8693)](https://datatracker.ietf.org/doc/html/rfc8693) for proper authentication flow. Please verify compatibility before deployment.

## Future Roadmap

- 🔍 Advanced search capabilities across all integrated tools
- ⚙️ User-customizable dashboard layouts and widgets
- 🔗 Additional third-party integrations

## Contributing

We welcome contributions! Please see our contributing guidelines for more information.

## License

This project is licensed under the terms specified in the LICENSE file.
