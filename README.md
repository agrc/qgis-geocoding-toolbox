# NOTE: This project is no longer maintained. Feel free to fork if you would like to continue to work on it.

# qgis-geocoding-toolbox

A QGIS plugin for geocoding addresses via [api.mapserv.utah.gov](https://api.mapserv.utah.gov) (Utah-only addresses).

[Download the latest release](`AGRCGeocodingToolbox.zip`).

## Development

Install development dependencies by running: `pip install -r requirements.txt` (recommended to do this within a virtual environment). Update this file by running: `pip freeze -l > requirements.txt`.

Run `ptw` or `pytest` to run tests.

[`pb_tool`](https://github.com/g-sherman/plugin_build_tool) is used to build and deploy the plugin.

Helpful commands:

- `pb_tool deploy` - Rebuild and deploy the plugin to your local plugins directory. Restart QGIS to see the changes. Use the [Plugin Reloader](https://plugins.qgis.org/plugins/plugin_reloader/) QGIS plugin to reload the plugin under development after running this command. This saves you from having to restart QGIS.
- `pb_tool zip` - Package the plugin into a zip file suitable for uploading to the QGIS plugin repository

### Release Steps

1. `pytest`
1. Update `metadata.txt` with new version number and changelog text
1. Commit and tag (e.g. `v1.0.0`) changes
1. `pb_tool zip`
1. Upload `AGRCGeocodingToolbox.zip` as a new version in the [QGIS Plugin Repository](http://plugins.qgis.org/plugins/AGRCGeocodingToolbox/version/add/)
