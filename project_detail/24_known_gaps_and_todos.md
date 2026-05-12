# Known Gaps And Todos

## Gaps

- No persistent cache exists, so the extension requires network access for every non-empty query.
- There is no packaged PNG icon; the first version uses an SVG icon.
- Ulauncher API imports are not available in a plain test environment, so unit tests focus on helper functions rather than full Ulauncher event integration.

## Todos

- Consider adding configurable timeout and result count preferences.
- Consider adding a disk cache for recent queries if repeated network calls become slow.
- Capture and keep an up-to-date screenshot for `README.md` and ext.ulauncher.io publishing.
- Replace the placeholder GitHub repository URL in `README.md` after the public repository is created.
