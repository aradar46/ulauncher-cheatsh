# Project Overview

## Purpose

This project is a Ulauncher extension that lets a user type `cht <query>` and see results from the cheat.sh service inside Ulauncher.

## User Workflow

1. The user opens Ulauncher.
2. The user types the configured keyword, default `cht`, followed by a query.
3. The extension requests `https://cht.sh/<query>?T`.
4. The extension renders command-focused Ulauncher result items.
5. Selecting a command result copies that command to the clipboard and hides Ulauncher.
6. Lower-priority actions allow copying the full cheat.sh response or opening it in a browser.

## Source Of Truth

`project_detail/` documents the extension behavior, boundaries, and known risks. Implementation changes that affect behavior, data flow, packaging, or external contracts must update these documents first.

## External Dependencies

- Ulauncher Extension API v2.
- Python standard library for HTTP requests, URL encoding, and timeout handling.
- cheat.sh HTTP service at `https://cht.sh`.

## Non-Goals

- No local cheat.sh mirror is bundled.
- No persistent cache is implemented in the first version.
- No React, Capacitor, Android, Firestore, or localStorage layer exists in this project.

## Current Status

Usable local extension with command-focused result formatting, tests, and publish-ready README.
