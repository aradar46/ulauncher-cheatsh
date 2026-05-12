import unittest

from cheatsh import build_cheatsh_url, normalize_query, preview_items, preview_lines, strip_ansi


class CheatShHelperTests(unittest.TestCase):
    def test_normalize_query_collapses_whitespace(self):
        self.assertEqual(
            normalize_query("  python   list   comprehension  "),
            "python list comprehension",
        )

    def test_build_cheatsh_url_preserves_namespaces_and_encodes_spaces(self):
        self.assertEqual(
            build_cheatsh_url("python/random list elements"),
            "https://cht.sh/python/random+list+elements?T",
        )

    def test_build_cheatsh_url_strips_outer_slashes(self):
        self.assertEqual(build_cheatsh_url("/tar/"), "https://cht.sh/tar?T")

    def test_strip_ansi_removes_color_sequences(self):
        self.assertEqual(strip_ansi("\x1b[31mred\x1b[0m"), "red")

    def test_preview_lines_skips_blanks_and_truncates(self):
        lines = preview_lines("\nfirst\n\n" + ("x" * 100), max_lines=2, max_line_length=10)

        self.assertEqual(lines, ("first", "xxxxxxxxx..."))

    def test_preview_items_hide_metadata_and_pair_comments_with_commands(self):
        items = preview_items(
            "\n".join(
                [
                    "#[cheat:docker]",
                    "# To start the docker daemon:",
                    "docker -d",
                    "",
                    "# To list containers:",
                    "docker ps",
                ]
            )
        )

        self.assertEqual(items[0].title, "start the docker daemon")
        self.assertEqual(items[0].description, "docker -d")
        self.assertEqual(items[0].copy_text, "docker -d")
        self.assertEqual(items[1].title, "list containers")
        self.assertEqual(items[1].description, "docker ps")
        self.assertEqual(items[1].copy_text, "docker ps")

    def test_preview_items_skip_prose_when_command_examples_exist(self):
        items = preview_items(
            "\n".join(
                [
                    "# tar",
                    "# GNU version of the tar archiving utility",
                    "# Long prose that should not become a launcher result " * 4,
                    "tar -xvf /path/to/foo.tar",
                    "",
                    "# To create an archive:",
                    "tar -cvf /path/to/foo.tar /path/to/foo/",
                ]
            )
        )

        self.assertEqual(items[0].title, "create an archive")
        self.assertEqual(items[0].description, "tar -cvf /path/to/foo.tar /path/to/foo/")


if __name__ == "__main__":
    unittest.main()
