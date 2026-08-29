[app]
title = MC Python Toolchain Check
package.name = mcpython
package.domain = org.mcpython

source.dir = .
source.include_exts = py,pyx,pxd,png,jpg,gif,ogg,txt,mclevel

version = 0.1

# The dependencies the real port needs. Cython and numpy are the risky
# ones - they compile native code for the target ABI.
requirements = python3,kivy,numpy,pillow,nbtlib

orientation = landscape
fullscreen = 1

[app:android]
android.api = 33
android.minapi = 21
android.ndk_api = 21
android.archs = arm64-v8a
android.accept_sdk_license = True
android.allow_backup = True

[buildozer]
log_level = 2
warn_on_root = 0
