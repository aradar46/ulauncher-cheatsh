# Frontend Architecture

## UI Ownership

The extension does not render its own frontend. Ulauncher renders all visible UI from result item objects returned by the extension.

## Result Item Design

The extension returns:

- A usage item when no query is provided.
- One or more command-focused preview items for successful cheat.sh responses.
- A lower-priority copy-full-result item.
- A browser fallback item that opens the full cheat.sh URL.
- An error item when the network request fails or cheat.sh returns no useful content.

Preview items are structured for Ulauncher rather than mirroring raw cheat.sh output:

- cheat.sh metadata lines such as `#[cheat:docker]` are hidden.
- Comment markers such as `# To start...` are removed from titles.
- The task/explanation becomes the result title.
- The command becomes the result description and copied text.
- Long prose-only blocks are skipped when command examples are available.
- Repeated instructional descriptions are avoided so the list stays scannable.

## Interaction Behavior

Selecting a command preview item copies that command to the clipboard and hides the Ulauncher window. Selecting the copy-full item copies the full cheat.sh response. Selecting the browser item opens the cheat.sh query in the default browser.

## Visual Assets

The extension uses `images/icon.svg` for manifest and result item icons. The asset is local and has no runtime network dependency.
