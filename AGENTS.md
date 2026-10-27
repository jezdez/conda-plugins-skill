# Repository guidance

This repository maintains portable Agent Skills for people developing conda plugins. Its deliverable is the content under `skills/`. It is not a conda plugin or an installable Python package. Python scripts validate and package that content.

## Structure and scope

- Keep installation and client setup in the root `README.md`.
- Keep each `skills/<name>/SKILL.md` short and route substantial guidance to its `references/` directory. Installed skill folders must work on their own.
- Maintain original instructions, concrete examples, and optional pinned provenance. A source link must not substitute for the guidance a colleague needs.
- `scripts/` contains repository checks and archive building. Tests belong in `tests/`.
- Generated archives belong in ignored `dist/`. Never place or commit a ZIP in the repository root.
- Use this checkout and preserve unrelated changes. Do not create another checkout, edit source plugin repositories, or change publication destinations without authorization.

## Skill content

Preserve compatibility with Codex, Claude Code, and Kilo. Use relative links within each skill folder and verify the complete folder is copied by installation tools. Do not assume a local checkout path, a client-specific tool name, or native plugin hooks.

Superpowers, Humanizer, and Ponytail remain required companions for the conda plugin workflow. Codex Security remains optional and applies to an authorized security review. Changes to those requirements need an explicit task requirement.

Read the existing reference before adding another rule. Synthesize reusable decisions from actual plugin instructions and implementations. Distinguish shared defaults from a source project's local choices. Update pinned provenance when changing a sourced claim. Respect standard argparse behavior and reuse conda APIs in examples.

Write user documentation for people. Develop explanations and complete worked examples, use Diátaxis, and apply Humanizer without removing useful depth. The compact skill entry point does not impose a length limit on human-facing documentation. Keep prose direct, avoid semicolons and vague labels, and preserve upstream license text verbatim.

Original work uses Apache License 2.0. Keep the root and each distributed skill's `LICENSE` identical. Preserve applicable upstream attribution and license terms in the skill's `THIRD_PARTY_NOTICES.md`. Companion repositories are installed separately and are not bundled here.

## Tooling and checks

Use the locked Pixi environment. After changing dependencies, tasks, or platforms in `pixi.toml`, run `pixi lock` and include `pixi.lock` in the change.

```sh
pixi run --locked check
pixi run --locked build
pixi run --locked pre-commit
```

`check` runs skill validation, Ruff linting and formatting checks, ty, and the full pytest suite. `build` validates and writes reproducible ZIPs under `dist/`. Use plain parametrized pytest functions, native fixtures, and real temporary files. Do not use mock libraries. Python code uses modern annotations and `from __future__ import annotations`.

For changed code examples or behavior claims, execute the affected examples in a disposable environment. Check documentation markup and recordings when those examples change. Prose-only corrections do not require unrelated conda, Sphinx, or platform runs. For changes to instructions, use a realistic independent application scenario when it would reveal a gap that static validation cannot find.

Do not install skills into the user's global client directories during verification. Keep temporary installation checks isolated. Report local checks, actual client invocation, hosted CI, and publication separately. After a push, take at most one CI snapshot unless asked to monitor it.

## Contributions

Follow `CONTRIBUTING.md`, `CODE_OF_CONDUCT.md`, and `SECURITY.md`. Use concise commit subjects and the repository's PR template. Do not prefix PR titles with `[codex]` or put validation commands and output in PR descriptions. Keep review findings in the chat unless their publication is authorized. Opening an issue in another repository requires explicit approval of the proposed issue.
