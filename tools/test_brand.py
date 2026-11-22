#!/usr/bin/env python3
"""Validate the organization profile and reproducible identity assets."""
import os
from pathlib import Path
import shutil
import struct
import subprocess
import sys
import tempfile
import unittest
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / "profile" / "assets"
SVG_FILES = ("casbench-logo.svg", "casbench-logo-transparent.svg", "casbench-banner.svg")


class BrandTests(unittest.TestCase):
    def test_profile_and_links(self):
        text = (ROOT / "profile" / "README.md").read_text(encoding="utf-8")
        self.assertIn("assets/casbench-banner.svg", text)
        self.assertTrue((ROOT / "profile" / "assets" / "casbench-banner.svg").is_file())
        self.assertIn("https://github.com/casbench/casbench.github.io", text)
        self.assertIn("https://casbench.github.io/", text)
        self.assertIn("may hide a benchmark error", text)

    def test_svg_sources_and_palette(self):
        for name in SVG_FILES:
            root = ET.parse(ASSETS / name).getroot()
            self.assertEqual(root.tag, "{http://www.w3.org/2000/svg}svg")
            data = (ASSETS / name).read_text(encoding="utf-8")
            self.assertIn("#2E9E5B", data)
            self.assertIn("#F2B705", data)
            self.assertEqual(len(root.findall(".//{http://www.w3.org/2000/svg}circle")), 8)
        self.assertEqual(ET.parse(ASSETS / "casbench-logo.svg").getroot().get("viewBox"), "0 0 512 512")
        self.assertEqual(ET.parse(ASSETS / "casbench-banner.svg").getroot().get("viewBox"), "0 0 1280 300")

    def test_png_exports(self):
        for size in (512, 1024):
            data = (ASSETS / f"casbench-avatar-{size}.png").read_bytes()
            self.assertLess(len(data), 1_000_000)
            self.assertEqual(data[:8], b"\x89PNG\r\n\x1a\n")
            self.assertEqual(struct.unpack(">II", data[16:24]), (size, size))

    def test_generated_svgs_are_reproducible(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "tools").mkdir()
            shutil.copy2(ROOT / "tools" / "generate_brand.py", root / "tools" / "generate_brand.py")
            env = dict(os.environ, PATH="", RSVG_CONVERT="")
            subprocess.run([sys.executable, "-I", str(root / "tools" / "generate_brand.py")], env=env, check=True,
                           stdout=subprocess.DEVNULL)
            for name in SVG_FILES:
                self.assertEqual((root / "profile" / "assets" / name).read_bytes(), (ASSETS / name).read_bytes())


if __name__ == "__main__":
    unittest.main()
