# Agent Instructions

## Living Knowledge and Documentation

- Treat this file as the project's living operational knowledge. Update it when
  work establishes a durable convention, architectural decision, workflow, or
  constraint that future agents need to follow.
- Keep all documentation and examples aligned with behavior, commands,
  configuration, and workflows. Remove obsolete guidance in the same change.
- Keep guidance concise and factual. Document stable project knowledge rather
  than temporary implementation details or a chronological history.

## Supported Platforms

- DMing must work consistently on Linux and macOS with Python 3.13 and 3.14.
- Keep paths and shell-facing documentation portable across both platforms.

## CLI Compatibility

- `dming` is the grouped CLI entry point. Keep the standalone `roll` command as
  a backward-compatible alias for `dming roll`.
- Chance tables use `dming chance`; do not restore the removed `dming table`
  command.
- Conversion tables use `dming convert`, remain Rich-only and equal-width, and
  put unit abbreviations in column headers. Distance includes 5-foot Squares;
  weight converts pounds to kilograms without a grams column.
- Official 2024 D&D reference tables use the `dming rules` command family and
  must remain aligned with the linked official D&D Beyond sources. Creature
  sizes include feet, meters, and Squares; carrying capacity includes pound and
  kilogram Strength multipliers.

## Code Quality and Verification

- Keep cyclomatic complexity at or below 10. The repository-wide Ruff `C901`
  check is part of `scripts.analyze`; prefer focused helpers over lint
  suppressions.
- Run `uv run --locked python -m scripts.analyze` and
  `uv run --locked python -m scripts.tests` before completing a change.

## Releases and Versions

- Git tags matching `vMAJOR.MINOR.PATCH` are the only release-version source.
  Hatchling and hatch-vcs derive package metadata from Git; never add or edit a
  static package version.
- GitHub Releases are the canonical changelog. Do not add a maintained changelog
  file or a version-bump commit.
- Release tags must point to commits on `main`. The protected release workflow
  builds once, verifies the tag against the artifacts, and publishes those same
  artifacts to PyPI and GitHub after approval.
- DMing does not publish Docker images.
- Release notes are generated from squash commit titles. Use user-visible
  `feat`, `fix`, `perf`, `docs`, `fix(security)`, or dependency-scoped
  `build(deps)`/`chore(deps)` types when applicable.

## Commits

Use [Conventional Commits](https://www.conventionalcommits.org/) for every commit:

```text
<type>(<optional scope>): <description>
```

Use a short, imperative description that summarizes the overall outcome. A
commit body, when useful, must be cohesive prose explaining the reason and
context, not a list of implemented features or code changes.

End every commit message with an `Assisted-by` trailer separated from the body
by a blank line:

```text
Assisted-by: <AI model> <version>
```

Use the actual AI model and version that generated the commit.

## Pull Requests

- Use a Conventional Commit title with a short, imperative summary of the
  overall outcome.
- Write the description as cohesive prose summarizing the change and its reason.
  Do not use a feature list or code-level implementation inventory.
- End the description with the `Assisted-by: <AI model> <version>` trailer.
