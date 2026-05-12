"""cheat.sh query and formatting helpers for the Ulauncher extension."""

from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Iterable, Optional, Tuple
from urllib.error import HTTPError, URLError
from urllib.parse import quote_plus
from urllib.request import Request, urlopen

DEFAULT_BASE_URL = "https://cht.sh"
DEFAULT_TIMEOUT_SECONDS = 3.5
USER_AGENT = "curl/8.5.0 ulauncher-cheatsh/0.1"
MAX_PREVIEW_LINES = 7
MAX_PREVIEW_LINE_LENGTH = 88
MAX_COMMAND_TITLE_LENGTH = 82
MAX_COMMENT_BLOCK_LENGTH = 180

ANSI_ESCAPE_RE = re.compile(r"\x1b\[[0-?]*[ -/]*[@-~]")


class CheatShError(Exception):
    """Raised when cheat.sh cannot return a usable response."""


@dataclass(frozen=True)
class PreviewItem:
    title: str
    description: str = ""
    copy_text: str = ""


@dataclass(frozen=True)
class CheatSheetResult:
    query: str
    url: str
    text: str
    preview_items: Tuple[PreviewItem, ...]


def normalize_query(query: Optional[str]) -> str:
    """Return a stripped query suitable for cheat.sh path generation."""
    return " ".join((query or "").strip().split())


def build_cheatsh_url(query: str, base_url: str = DEFAULT_BASE_URL) -> str:
    """Build a cheat.sh URL while preserving slash-separated namespaces."""
    normalized = normalize_query(query).strip("/")
    if not normalized:
        raise ValueError("query must not be empty")

    encoded_segments = [
        quote_plus(segment, safe=":")
        for segment in normalized.split("/")
        if segment
    ]
    return f"{base_url.rstrip('/')}/{'/'.join(encoded_segments)}?T"


def strip_ansi(text: str) -> str:
    return ANSI_ESCAPE_RE.sub("", text)


def truncate_line(line: str, max_length: int = MAX_PREVIEW_LINE_LENGTH) -> str:
    if len(line) <= max_length:
        return line
    return f"{line[: max_length - 1]}..."


def clean_comment_line(line: str) -> str:
    cleaned = line.lstrip("#").strip()
    if not cleaned or cleaned == "---" or cleaned.startswith("tags:"):
        return ""
    if cleaned.lower().startswith("to "):
        cleaned = cleaned[3:]
    return cleaned.rstrip(":").strip()


def is_metadata_line(line: str) -> bool:
    return line.startswith("#[") and line.endswith("]")


def visible_lines(text: str) -> Tuple[str, ...]:
    return tuple(line.strip() for line in strip_ansi(text).splitlines() if line.strip())


def content_lines(text: str) -> Tuple[str, ...]:
    return tuple(line.strip() for line in strip_ansi(text).splitlines())


def prefer_compact_cheat_section(lines: Tuple[str, ...]) -> Tuple[str, ...]:
    for index, line in enumerate(lines):
        if line.startswith("#[cheat:"):
            return lines[index:]
    return lines


def is_comment_line(line: str) -> bool:
    return line.startswith("#")


def is_yaml_noise(line: str) -> bool:
    return line == "---" or line.startswith("tags:")


def is_probable_command(line: str) -> bool:
    if not line or is_comment_line(line) or is_yaml_noise(line):
        return False
    if line.startswith("[") and "]:" in line:
        return False
    if len(line) > 140:
        return False
    return True


def split_blocks(lines: Tuple[str, ...]) -> Tuple[Tuple[str, ...], ...]:
    blocks = []
    current = []

    for line in lines:
        if not line:
            if current:
                blocks.append(tuple(current))
                current = []
            continue
        if is_metadata_line(line):
            if current:
                blocks.append(tuple(current))
                current = []
            continue
        if is_yaml_noise(line):
            continue
        if is_comment_line(line) and clean_comment_line(line) == "":
            if current:
                blocks.append(tuple(current))
                current = []
            continue
        current.append(line)

    if current:
        blocks.append(tuple(current))

    return tuple(blocks)


