# Data Models

## QueryInput

Source: Ulauncher `KeywordQueryEvent.get_argument()`.

Fields:

- `raw`: optional string from Ulauncher.
- `normalized`: stripped string used for query construction.

Validation:

- Empty or whitespace-only input is treated as missing input.
- The extension does not persist query input.

## CheatSheetResult

In-memory representation only.

Fields:

- `query`: normalized query string.
- `url`: cheat.sh request URL.
- `text`: full plain-text cheat.sh response.
- `preview_items`: list of concise preview rows suitable for Ulauncher result display.

## PreviewItem

In-memory representation only.

Fields:

- `title`: cleaned user-visible summary.
- `description`: optional command or detail associated with the title.
- `copy_text`: text copied when the item is selected.

Validation:

- `text` must contain at least one non-empty non-control line to be considered successful.
- Preview rows are capped to avoid oversized Ulauncher lists.
- cheat.sh metadata lines are never shown as preview rows.
- Command preview rows should copy a command, not the full cheat.sh response.

## ErrorResult

In-memory representation only.

Fields:

- `title`: short user-visible error.
- `description`: actionable detail when possible.

Storage:

- No data is written to disk.
- No local cache exists in the first version.
