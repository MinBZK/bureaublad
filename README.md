# Mijn Bureaublad

This is a portal that consolidates important features from multiple opensource tools into on entry point for the user.



## Getting Started

To get started you will need `docker engine` and `docker compose` installed.

```sh
docker compose build
docker compose up
```

## Solution Architecture

The idea behind this tool is to consolidate important features from multiple tools into one place for the users. This will be the landing place from which they acces all other tools.

The tools consists of two main containers. A backend and a frontend. The frontend is a SPA application and the backend a REST api. In the future we will add a websocket, but is not in scope for the first version. Other containers will be a OpenID connect authentication system with a Token Exchange. We assume that the user can access all other tools through an OpenID connect system so that we can use the token exchange to access all other resources as the user. 

We may add a search feature where information is streamed into from other tools. 


### C4 model

We use the C4 model to make a diagram of the tools.

```mermaid
   C4Context
      title System Context diagram for Mijn Portal
```



## Technical Architecture

The current tools we use try to adhere to the tools uses by our partners so we can cooperate better. Which means we will use [django rest framework](https://www.django-rest-framework.org/) and [react](https://react.dev/). 
