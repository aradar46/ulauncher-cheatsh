# Ulauncher cheat.sh Extension

Type `cht <query>` in Ulauncher to show cheat.sh results.

## Examples

- `cht tar`
- `cht python list comprehension`
- `cht python/random list elements`
- `cht ~snapshot`

Selecting a preview result copies the full cheat.sh response to the clipboard. The final result opens the full answer in your browser.

## Install For Local Development

Ulauncher loads extensions from:

```bash
~/.local/share/ulauncher/extensions/
```

Clone or symlink this directory there:

```bash
mkdir -p ~/.local/share/ulauncher/extensions
ln -s "$PWD" ~/.local/share/ulauncher/extensions/ulauncher-cheatsh
```

Restart Ulauncher, then type `cht tar`.

For debugging:

```bash
ulauncher -v
```

## Tests

The test suite covers helper functions that do not require Ulauncher:

```bash
python -m unittest discover -s tests
```

## Notes

This extension uses direct HTTPS requests to `https://cht.sh` and does not require the `cht.sh` command-line client.