def title_from_comments(comments: Tuple[str, ...], command: str) -> str:
    cleaned = [clean_comment_line(comment) for comment in comments]
    cleaned = [comment for comment in cleaned if comment]

    if not cleaned:
        return command

    short_comments = [comment for comment in cleaned if len(comment) <= MAX_COMMAND_TITLE_LENGTH]
    if short_comments:
        return short_comments[-1]

    return cleaned[0]


def command_preview_items(
    lines: Tuple[str, ...],
    max_items: int,
    max_line_length: int,
) -> Tuple[PreviewItem, ...]:
    items = []

    for block in split_blocks(lines):
        comments = tuple(line for line in block if is_comment_line(line))
        commands = tuple(line for line in block if is_probable_command(line))
        if not commands:
            continue
        comment_text_length = sum(len(clean_comment_line(comment)) for comment in comments)
        if comment_text_length > MAX_COMMENT_BLOCK_LENGTH:
            continue

        for command in commands:
            title = title_from_comments(comments, command)
            items.append(
                PreviewItem(
                    title=truncate_line(title, max_line_length),
                    description=truncate_line(command, max_line_length),
                    copy_text=command,
                )
            )
            if len(items) >= max_items:
                return tuple(items)

    return tuple(items)


def preview_items(
    text: str,
    max_items: int = MAX_PREVIEW_LINES,
    max_line_length: int = MAX_PREVIEW_LINE_LENGTH,
) -> Tuple[PreviewItem, ...]:
    command_items = command_preview_items(
        prefer_compact_cheat_section(content_lines(text)),
        max_items,
        max_line_length,
    )
    if command_items:
        return command_items

    lines = visible_lines(text)
    items = []
    index = 0

    while index < len(lines):
        line = lines[index]
        if is_metadata_line(line):
            index += 1
            continue

        if line.startswith("#"):
            title = clean_comment_line(line)
            description = ""
            if index + 1 < len(lines):
                next_line = lines[index + 1]
                if not next_line.startswith("#") and not is_metadata_line(next_line):
                    description = truncate_line(next_line, max_line_length)
                    index += 1

            if title:
                items.append(
                    PreviewItem(
                        title=truncate_line(title, max_line_length),
                        description=description,
                        copy_text=line,
                    )
                )
        else:
            items.append(
                PreviewItem(
                    title=truncate_line(line, max_line_length),
                    copy_text=line,
                )
            )

        if len(items) >= max_items:
            break
        index += 1

    if items:
        return tuple(items)

    fallback = [
        PreviewItem(title=truncate_line(line, max_line_length), copy_text=line)
        for line in lines
        if not is_metadata_line(line)
    ]
    return tuple(fallback[:max_items])


def preview_lines(
    text: str,
    max_lines: int = MAX_PREVIEW_LINES,
    max_line_length: int = MAX_PREVIEW_LINE_LENGTH,
) -> Tuple[str, ...]:
    return tuple(
        item.title
        for item in preview_items(
            text,
            max_items=max_lines,
            max_line_length=max_line_length,
        )
    )


def fetch_text(url: str, timeout: float = DEFAULT_TIMEOUT_SECONDS) -> str:
    request = Request(url, headers={"User-Agent": USER_AGENT})

    try:
        with urlopen(request, timeout=timeout) as response:
            body = response.read()
    except HTTPError as exc:
        raise CheatShError(f"cheat.sh returned HTTP {exc.code}") from exc
    except TimeoutError as exc:
        raise CheatShError("cheat.sh request timed out") from exc
    except URLError as exc:
        detail = getattr(exc, "reason", exc)
        raise CheatShError(f"could not reach cheat.sh: {detail}") from exc

    return body.decode("utf-8", errors="replace")


def query_cheatsh(query: str, timeout: float = DEFAULT_TIMEOUT_SECONDS) -> CheatSheetResult:
    normalized = normalize_query(query)
    if not normalized:
        raise ValueError("query must not be empty")

    url = build_cheatsh_url(normalized)
    text = strip_ansi(fetch_text(url, timeout=timeout)).strip()
    previews = preview_items(text)

    if not previews:
        raise CheatShError("cheat.sh returned an empty response")

    return CheatSheetResult(
        query=normalized,
        url=url,
        text=text,
        preview_items=previews,
    )


def join_description(parts: Iterable[str]) -> str:
    return " | ".join(part for part in parts if part)
