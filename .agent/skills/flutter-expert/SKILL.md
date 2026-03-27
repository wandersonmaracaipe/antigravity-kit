---
name: flutter-expert
description: Flutter 3.29+ architecture and performance patterns. Covers state management decisions, rendering performance, platform integration, and release hardening.
allowed-tools: Read, Write, Edit, Glob, Grep, Bash
---

# Flutter Expert

> Flutter apps should be smooth (60/120fps), testable, and platform-aware.

## 1) State Management Decision

Choose by complexity:
- Small feature: `setState` + local state
- Medium app: Riverpod/Provider
- Complex domain workflows: BLoC/Cubit or layered Riverpod architecture

## 2) UI & Rendering Performance

- Prefer const widgets whenever possible
- Minimize unnecessary rebuilds (selectors, split widgets)
- Use lazy lists (`ListView.builder`, `SliverList`)
- Offload heavy work from UI thread (isolates)
- Profile with DevTools before optimization

## 3) Architecture

- Feature-first folders for product scalability
- Keep presentation, domain, and data concerns separated
- Repository abstraction for API/local cache strategy
- Handle offline-first where product requires resiliency

## 4) Platform Integration

- Respect iOS and Android navigation/interaction conventions
- Use platform channels only when package ecosystem is insufficient
- Guard permissions with explicit UX and graceful fallbacks

## 5) Testing Strategy

- Unit tests for domain and mappers
- Widget tests for UI logic
- Integration tests for critical user journeys

## 6) Release Hardening

- Crash reporting and performance telemetry
- Flavor/environment separation
- Secure storage for sensitive tokens
- Size and startup budget monitoring

## 7) Anti-Patterns

- Giant StatefulWidget with mixed business logic
- setState over entire screen for tiny UI changes
- Blocking sync work in UI isolate
- Ignoring frame drops and jank in release targets
