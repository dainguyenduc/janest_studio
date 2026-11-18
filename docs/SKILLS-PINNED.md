# Pinned custom skills

The custom skills this harness depends on are **copied into the repo** at
`.claude/skills/`, not referenced from `~/.claude-account3/skills/`. The project copy is what
runs (project skills take precedence over user-level ones), so the pipeline cannot drift when
the user-level skills are edited.

Source: `~/.claude-account3/skills/` — not a git repo and the skills carry no version field, so
they are pinned by content hash. Snapshot taken **2026-11-18**.

| Skill | Files | SKILL.md sha256 (first 16) | Source mtime |
|---|---|---|---|
| `p2p-explore` | 1 | `0154f80bd4346d2e` | 2026-09-30 |
| `p2p-plan` | 1 | `db0e6685baf4c7c6` | 2026-09-30 |
| `p2p-build` | 1 | `ea43cd3992868c9d` | 2026-09-30 |
| `p2p-fix` | 1 | `977e9b43775a5d3a` | 2026-09-30 |
| `p2p-investigate` | 1 | `e75aba52b55bf5d3` | 2026-09-30 |
| `p2p-review` | 1 | `8691ff01bb4f413a` | 2026-09-30 |
| `p2p-commit` | 1 | `0af172c1255456e1` | 2026-09-30 |
| `p2p-challenge` | 1 | `9f642a45a7e7ee6b` | 2026-09-30 |
| `pixel-art-game-style` | 6 | `6dcba76b40d44b76` | 2026-11-17 |
| `pixelstrata` | 14 | `cabac964483c3741` | — (vendored, see STACK.md §4) |
| `pixelorama` | 2 | `b0a69d84ba729b22` | — (vendored, see STACK.md §4) |
| `godot-mcp` | 2 | `d6a1ab7d777b8cbe` | — (vendored, see STACK.md §4) |

The last three come from PixelStrata v0.3.0 and are pinned by its git tag instead —
see `docs/STACK.md` §4.

## Keeping them in sync

`tools/skills-diff.sh` compares every pinned skill against the user-level copy and prints the
drift. Nothing syncs automatically — that is the point. To adopt a user-level change
deliberately:

```bash
tools/skills-diff.sh                 # see what differs
tools/skills-diff.sh --pull <skill>  # copy user-level -> project, then commit
```

A pinned skill that no longer exists user-level keeps working; the project copy is self-contained.

## Known gap: graphatlas

`p2p-build`, `p2p-fix` and `p2p-explore` declare `mcp__graphatlas__*` and probe for 10 tools
(`ga_architecture`, `ga_symbols`, `ga_callers`, `ga_callees`, `ga_impact`, `ga_importers`,
`ga_hubs`, `ga_risk`, `ga_file_summary`, `ga_reindex`). **No such server exists** — it is not on
npm, not on PyPI, not on GitHub, and not configured in either Claude config dir. The skills'
own Phase 0a probe handles this: `ga_architecture` fails → GA unavailable → grep + `git log`
fallback. Nothing is broken.

Substituting a real code-graph MCP server was considered and rejected: CodeGraph,
code-graph-mcp, grapha and codegraph-mcp were all checked and **none supports GDScript**, so an
indexer would be blind to this project's actual code. Revisit only if a GDScript-aware code
graph appears, or if this project grows a C#/TypeScript surface worth indexing.
