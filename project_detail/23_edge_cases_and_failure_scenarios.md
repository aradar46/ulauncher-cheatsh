# Edge Cases And Failure Scenarios

## Empty Query

When the user types only `cht`, the extension shows usage examples instead of calling cheat.sh.

## Slow Or Unavailable Network

The cheat.sh request uses a short timeout. On timeout or connection failure, the extension returns an error result and a browser fallback item.

## cheat.sh HTTP Error

HTTP failures are caught and displayed as user-visible errors.

The extension uses a curl-compatible `User-Agent` to avoid cheat.sh server errors observed with arbitrary custom user agents. If cheat.sh changes this behavior later, the fallback is still a visible HTTP error item plus browser-open option.

## ANSI Or Control Formatting

The request uses `?T` to disable terminal colors. The extension also strips ANSI escape codes defensively before previewing and copying content.

## Long Responses

cheat.sh can return long answers. The extension limits preview rows and line lengths while keeping the full response available through a dedicated copy-full item. If no structured command examples are found, the extension falls back to cleaned non-empty lines and copies the full response for those fallback rows.

## Query Namespaces

Users may include slashes for cheat.sh namespaces, such as `python/list append`. The URL builder preserves slashes and encodes each path segment separately.

## Service Semantics

cheat.sh may return generated StackOverflow-style answers, not only static cheat sheets. The extension treats cheat.sh as the authority for returned content and does not validate technical correctness.
