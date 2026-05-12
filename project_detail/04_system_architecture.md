# System Architecture

## Layers

### UI Layer

Ulauncher owns the UI. The extension only returns `ExtensionResultItem` objects through `RenderResultListAction`.

### Event Layer

`main.py` subscribes to `KeywordQueryEvent`. The listener extracts the user's query after the `cht` keyword and delegates query construction, fetching, and result formatting to pure helper functions where practical.

### Domain Layer

Domain logic lives in small functions in `main.py`:

- Normalize user query text.
- Build a cheat.sh URL.
- Strip ANSI escape sequences from cheat.sh output.
- Convert text output into preview result rows.

These helpers avoid Ulauncher-specific imports when possible so they can be tested outside Ulauncher.

### Integration Layer

The integration layer performs a bounded HTTPS request to cheat.sh using Python standard library APIs. Network failures are converted to user-visible Ulauncher results instead of raising unhandled exceptions.

## Data Flow

1. Ulauncher sends `KeywordQueryEvent`.
2. Extension reads `event.get_argument()`.
3. Empty query returns a usage/help item.
4. Non-empty query is URL-encoded and sent to cheat.sh.
5. cheat.sh text is normalized and truncated for previews.
6. Ulauncher renders result items.
7. Selecting a result copies the full response to the clipboard.

## Architectural Decisions

- Use direct HTTPS calls instead of shelling out to `curl` or requiring the `cht.sh` CLI. This keeps installation simple and avoids external command dependencies.
- Use `?T` in cheat.sh requests to disable terminal color sequences. ANSI stripping remains in code as defensive cleanup.
- Send a curl-compatible `User-Agent` header because cheat.sh's HTTP interface is primarily optimized for curl-style clients and can return server errors for generic custom agents.
- Keep all files at the extension root, matching Ulauncher tutorial conventions.
- Use `required_api_version` range `^2.0.0` in extension metadata to match common Ulauncher extension manifests and avoid compatibility parsing differences across Ulauncher releases.
- Point `versions.json` at a tested GitHub commit hash. Ulauncher reads `versions.json` first, then downloads the extension from the `commit` branch/tag/hash it declares; using an immutable commit avoids branch cache ambiguity during installation.

## Migration Considerations

Future migrations should preserve the default keyword `cht` unless intentionally documented as a breaking change. For each release, update `versions.json` to point at the new tested commit hash or a release tag and document any release policy change here.
