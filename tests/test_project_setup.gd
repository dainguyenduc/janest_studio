@tool
extends McpTestSuite
## Guards the pixel-art rendering contract from CLAUDE.md "Locked decisions".
## A silent change to any of these ruins every sprite in the game, so it is
## cheaper to fail here than to notice it in a screenshot three phases later.


func suite_name() -> String:
	return "project_setup"


func test_main_scene_loads() -> void:
	var path: String = ProjectSettings.get_setting("application/run/main_scene", "")
	assert_ne(path, "", "application/run/main_scene must be set")
	var scene := load(path)
	assert_true(scene is PackedScene, "main scene should load as a PackedScene: %s" % path)
	var root := track((scene as PackedScene).instantiate())
	assert_true(root != null, "main scene should instantiate")


func test_base_resolution_is_384x216() -> void:
	assert_eq(int(ProjectSettings.get_setting("display/window/size/viewport_width", 0)), 384)
	assert_eq(int(ProjectSettings.get_setting("display/window/size/viewport_height", 0)), 216)


func test_stretch_mode_is_viewport() -> void:
	assert_eq(
		str(ProjectSettings.get_setting("display/window/stretch/mode", "")),
		"viewport",
		"pixel art needs integer-scaled viewport stretch, not 'disabled' or 'canvas_items'"
	)


func test_texture_filter_is_nearest() -> void:
	# 0 == TEXTURE_FILTER_NEAREST. Linear filtering blurs every sprite.
	assert_eq(
		int(ProjectSettings.get_setting("rendering/textures/canvas_textures/default_texture_filter", -1)),
		0,
		"default_texture_filter must be Nearest"
	)


func test_pixel_snap_enabled() -> void:
	assert_true(
		bool(ProjectSettings.get_setting("rendering/2d/snap/snap_2d_transforms_to_pixel", false)),
		"snap_2d_transforms_to_pixel must be on"
	)
	assert_true(
		bool(ProjectSettings.get_setting("rendering/2d/snap/snap_2d_vertices_to_pixel", false)),
		"snap_2d_vertices_to_pixel must be on"
	)


func test_godot_ai_plugin_enabled() -> void:
	var enabled: PackedStringArray = ProjectSettings.get_setting(
		"editor_plugins/enabled", PackedStringArray()
	)
	assert_contains(
		Array(enabled),
		"res://addons/godot_ai/plugin.cfg",
		"the Godot AI plugin is the engine-in-the-loop MCP; it must stay enabled"
	)
