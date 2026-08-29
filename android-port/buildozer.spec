[app]
title = Minecraft Python Edition
package.name = mcpython
package.domain = org.mcpython

source.dir = .
source.include_exts = py,png,jpg,gif,ogg,txt,mclevel

# game/ is built by the mcgame recipe and installed into site-packages;
# packaging it again as app data would duplicate 23 MB into the APK.
source.exclude_dirs = game,p4a-recipes,bin,.buildozer

version = 20100223

# mcgame is the local recipe that cythonises the game's 33 .pyx modules.
requirements = python3,kivy,numpy,pillow,nbtlib,mcgame

p4a.local_recipes = ./p4a-recipes

orientation = landscape
fullscreen = 1

# Android options must live in [app]; buildozer ignores an [app:android]
# section, which silently drops accept_sdk_license.
android.api = 33
android.minapi = 24
android.ndk_api = 24
android.archs = arm64-v8a
android.accept_sdk_license = True
android.allow_backup = True

[buildozer]
log_level = 2
warn_on_root = 0
