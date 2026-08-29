# Development Instructions

## Setup

Install uv:

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
# or on macOS
brew install uv
```

Create the project environment and install the locked development dependencies:

```bash
uv sync --locked
```

Install the pre-commit hooks:

```bash
uv run pre-commit install
```

Run the grouped DMing CLI:

```bash
uv run dming --help
uv run dming roll 2d20kh1
uv run dming chance d20+5
uv run dming convert distance
uv run dming convert weight
uv run dming rules sizes
```

The standalone `uv run roll <dice>` executable remains a backward-compatible
shortcut for `uv run dming roll <dice>`.

## CLI Structure

- `dming roll` handles dice expressions; only roll output supports `--details`
  and `--plain`.
- `dming chance` renders single-die threshold probabilities.
- `dming convert distance` renders inches, feet, and miles in metric units and
  5-foot Squares. `dming convert weight` renders pounds in kilograms.
- `dming rules` renders immutable 2024 D&D reference data for abilities,
  carrying capacity, Difficulty Classes, Proficiency Bonus, and creature sizes.

Chance, conversion, and rules tables are Rich-only. Measurement columns put
their unit abbreviations in the headers. All conversion tables share one width,
and creature-size references show both feet and meters.

## Verification

Apply code styles:

```bash
uv run --locked python -m scripts.styles
```

Run code analysis:

```bash
uv run --locked python -m scripts.analyze
```

Run unit tests:

```bash
uv run --locked python -m scripts.tests
```

Build the distributions:

```bash
uv build --clear
```

## Release

Git tags are the only source of release versions. Package metadata is derived from
the nearest semantic version tag by `hatch-vcs`; never edit a version field or a
changelog file for a release. GitHub Releases are the canonical release history.

Before releasing, ensure `main` is current, clean, and passing CI:

```bash
git switch main
git pull --ff-only origin main
git status --short
uv lock --check
uv run --locked python -m scripts.analyze
uv run --locked python -m scripts.tests
```

Choose the next version according to [Semantic Versioning](https://semver.org/),
then create and push an annotated tag:

```bash
git tag -a v0.2.0 -m "Release v0.2.0"
git push origin v0.2.0
```

The release workflow validates that the tag is exactly `vMAJOR.MINOR.PATCH` and
points to a commit on `main`. It then tests and builds the distributions, verifies
the release version, generates notes from Conventional Commits, attests and
publishes the package to PyPI, and creates the GitHub Release. DMing does not
publish a Docker image.

Configure the PyPI trusted publisher for owner `sauljabin`, repository `dming`,
workflow `release.yml`, and environment `release`. GitHub release creation uses
the built-in token and needs no personal access token.

If publishing fails, do not move the tag or create a replacement version commit.
Fix the external configuration if necessary and rerun only the failed GitHub
Actions jobs. PyPI artifacts are immutable; if an incorrect artifact was already
published, create a new patch version instead of reusing the tag.
