# claude-plugins

One marketplace for my Claude Code plugins. It's only a catalog: each plugin lives in its own repository, and this file points at it.

## Setup

At the prompt of a terminal session:

```
/plugin marketplace add MasonRhodesDev/claude-plugins
```

Then install what you want:

```
/plugin install needs-you@mrhodes
/plugin install pm-loop@mrhodes
```

From a shell, use `claude plugin marketplace add …` and `claude plugin install …` the same way.

## Plugins

| Plugin | Repository | What it does |
|---|---|---|
| `needs-you` | [MasonRhodesDev/needs-you](https://github.com/MasonRhodesDev/needs-you) | Claude ends every turn with a typed "What I need from you" list; answer it from a band above the prompt and the answers send themselves. |
| `pm-loop` | [MasonRhodesDev/pm-loop](https://github.com/MasonRhodesDev/pm-loop) | Event-driven, script-first PM loop for GitHub repos worked by Claude Code lanes. |

## Adding a plugin

Add an entry to `.claude-plugin/marketplace.json` whose `source` is `{ "source": "github", "repo": "MasonRhodesDev/<repo>" }` (or `git-subdir` with a `path` when the plugin sits in a subfolder), then run `claude plugin validate .`.
