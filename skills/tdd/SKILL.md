---
name: tdd
description: Test-driven development (red→green). Use when adding features or fixing bugs test-first, when asked for "tests first" / "red-green", or when touching production logic. The core move is agreeing on the seam — the public boundary to test — before writing anything.
---
# Test-Driven Development

TDD is the red → green loop. This skill is the bar that makes the loop
produce tests worth keeping.

## What a good test is
It verifies behavior **through the public interface**, never the internals.
Rewrite the whole implementation and a good test still passes. It reads like
a spec: "checkout succeeds with a valid cart" tells you in one line that the
capability exists.

## Seams — where tests go
A **seam** is a public boundary where behavior is observable from outside.
Tests go on seams, never inside them.

**Agree on the seams before writing.** You cannot test everything, so ask
"where is the public interface, and which seams deserve tests?" first, and
spend the effort on critical paths and complex logic. Do not write tests on
seams nobody agreed to.

## Anti-patterns (write one of these → discard it and redo)
- **Implementation coupling**: mocking internal collaborators, testing
  private methods, back-door assertions (inspecting the DB instead of the
  interface). Symptom: refactoring breaks tests while behavior is unchanged.
- **Tautology**: computing the expectation the same way the code does
  (`expect(add(a,b)).toBe(a+b)`) — structurally unable to fail. Expectations
  come from an independent source: known-good values, the spec, hand
  calculation.
- **Horizontal slicing**: writing all the tests first, then all the code —
  you end up testing imagined behavior. Go **vertical**: one test → one
  implementation → next. Each test is a tracer round informed by the
  previous cycle.

## Loop rules
- **Red first**: write the failing test, then the minimal code that passes
  it. No speculative features.
- **One slice per cycle**: one seam, one test, one minimal implementation.
- **Refactoring lives outside the loop**: not inside red→green — after it,
  with a review pass.

## With debugging
When fixing a bug, `systematic-debugging` Phase 4 calls this skill: failing
reproduction test first, then the fix.

<!-- Derived from the tdd skill in mattpocock/skills (MIT, Copyright (c) 2026 Matt Pocock), condensed and adjusted. See THIRD_PARTY_NOTICES.md. -->
