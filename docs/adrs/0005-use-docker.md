# Title

Date: `2024-01-13`

## Status

Proposed

## Context

The application will be deployed on a server. To ensure proper operation after deployment, it is
recommended to use Docker and Docker Compose.

## Decision

We will be using Docker as part of the initial setup in order to make sure in the very beginning
that code written locally will work inside a container.

## Consequences

Risk of incorrect working outside local development environment is mitigated.

## Keywords

- docker
- docker compose
- deployment
