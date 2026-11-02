# Contributing

This repository collects practices for colleagues developing conda plugins with Codex, Claude Code, and Kilo. Useful contributions explain a development decision, provide a worked example, or correct guidance that no longer matches the supported APIs.

Read [AGENTS.md](AGENTS.md) for repository rules and [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md) for participation expectations. If the question concerns a particular plugin's implementation, use this repository to improve the general guidance and keep implementation changes in that plugin's own project.

## Set up the repository

Use [Pixi](https://pixi.sh/) to create the locked development environment:

```sh
pixi install --locked
pixi run --locked check
```

The environment contains Python, PyYAML, pytest, Ruff, ty, and pre-commit. It does not install the skill or its companions into your agent clients. Follow the [README setup instructions](README.md#install-with-npx) when you want to use them.

## Change a skill

Start with the reader's task and the existing reference that covers it. Keep `SKILL.md` focused on discovery, essential requirements, and routing. Put substantial examples and domain guidance in the relevant reference. Preserve complete standalone skill folders, including license notices.

Verify API and tool claims against the supported version or current upstream source. Record pinned examples in the source reference. Explain which rules are general defaults and which belong to one source plugin. Apply Humanizer to prose while keeping the technical facts and the detail needed by a human reader.

Run the checks and rebuild the distribution:

```sh
pixi run --locked check
pixi run --locked build
pixi run --locked pre-commit
```

The validator checks skill metadata, supported Markdown links and anchors, standalone references, and distribution notices. It does not execute examples or prove that an agent follows the instructions. Execute changed examples and use a realistic application scenario for substantial instruction changes. Keep tests that exercise observable behavior, such as a broken link or an archive missing a notice.

When changing `pixi.toml`, run `pixi lock` and include the updated lockfile. `pixi run --locked build` writes `dist/conda-plugins.zip`. Generated files stay untracked and out of the repository root. Inspect the ZIP before sharing it with the intended audience.

## Test installation on Linux, macOS, and Windows

Run the [installation check workflow](https://github.com/jezdez/conda-plugin-skills/actions/workflows/setup.yml) from GitHub Actions to test the pinned copy-installation fixture in `scripts/check_setup.py`. It runs only on manual dispatch, using fresh Linux, macOS, and Windows runners. Windows uses Git Bash. The check installs from the live GitHub sources into the runner's initially empty skill directories, compares the installed files with their source revisions, checks Bash helper syntax, and asks each client to list its skills without sending a model prompt.

The fixture retains Skills CLI 1.7.4 and the former README setup command for repeatable installer behavior. It does not test all versions or installation methods described by the upstream docs. It fetches skills from the source repositories' default branches, so a successful run does not validate unpublished skill changes on your branch.

The workflow saves a verification summary as a private artifact for seven days. It records source revisions, file checks, and client discovery results. The test script requires a GitHub-hosted runner and empty client skill directories to guard against accidental local installations. Model behavior and native plugin hooks need separate checks.

## Propose the change

Keep changes focused and describe the problem and resulting behavior. Update [CHANGELOG.md](CHANGELOG.md) for user-visible guidance, installation, or packaging changes. Follow the PR template. Share check results separately from the PR description.

Report security concerns through the private route in [SECURITY.md](SECURITY.md). Contributions of original material use [Apache License 2.0](LICENSE). Retain the applicable licenses and attribution for adapted material.
