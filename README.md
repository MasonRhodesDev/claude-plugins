# claude-plugins

One marketplace for my Claude Code plugins. It's only a catalog: each plugin lives in its own repository, and `.claude-plugin/marketplace.json` points at it.

## Setup

At the prompt of a terminal session:

```
/plugin marketplace add MasonRhodesDev/claude-plugins
```

Then install what you want:

```
/plugin install pm-loop@mrhodes
```

From a shell, use `claude plugin marketplace add …` and `claude plugin install …` the same way.

## Plugins

Built by the Build catalog workflow; don't edit between the markers.

<!-- catalog:begin -->
| Plugin | Repository | What it does |
|---|---|---|
| `pm-loop` | [MasonRhodesDev/pm-loop](https://github.com/MasonRhodesDev/pm-loop) | Event-driven, script-first PM loop for GitHub repos worked by Claude Code lanes: poller/webhook → queue → one small headless PM tick; scripted pre-merge/merge, STATUS entries, fact-checks, review routing; fresh capped agents; local LLM for prose only. |
<!-- catalog:end -->

## Adding a plugin

Tag its public repository with the `claude-plugin` topic:

```
gh repo edit MasonRhodesDev/<repo> --add-topic claude-plugin
```

The Build catalog workflow runs daily and from its Run workflow button (Actions tab). It reads the repo's `.claude-plugin/plugin.json`, or its own `.claude-plugin/marketplace.json` when the plugin sits in a subfolder, and commits the updated catalog. Private repositories are never listed. Run `python3 scripts/build_catalog.py` to rebuild locally.
