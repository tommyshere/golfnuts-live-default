# golfnuts-live-default

AWS Lambda handler for the `$default` route of the GolfNuts Live WebSocket API.

## Purpose

This function handles any incoming WebSocket messages that don't match a specific route. It serves as a catch-all handler for client-to-server communication.

## How It Works

1. Client sends a message over an established WebSocket connection
2. API Gateway routes the message to this Lambda via the `$default` route
3. The handler processes the message and returns a response

## Current State

Currently returns a simple success response. Can be extended to handle:
- Subscribing to specific round updates
- Client heartbeat/ping messages
- Custom client commands

## Infrastructure

- **Trigger:** API Gateway WebSocket `$default` route

## Related Services

- `golfnuts-live-connect` - Stores connection IDs when clients connect
- `golfnuts-live-disconnect` - Removes connection IDs when clients disconnect
