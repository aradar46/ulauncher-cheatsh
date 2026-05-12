# Storage Strategy

## Persistence

The extension does not persist user data, responses, cache entries, preferences, or history.

## Ulauncher Preferences

The configured keyword is stored by Ulauncher, not by this extension. The manifest defines the default keyword as `cht`.

## Offline Behavior

There is no offline cache. If cheat.sh cannot be reached, the extension displays a network failure result.

## Future Cache Consideration

A future cache could store recent query responses on disk, but that would require documenting:

- Cache location.
- Expiration rules.
- Privacy implications.
- Failure fallback order.
- Migration and cleanup behavior.
