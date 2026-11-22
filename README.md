# CASbench organization profile

This repository contains the public organization profile in `profile/README.md` and its visual identity in `profile/assets/`. The benchmark suite and its sources are in [casbench.github.io](https://github.com/casbench/casbench.github.io).

The organization mark extends [the benchmark site's existing results-matrix mark](https://github.com/casbench/casbench.github.io/tree/main/assets/brand) by Sébastien Celles: filled green dots, hollow yellow dots and an empty cell. This adaptation was prepared with AI assistance and awaits contributor review. It uses the same ink, off-white, steel, green and yellow palette. The profile banner deliberately contains no benchmark measurements.

- `casbench-logo.svg`: primary mark on the ink background.
- `casbench-logo-transparent.svg`: mark for a separately chosen background.
- `casbench-avatar-512.png` and `casbench-avatar-1024.png`: square, circular-crop-safe avatar exports.
- `casbench-banner.svg`: organization profile banner.

Regenerate the SVG files with `python3 -I tools/generate_brand.py`. With `rsvg-convert` on `PATH`, the same command also generates the two PNG files. Alternatively set `RSVG_CONVERT` to its executable path. The committed PNGs were rendered with librsvg 2.62.4. The original benchmark identity and this adaptation are CC BY 4.0; see [LICENSE](LICENSE).

Suggested organization description: “Reproducible benchmarks for computer algebra systems.” Suggested website: `https://casbench.github.io/`.

The profile README becomes visible after it is committed to the default branch of the public `.github` repository. The avatar PNG is a separate upload in the organization settings; committing it alone does not change the organization picture.
