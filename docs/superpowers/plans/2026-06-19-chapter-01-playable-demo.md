# Chapter 01 Playable Demo Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build a local playable browser demo for Chapter 01 of 《超GAG机器人大战：万机残响》.

**Architecture:** Use a zero-dependency static web app with a tested pure JavaScript state engine. Story, exploration nodes, tactical battles, choices, variables, and gallery entries are data-driven, while the UI renders the current mode from state.

**Tech Stack:** Native ES modules, Node 22 built-in `node:test`, browser DOM APIs, CSS pixel-art style, local static Node server.

---

### Task 1: Core State Engine

**Files:**
- Create: `demo/chapter1/package.json`
- Create: `demo/chapter1/tests/engine.test.js`
- Create: `demo/chapter1/src/content.js`
- Create: `demo/chapter1/src/engine.js`

- [ ] Write tests for chapter progression, variables, battle outcomes, and resource trade-offs.
- [ ] Run `npm test` in `demo/chapter1` and verify tests fail because engine files do not exist yet.
- [ ] Implement content data and pure engine functions.
- [ ] Run `npm test` and verify all tests pass.

### Task 2: Playable Browser UI

**Files:**
- Create: `demo/chapter1/index.html`
- Create: `demo/chapter1/src/styles.css`
- Create: `demo/chapter1/src/app.js`
- Create: `demo/chapter1/server.mjs`

- [ ] Render actual game as first screen: chapter rail, stage view, dialogue box, choices, codex, variables, and gallery.
- [ ] Support exploration choices, story dialogue, two tactical battle scenes, resource choice, and chapter settlement.
- [ ] Add GBA-memory visual language: tight panels, pixel grid, Q unit chips, mecha pose cards, fire/legal scan effects.
- [ ] Run local server and verify the UI loads.

### Task 3: Verification And Handoff

**Files:**
- Modify: `demo/chapter1/README.md`

- [ ] Add run instructions and known demo boundaries.
- [ ] Run `npm test`.
- [ ] Run a browser smoke check against local server.
- [ ] Report demo URL, files, verification evidence, and remaining design issues surfaced by the build.
