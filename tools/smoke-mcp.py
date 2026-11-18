#!/usr/bin/env python3
"""Smoke-test the Godot AI MCP chain: bridge -> python server -> live editor.

Run the editor first (tools/godot-editor.sh), then:  python3 -I tools/smoke-mcp.py
Proves initialize + tools/list + one real tools/call against the open project.
"""
import json, subprocess, sys, time
cfg = json.load(open("/Volumes/DATA/personal_project/game_dev/janest_studio/.mcp.json"))["mcpServers"]["godot-ai"]
cmd = [cfg["command"]] + cfg["args"]
p = subprocess.Popen(cmd, stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                     stderr=subprocess.DEVNULL, text=True, bufsize=1)
def send(o):
    p.stdin.write(json.dumps(o) + "\n"); p.stdin.flush()

send({"jsonrpc":"2.0","id":1,"method":"initialize","params":{
      "protocolVersion":"2025-06-18","capabilities":{},
      "clientInfo":{"name":"janest-smoke","version":"0.1"}}})
send({"jsonrpc":"2.0","method":"notifications/initialized"})
send({"jsonrpc":"2.0","id":2,"method":"tools/list"})
send({"jsonrpc":"2.0","id":3,"method":"tools/call",
      "params":{"name":"editor_state","arguments":{}}})

deadline = time.time() + 120
seen = set()
while time.time() < deadline and {1,2,3} - seen:
    line = p.stdout.readline()
    if not line: break
    try: msg = json.loads(line)
    except Exception: continue
    i = msg.get("id")
    if i == 1:
        si = msg.get("result",{}).get("serverInfo",{})
        print(f"[ok] initialize -> {si.get('name')} {si.get('version')}"); seen.add(1)
    elif i == 2:
        tools = msg.get("result",{}).get("tools",[])
        names = sorted(t["name"] for t in tools)
        print(f"[ok] tools/list -> {len(names)} tools")
        print("     " + ", ".join(names[:12]) + (" ..." if len(names)>12 else ""))
        for must in ("project_run","logs_read","test_run","editor_screenshot","scene_manage","node_create"):
            print(f"     {'ok ' if must in names else 'MISSING'} {must}")
        seen.add(2)
    elif i == 3:
        r = msg.get("result") or msg.get("error")
        txt = json.dumps(r)
        print(f"[{'ok' if 'error' not in msg else '!!'}] tools/call editor_state -> {txt[:420]}")
        seen.add(3)
p.terminate()
print("missing responses:", sorted({1,2,3}-seen) or "none")
