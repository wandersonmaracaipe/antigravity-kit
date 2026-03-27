---
name: go-patterns
description: Go 1.24+ backend and systems patterns. Concurrency, context propagation, API design, observability, and production-grade service architecture.
allowed-tools: Read, Write, Edit, Glob, Grep, Bash
---

# Go Patterns

> Idiomatic Go favors simplicity, explicit errors, context-aware cancellation, and measurable performance.

## 1) Project Shape

Use layered modules:
- `cmd/` entrypoints
- `internal/` private app logic
- `pkg/` reusable components (only when truly reusable)
- `api/` contracts (OpenAPI/proto)

## 2) Concurrency Rules

- Pass `context.Context` as first parameter in request-scoped operations
- Use goroutines only with bounded fan-out
- Use worker pools for controlled concurrency
- Avoid goroutine leaks: every goroutine must have cancellation/exit condition

## 3) API Design

- Keep handlers thin; service layer handles business rules
- Validate input at boundaries
- Return structured errors (machine code + user-safe message)
- Use timeouts for all external calls (DB, HTTP, queue)

## 4) Data & Performance

- Measure before optimizing (pprof, tracing, benchmarks)
- Keep allocations low in hot paths
- Prefer clear code over micro-optimizations unless benchmarked
- Use connection pools with explicit limits

## 5) Reliability & Ops

- Graceful shutdown with context cancellation
- Health/readiness endpoints
- Retries with backoff + jitter (idempotent operations only)
- Circuit breaking for unstable dependencies

## 6) Security Defaults

- Strict input validation
- Safe HTTP headers and request body limits
- Secret handling via env/secret manager
- Dependency and vulnerability scanning in CI

## 7) Anti-Patterns

- Ignoring context cancellation
- Panics for expected error paths
- Unbounded goroutines in loops
- Global mutable state without synchronization strategy
