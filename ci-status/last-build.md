# Build 35 — success

commit: 8d09001d10a1adb837de397d59454cb1b8cab18f
run: https://github.com/westd72882-glitch/OGSR-AIMODE/actions/runs/33302906352

## Diagnosis (log has 335 lines)
```
[1m[90m[DEBUG][39m[0m:   	> Task :processDebugResources
[1m[90m[DEBUG][39m[0m:   	> Task :mergeDebugJniLibFolders
[1m[90m[DEBUG][39m[0m:   	
[1m[90m[DEBUG][39m[0m:   	> Task :compileDebugJavaWithJavac
[1m[90m[DEBUG][39m[0m:   	Note: Some input files use or override a deprecated API.
[1m[90m[DEBUG][39m[0m:   	Note: Recompile with -Xlint:deprecation for details.
[1m[90m[DEBUG][39m[0m:   	
[1m[90m[DEBUG][39m[0m:   	> Task :dexBuilderDebug
[1m[90m[DEBUG][39m[0m:   	> Task :mergeProjectDexDebug
[1m[90m[DEBUG][39m[0m:   	> Task :mergeDebugNativeLibs
[1m[90m[DEBUG][39m[0m:   	> Task :validateSigningDebug
[1m[90m[DEBUG][39m[0m:   	> Task :writeDebugAppMetadata
[1m[90m[DEBUG][39m[0m:   	> Task :writeDebugSigningConfigVersions
[1m[90m[DEBUG][39m[0m:   	> Task :stripDebugDebugSymbols
[1m[90m[DEBUG][39m[0m:   	> Task :packageDebug
[1m[90m[DEBUG][39m[0m:   	> Task :createDebugApkListingFileRedirect
[1m[90m[DEBUG][39m[0m:   	> Task :assembleDebug
[1m[90m[DEBUG][39m[0m:   	
[1m[90m[DEBUG][39m[0m:   	[Incubating] Problems report is available at: file:///home/runner/work/OGSR-AIMODE/OGSR-AIMODE/android-port/.buildozer/android/platform/build-arm64-v8a/dists/mcpython/build/reports/problems/problems-report.html
[1m[90m[DEBUG][39m[0m:   	
[1m[90m[DEBUG][39m[0m:   	Deprecated Gradle features were used in this build, making it incompatible with Gradle 9.0.
[1m[90m[DEBUG][39m[0m:   	
[1m[90m[DEBUG][39m[0m:   	You can use '--warning-mode all' to show the individual deprecation warnings and determine if they come from your own scripts or plugins.
[1m[90m[DEBUG][39m[0m:   	
[1m[90m[DEBUG][39m[0m:   	For more on this, please refer to https://docs.gradle.org/8.14.3/userguide/command_line_interface.html#sec:command_line_warnings in the Gradle documentation.
[1m[90m[DEBUG][39m[0m:   	
[1m[90m[DEBUG][39m[0m:   	BUILD SUCCESSFUL in 31s
[1m[90m[DEBUG][39m[0m:   	34 actionable tasks: 34 executed
[1m[INFO][0m:    [36m<- directory context /home/runner/work/OGSR-AIMODE/OGSR-AIMODE/android-port/.buildozer/android/platform/python-for-android[39m
[1m[90m[DEBUG][39m[0m:   All possible dists: [<Distribution: name mcpython with recipes (freetype, hostpython3, jpeg, libffi, openssl, png, sdl2_image, sdl2_mixer, sdl2_ttf, sqlite3, python3, sdl2, numpy, pillow, pyjnius, setuptools, android, mcgame, kivy, nbtlib, filetype, certifi, six, idna, requests, chardet, charset_normalizer, urllib3)>]
[1m[90m[DEBUG][39m[0m:   Dist matching name and arch: [<Distribution: name mcpython with recipes (freetype, hostpython3, jpeg, libffi, openssl, png, sdl2_image, sdl2_mixer, sdl2_ttf, sqlite3, python3, sdl2, numpy, pillow, pyjnius, setuptools, android, mcgame, kivy, nbtlib, filetype, certifi, six, idna, requests, chardet, charset_normalizer, urllib3)>]
[1m[90m[DEBUG][39m[0m:   Dist matching ndk_api and recipe: [<Distribution: name mcpython with recipes (freetype, hostpython3, jpeg, libffi, openssl, png, sdl2_image, sdl2_mixer, sdl2_ttf, sqlite3, python3, sdl2, numpy, pillow, pyjnius, setuptools, android, mcgame, kivy, nbtlib, filetype, certifi, six, idna, requests, chardet, charset_normalizer, urllib3)>]
[1m[INFO][0m:    Of the existing distributions, the following meet the given requirements:
[1m[INFO][0m:    	[32m[1mmcpython[0m: min API 24, includes recipes ([32mfreetype, hostpython3, jpeg, libffi, openssl, png, sdl2_image, sdl2_mixer, sdl2_ttf, sqlite3, python3, sdl2, numpy, pillow, pyjnius, setuptools, android, mcgame, kivy, nbtlib, filetype, certifi, six, idna, requests, chardet, charset_normalizer, urllib3[0m), built for archs ([34marm64-v8a[0m)
[1m[INFO][0m:    [1m[94mmcpython has compatible recipes, using this one[0m
[1m[INFO][0m:    [1m[32m# Copying android package to current directory[0m[39m
[1m[INFO][0m:    [1m[32m# Android package filename not found in build output. Guessing...[0m[39m
[1m[INFO][0m:    [1m[32m# Found android package file: /home/runner/work/OGSR-AIMODE/OGSR-AIMODE/android-port/.buildozer/android/platform/build-arm64-v8a/dists/mcpython/build/outputs/apk/debug/mcpython-debug.apk[0m[39m
[1m[INFO][0m:    # Add version number to android package
[1m[INFO][0m:    # Android package renamed to mcpython-debug-20100223.apk
stty: 'standard input': Inappropriate ioctl for device
[1m[90m[DEBUG][39m[0m:   [90m->[0m running cp /home/runner/work/OGSR-AIMODE/OGSR-AIMODE/android-port/.buildozer/android/platform/build-arm64-v8a/dists/mcpython/build/outputs/apk/debug/mcpython-debug.apk mcpython-debug-20100223.apk[0m
No setup.py/pyproject.toml used, copying full private data into .apk.
Applying Java source code patches...
Applying patch: src/patches/SDLActivity.java.patch
Warning: failed to apply patch (exit code 1), assuming it is already applied:  src/patches/SDLActivity.java.patch
Applying patch: src/patches/SDLSurface.java.patch
Warning: failed to apply patch (exit code 1), assuming it is already applied:  src/patches/SDLSurface.java.patch
[0m[1;34m# Android packaging done![0m
[0m[1;34m# APK mcpython-20100223-arm64-v8a-debug.apk available in the bin directory[0m
```

## Generated build.gradle (head)
```
     1	apply plugin: 'com.android.application'
     2	
     3	
     4	android {
     5	    namespace 'org.mcpython.mcpython'
     6	    compileSdkVersion 33
     7	    buildToolsVersion '37.0.0'
     8	    defaultConfig {
     9	        minSdkVersion 24
    10	        targetSdkVersion 33
    11	        versionCode 20100223
    12	        versionName '20100223'
    13	        manifestPlaceholders = [:]
    14	    }
    15	
    16		
    17		packagingOptions {
    18	        jniLibs {
    19	            useLegacyPackaging = true
    20	        }
    21	        doNotStrip '**/*.so'
```

## Recipe stage
```
c files: 33
```
