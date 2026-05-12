# Business Logic

## Keyword Behavior

The default keyword is `cht`. Users can override it through Ulauncher preferences.

## Query Construction

The extension maps user text to cheat.sh paths:

- `cht tar` -> `https://cht.sh/tar?T`
- `cht python list comprehension` -> `https://cht.sh/python+list+comprehension?T`
- `cht python/random list elements` -> `https://cht.sh/python/random+list+elements?T`

Spaces are encoded as `+`. Existing slashes are preserved so users can target cheat.sh namespaces.

Requests include a curl-compatible `User-Agent`. This is an integration compatibility rule for cheat.sh and does not require the local `curl` binary to be installed.

## Result Formatting

Ulauncher preview rows are command-focused. The user should be able to scan tasks and copy a useful command with Enter:

- Blank lines are ignored for preview extraction.
- ANSI escape codes are stripped defensively.
- cheat.sh metadata lines are ignored.
- Leading shell/comment markers are removed from explanatory titles.
- A comment followed by a command becomes one result row where the comment is the title, the command is the description, and Enter copies the command.
- Long prose-only blocks are skipped when command examples are available.
- The full cheat.sh response is available through a separate lower-priority copy row.
- Very long preview lines are shortened.
- The preview list is capped.

## Failure Handling

The extension must return Ulauncher result items for failures instead of crashing:

- Missing query: show usage examples.
- Timeout or network failure: show an error item and browser fallback.
- HTTP error: show status-aware error detail where available.
- Empty response: show an empty-result item and browser fallback.

## Rationale

Ulauncher result views are compact and action-oriented. The best default action is copying a specific command, while full-answer copy and browser open remain available for deeper reading.
