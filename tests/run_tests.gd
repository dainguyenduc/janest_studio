extends SceneTree
## Headless CLI runner for this project's GDScript test suites.
##
## Suites are plain `McpTestSuite` subclasses in res://tests/test_*.gd — the same
## format the Godot AI `test_run` MCP tool discovers, so one suite works both ways:
## headless from the terminal (this script) and in the live editor (test_run).
##
## Usage (see tools/run-tests.sh, which wraps this):
##   godot --headless --path . --script res://tests/run_tests.gd -- [options]
##
##   --list              print "<suite>.<test>" per test and exit 0, run nothing
##   -t <pattern>        run only tests whose method name contains <pattern>
##   --suite <name>      run only the suite with this suite_name()
##
## Exit codes: 0 all green · 1 a test failed, a suite failed to load, or a
## filter matched nothing (a filter matching 0 tests must never read as pass).

const TESTS_DIR := "res://tests"


func _initialize() -> void:
	var args := OS.get_cmdline_user_args()
	var list_only := args.has("--list")
	var pattern := _arg_value(args, "-t")
	var suite_filter := _arg_value(args, "--suite")

	var load_errors: Array[String] = []
	var suites := _discover(load_errors)

	for err in load_errors:
		printerr("LOAD ERROR: %s" % err)

	if suites.is_empty():
		if load_errors.is_empty():
			print("No test suites in %s (expected test_*.gd extending McpTestSuite)." % TESTS_DIR)
			quit(0)
		else:
			printerr("No loadable test suites.")
			quit(1)
		return

	if list_only:
		var listed := 0
		for suite in suites:
			var sname: String = suite.suite_name()
			if suite_filter != "" and sname != suite_filter:
				continue
			for m in suite.get_method_list():
				var mname: String = m.get("name", "")
				if not mname.begins_with("test_"):
					continue
				if pattern != "" and not mname.contains(pattern):
					continue
				print("%s.%s" % [sname, mname])
				listed += 1
		if listed == 0:
			printerr("No tests matched (suite=%s, -t=%s)." % [suite_filter, pattern])
			quit(1)
		else:
			quit(0)
		return

	var runner := McpTestRunner.new()
	var res: Dictionary = runner.run_suites(suites, suite_filter, pattern, {}, true)

	var total: int = res.get("total", 0)
	var passed: int = res.get("passed", 0)
	var failed: int = res.get("failed", 0)
	var skipped: int = res.get("skipped", 0)

	for r in res.get("results", []):
		var mark := "ok  "
		if r.get("skipped", false):
			mark = "skip"
		elif not r.get("passed", false):
			mark = "FAIL"
		print("[%s] %s.%s" % [mark, r.get("suite", "?"), r.get("test", r.get("name", "?"))])

	for f in res.get("failures", []):
		printerr("FAIL %s.%s: %s" % [
			f.get("suite", "?"), f.get("test", f.get("name", "?")), f.get("message", "")
		])

	print("\n%d total · %d passed · %d failed · %d skipped · %d ms" % [
		total, passed, failed, skipped, res.get("duration_ms", 0)
	])

	if failed > 0 or not load_errors.is_empty():
		quit(1)
	elif total == 0 and (pattern != "" or suite_filter != ""):
		printerr("Filter matched 0 tests (suite=%s, -t=%s) — not a pass." % [suite_filter, pattern])
		quit(1)
	else:
		quit(0)


func _arg_value(args: PackedStringArray, flag: String) -> String:
	for i in args.size():
		if args[i] == flag and i + 1 < args.size():
			return args[i + 1]
	return ""


func _discover(load_errors: Array[String]) -> Array:
	var suites := []
	var dir := DirAccess.open(TESTS_DIR)
	if dir == null:
		load_errors.append("cannot open %s" % TESTS_DIR)
		return suites

	var names := dir.get_files()
	names.sort()
	for file_name in names:
		if not file_name.begins_with("test_") or not file_name.ends_with(".gd"):
			continue
		var path := "%s/%s" % [TESTS_DIR, file_name]
		var script: Resource = load(path)
		if script == null or not (script is GDScript):
			load_errors.append("%s: not a loadable GDScript" % path)
			continue
		var instance: Variant = (script as GDScript).new()
		if not (instance is McpTestSuite):
			load_errors.append("%s: does not extend McpTestSuite" % path)
			continue
		suites.append(instance)

	suites.sort_custom(func(a, b): return a.suite_name() < b.suite_name())
	return suites
