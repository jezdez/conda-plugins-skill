# Documentation and terminal demos

Use this guide when writing or reviewing a plugin's README, documentation site, tutorials, examples, or demo recordings. Follow the target repository's documentation instructions and existing presentation. The patterns below come from the plugin sources listed in [sources.md](sources.md#documentation-and-demos).

## Write for people who want to learn and explore

Write for the person installing, using, or maintaining the plugin. Establish what they want to accomplish, what they already know, and what they need explained. Keep agent procedures in `AGENTS.md` and skill instructions. User documentation should explain the product through the reader's tasks.

Documentation should be expansive enough to teach. Develop the explanation, supply complete worked examples, and give readers ways to explore related topics. The skill's compact routing and the preference for small implementations do not impose a length limit on user documentation. Let the reader's needs determine the depth.

Introduce unfamiliar terms before using them in instructions. For example, explain the difference between a requested package specification and a resolved package record before asking someone to choose an export format. Explain what a command changes, where its result goes, and how the reader can recognize success. Show realistic configuration and output, with commentary on the parts that matter.

For a substantial feature, consider the whole learning journey: a first successful use, guides for recurring tasks, exact reference material, and an explanation of the design and its limits. Include troubleshooting for likely mistakes and useful variations such as another shell, manifest format, or platform. Add these where they help the audience, without forcing every variation into the introductory tutorial.

Apply the required Humanizer skill while drafting and before delivery. Keep useful detail, examples, caveats, and precise terminology. Remove repetitive framing and inflated claims. Read the result as a colleague trying to learn the plugin, and repair places where a list of commands needs an explanation. Avoid excessive emphasis, unexplained jargon, and prose that addresses an agent instead of the reader.

## Organize around Diátaxis

Choose the page's purpose before writing it. [Diátaxis](https://diataxis.fr/) distinguishes four reader needs:

| Form | Reader's need | Content for a conda plugin |
| --- | --- | --- |
| Tutorial | Learn through a guided experience | A stated outcome, prerequisites, a small example built step by step, explanations at the point of use, observable results, cleanup, and a next step |
| How-to guide | Complete a specific task | A task-oriented title, starting conditions, direct steps, relevant alternatives, and recovery from likely failures |
| Reference | Look up an exact fact | Commands, flags, defaults, settings, format aliases, schemas, API behavior, supported versions, errors, and limitations |
| Explanation | Understand reasons and relationships | Concepts, design decisions, tradeoffs, compatibility with other tools, and why behavior differs between cases |

Keep each page's main purpose clear and link to the other forms where they help. A tutorial can briefly explain a step and link to a fuller discussion. Reference pages need accurate descriptions and examples, but should not require following a tutorial to find a default value.

Give the homepage enough context to choose a route. Describe what the plugin does, its installation requirements and current status, then offer a clear starting tutorial and links for experienced users. Keep the README useful on GitHub with a short working example and links to the fuller site. Maintain one authoritative detailed explanation for each topic.

Use the repository's navigation conventions. `tutorials/`, `how-to/`, `reference/`, and `explanation/` are useful directory names when the site has enough content. A smaller site can express the same purposes through pages such as `quickstart`, `howto`, `cli`, and `why`. Split large API references by subject and describe what readers will find on each linked page.

## Use Sphinx, MyST, and sphinx-design together

For a new plugin in this collection, start with Sphinx, `conda-sphinx-theme`, MyST Markdown, and `sphinx-design`. Preserve an existing project's chosen stack. Inspect `docs/conf.py`, the docs dependency group, build tasks, and hosting configuration before changing them.

The small shared configuration is:

```python
extensions = ["myst_parser", "sphinx_design"]
html_theme = "conda_sphinx_theme"
myst_enable_extensions = ["colon_fence"]
```

Declare the corresponding packages in the repository's documentation environment. Extend its existing configuration instead of replacing it. Enable additional MyST extensions such as `deflist`, `fieldlist`, or `tasklist` only when the content uses them. Autodoc, Napoleon, intersphinx, Mermaid, and generated CLI help should each serve an actual documentation need. Regenerate `pixi.lock` after changing Pixi dependencies or tasks.

MyST supplies Markdown authoring with Sphinx directives and roles. `sphinx-design` supplies presentation components. Enable MyST's [`colon_fence`](https://myst-parser.readthedocs.io/en/latest/syntax/optional.html#colon-fences) extension for nested colon-fenced directives. Use longer fences around containers than around their children.

Use responsive cards to help readers choose a subject. For example, this homepage markup links to four pages that must exist in the site:

```markdown
::::{grid} 1 1 2 2
:gutter: 3

:::{grid-item-card} Get started
:link: tutorials/getting-started
:link-type: doc

Install the plugin and create your first environment export.
:::

:::{grid-item-card} Export an environment
:link: how-to/export
:link-type: doc

Choose a format and save the result for another tool.
:::

:::{grid-item-card} Format reference
:link: reference/formats
:link-type: doc

Look up format names, defaults, and supported fields.
:::

:::{grid-item-card} Understand the export
:link: explanation/export-model
:link-type: doc

Learn how package requests and resolved records affect the output.
:::
::::
```

Keep a Sphinx `toctree` for those pages so they participate in navigation. A hidden toctree can accompany the homepage cards. Cards and a toctree have different jobs, and each destination still needs a useful page. The [sphinx-design grid documentation](https://sphinx-design.readthedocs.io/en/latest/grids.html) explains the responsive column settings.

Use `tab-set` and `tab-item` for equivalent alternatives, such as POSIX versus PowerShell commands or `conda.toml` versus `pyproject.toml`. Keep labels short: `POSIX`, `PowerShell`, `TOML`, or the filename. Show a complete working alternative inside each tab and keep shared explanation outside it. Required sequential steps should remain in reading order. Optional dropdowns can hold secondary detail, but prerequisites and important limitations must remain visible.

Use `{doc}` for page references, `(label)=` with `{ref}` for named sections, and domain roles such as `{py:func}` for documented APIs. Configure intersphinx when referencing another project's API inventory. Preserve valid relative Markdown links already used by the site. Avoid hard-coded output `.html` paths that depend on the selected Sphinx builder.

Use the theme's spacing, typography, and responsive components before adding custom CSS. Check cards, tab labels, tables, code blocks, and images on narrow screens. Include descriptive alternative text for images. A diagram should explain a relationship the prose would otherwise make hard to follow.

## Make examples useful and truthful

A tutorial should run from its stated starting conditions. Include the complete small fixture or manifest, the command to execute, what the result means, and how to inspect it. Link downloadable examples when they would be tedious to reconstruct. Keep shared code samples tied to maintained files with `literalinclude` where that improves accuracy.

Install the plugin into the environment that runs conda, and make that relationship clear to the reader. Generated CLI-help directives also need the installed plugin in the documentation environment. Do not assume that building HTML executes shell blocks or validates sample output.

Use current published installation commands when describing a release. Label development-only installation or unreleased behavior explicitly. Show actual output or clearly identify an excerpt. Explain values that can vary by platform, solver result, or version instead of presenting a transient package count as guaranteed.

Keep claims precise. Format validation, inventory completeness, signature verification, and publisher authorization prove different things. Explain compatibility with adjacent tools in practical terms. For example, workspace documentation should explain which manifests it reads and which operations conda performs.

## Record demos in the established VHS style

Use a short recording to help a person see a workflow before trying it. Pick a useful story with a visible starting state, a few ordinary commands, and a result worth inspecting. Put copyable commands and enough explanation beside the GIF for readers to complete the task without playing it.

Workspaces, Exec, Global, and Completion share VHS source tapes and a `demos/_settings.tape` file. Preserve the target project's settings. For a new sibling plugin without a recording style, these settings reproduce their shared appearance in `demos/_settings.tape`:

```text
Set Shell "bash"
Set FontFamily "JetBrains Mono"
Set FontSize 20
Set Width 1200
Set Height 600
Set Margin 20
Set MarginFill "#19191b"
Set Padding 20
Set Theme "Dark+"
Set TypingSpeed 40ms
Set WaitTimeout 120s

Env DEMO_PS1 "\[\e[1;38;2;67;176;42m\]$\[\e[0m\] "
Env BAT_OPTS "--color=always --paging=never --plain"
Env BAT_THEME "Visual Studio Dark+"
Env TERM "xterm-256color"
```

Use an environment containing the installed plugin, VHS, its `ttyd` and `ffmpeg` dependencies, and the selected font. Include Bat when a tape uses it to display files. Follow the project's environment tasks and the [VHS installation instructions](https://github.com/charmbracelet/vhs#installation) for missing tools.

Keep shared appearance in `_settings.tape` and source it from individual tapes. Inspect the repository's fixture layout and demo task before adding another recording. Shell demonstrations may need their own initialization, as in the Fish completion example. Adjust dimensions when a workflow needs more space, then check readability at the size where the docs embed it.

Prepare fixtures and machine setup under VHS `Hide`, then `Show` the user-facing workflow. Use brief visible shell comments to introduce a step. Allow time to read results, typically one to three seconds in the existing recordings. Synchronize execution with expected output or the prompt. Sleeps provide reading time and do not establish that a command finished.

Use real plugin commands and their real output. Show genuine Tab completion when teaching completion. Keep first-run setup and later cache reuse distinguishable. Disclose omitted installation or image-build waits when they would change the viewer's expectations. A demo is not a timing benchmark.

Allocate disposable demo state with `mktemp`, check allocation success, and clean up only the directory allocated for that recording. Use plugin-specific cache and state settings where available. Keep credentials and personal paths out of fixtures and frames. Record from the intended development environment without modifying the user's real environments or shell configuration.

After installing the [bundled greet example](plugin-guide.md#install-and-run-the-example), this `demos/greet.tape` demonstrates the shared setup and a real result:

```text
Require conda
Source demos/_settings.tape
Output demos/greet.gif

Hide
Type `export PS1="$DEMO_PS1"`
Enter
Wait /\$/
Type `demo_root=$(mktemp -d "${TMPDIR:-/tmp}/conda-greet-demo.XXXXXX") || exit 1`
Enter
Wait /\$/
Type `trap 'rm -rf -- "$demo_root"' EXIT`
Enter
Wait /\$/
Type `cd "$demo_root" && clear`
Enter
Wait /\$/
Show

Type "# Greet someone with the installed conda plugin"
Enter
Sleep 500ms
Type@80ms "conda greet --name Ada"
Enter
Wait+Screen /Hello, Ada!/
Wait /\$/
Sleep 3s
```

Run `vhs validate demos/greet.tape` to check its syntax, then `vhs demos/greet.tape` from the repository root to record it. Syntax validation does not execute the command. The result wait in this example checks the greeting before allowing reading time. Adapt the command, expected result, and fixtures to the plugin being documented.

Keep source tapes, required fixtures, and the GIF embedded by the documentation together in version control. Follow the repository's policy for additional formats such as MP4. Preserve its selected and batch regeneration commands. In the audited repositories these commonly use `pixi run demos <name>` and `pixi run demos`, but confirm the task definition before running either.

## Validate the reader's experience

Run the repository's declared documentation task in its declared environment. Use its strict build when available. For a new Sphinx setup, enable warnings as errors and unresolved-reference checking, for example with `sphinx-build -W --keep-going -n -b dirhtml docs docs/_build/dirhtml`. Fix the cause of new warnings instead of broadly suppressing them.

For new or changed commands, examples, or behavior claims, execute representative tutorial and how-to commands from clean disposable state. Use an existing example-check task if the project provides one. Check affected shell and platform variants on the platforms claimed, and report variants that were not exercised. A successful Sphinx build proves neither the commands nor the explanatory claims correct.

Inspect rendered pages for navigation, broken references, tab behavior, code overflow, and readable figures. Replay changed demo recordings and check the whole playback for clipping, missing glyphs, command failures, reading time, and stale output. Re-record when visible behavior changes. Keep GIFs small enough to load comfortably without making their text unreadable.

Finish with a Humanizer pass and a reader review. Can a newcomer follow the tutorial from its prerequisites, recognize the result, recover from a likely mistake, and find the next useful page? Can an experienced reader find the exact setting or format detail quickly? Retain the explanation and examples needed to answer those questions.

Report the docs build, example execution, visual review, and any untested platforms accurately. Report publication separately. External link checking may need a scheduled or manual task when remote services make it unreliable in ordinary pull-request checks.
