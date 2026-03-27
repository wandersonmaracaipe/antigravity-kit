---
name: php-laravel12
description: PHP 8.4+ and Laravel 12 engineering patterns. Covers architecture, Eloquent performance, queues, events, API security, and production hardening.
allowed-tools: Read, Write, Edit, Glob, Grep, Bash
---

# PHP & Laravel 12

> Build maintainable Laravel 12 systems with clear architecture, predictable performance, and strong security defaults.

## 1) Stack Decision

Use **Laravel 12** when you need:
- Fast delivery with batteries included
- Strong ecosystem (auth, queues, cache, jobs, events)
- Monolith-first with clean modular boundaries

Use lighter PHP stack (Slim/Symfony micro-kernel) when:
- Ultra-minimal runtime surface
- Very constrained microservice
- You do not need full Laravel subsystems

## 2) Architecture Rules

- Prefer **Controller -> Action/Service -> Repository/Model** boundaries
- Keep controllers thin (HTTP concerns only)
- Business rules belong in service/action layer
- Use FormRequest for validation and authorization boundaries
- Use policies/gates for authorization, never inline role checks everywhere

## 3) Data & Eloquent Performance

- Prevent N+1 with eager loading (`with`, `loadMissing`)
- Use DTO/Resource for API output shape control
- Add indexes based on real query patterns
- For high-volume writes, use chunking/batch updates carefully
- Prefer query scopes for reusable filters

## 4) Async & Reliability

- Queue long tasks (mail, webhooks, reports)
- Make jobs idempotent (retry-safe)
- Use outbox-style pattern for critical integrations
- Add dead-letter/failed job strategy with alerting

## 5) API Security Defaults

- Validate all input (FormRequest)
- Use rate limits per route profile
- Prefer token/session strategy by product requirement (Sanctum/Passport)
- Never expose internal exception payloads
- Enforce audit logging for sensitive actions

## 6) Laravel 12 Production Checklist

- Env isolation + secret management
- Config/cache route optimization in release pipeline
- DB migration strategy with rollback plan
- Queue worker supervision and health checks
- Observability: logs, metrics, traces, slow query monitoring

## 7) Anti-Patterns

- Fat controllers with business logic
- Unbounded eager loading of huge graphs
- Synchronous external API calls on request path without timeout/circuit protection
- Role checks duplicated in multiple layers instead of centralized policy
