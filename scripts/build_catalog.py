#!/usr/bin/env python3
"""Rebuild .claude-plugin/marketplace.json and the README's plugin table.

Lists the owner's public repositories tagged with the topic, and for each one
reads its .claude-plugin/plugin.json (a plugin at the repo's root) or, failing
that, its own .claude-plugin/marketplace.json (plugins in subfolders). Private
repositories are never listed, whatever their topics.

Needs `gh` signed in (GH_TOKEN in Actions). Writes files only when they change.
"""

import base64
import json
import pathlib
import subprocess
import sys

OWNER = "MasonRhodesDev"
TOPIC = "claude-plugin"
ROOT = pathlib.Path(__file__).resolve().parent.parent
MARKETPLACE = ROOT / ".claude-plugin" / "marketplace.json"
README = ROOT / "README.md"
BEGIN, END = "<!-- catalog:begin -->", "<!-- catalog:end -->"


def gh(*args: str) -> str:
    return subprocess.run(["gh", *args], check=True, capture_output=True, text=True).stdout


def read_json(repo: str, path: str) -> dict | None:
    try:
        out = gh("api", f"repos/{repo}/contents/{path}")
    except subprocess.CalledProcessError:
        return None
    return json.loads(base64.b64decode(json.loads(out)["content"]))


def plugins_of(repo: str) -> list[dict]:
    root = read_json(repo, ".claude-plugin/plugin.json")
    if root is not None:
        return [{"name": root["name"], "source": {"source": "github", "repo": repo}, "description": root.get("description", "")}]

    found = []
    for entry in (read_json(repo, ".claude-plugin/marketplace.json") or {}).get("plugins", []):
        source = entry.get("source")
        if not isinstance(source, str):
            continue
        path = source.removeprefix("./").strip("/")
        manifest = read_json(repo, f"{path}/.claude-plugin/plugin.json" if path else ".claude-plugin/plugin.json") or {}
        found.append(
            {
                "name": entry["name"],
                "source": {"source": "github", "repo": repo}
                if not path
                else {"source": "git-subdir", "url": f"https://github.com/{repo}.git", "path": path},
                "description": manifest.get("description") or entry.get("description", ""),
            }
        )
    return found


def main() -> int:
    repos = json.loads(
        gh("search", "repos", "--owner", OWNER, "--topic", TOPIC, "--visibility", "public", "--limit", "200", "--json", "fullName,visibility")
    )
    plugins = []
    for repo in sorted(r["fullName"] for r in repos if r["visibility"] == "public"):
        found = plugins_of(repo)
        if not found:
            print(f"skip {repo}: no plugin.json or marketplace.json", file=sys.stderr)
        plugins += found
    plugins.sort(key=lambda p: p["name"])

    names = [p["name"] for p in plugins]
    if len(names) != len(set(names)):
        print(f"duplicate plugin names: {names}", file=sys.stderr)
        return 1

    catalog = json.loads(MARKETPLACE.read_text())
    catalog["plugins"] = plugins
    text = json.dumps(catalog, indent=2, ensure_ascii=False) + "\n"
    if MARKETPLACE.read_text() != text:
        MARKETPLACE.write_text(text)

    rows = ["| Plugin | Repository | What it does |", "|---|---|---|"]
    for p in plugins:
        repo = p["source"].get("repo") or p["source"]["url"].removeprefix("https://github.com/").removesuffix(".git")
        rows.append(f"| `{p['name']}` | [{repo}](https://github.com/{repo}) | {p['description'].replace('|', '/')} |")
    readme = README.read_text()
    head, rest = readme.split(BEGIN, 1)
    _, tail = rest.split(END, 1)
    new = f"{head}{BEGIN}\n{chr(10).join(rows)}\n{END}{tail}"
    if new != readme:
        README.write_text(new)

    print(f"{len(plugins)} plugins: {', '.join(names)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
