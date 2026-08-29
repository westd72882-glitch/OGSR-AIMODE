# Build 32 — failure

commit: d26abf5d15a1ffed968176b2840bcb99eb2de0cb
run: https://github.com/westd72882-glitch/OGSR-AIMODE/actions/runs/33278970756

## Compile errors
```
591:[1m[90m[DEBUG][39m[0m:   	clang: error: no such file or directory: 'mc/JavaUtils.c'
630:clang: error: no such file or directory: 'mc/JavaUtils.c'
```

## Cythonise + recipe
```
195:[1m[INFO][0m:    [1m[94mThe requirements (certifi, chardet, charset_normalizer, filetype, idna, nbtlib, requests, six, urllib3) were not found as recipes, they will be installed with pip.[0m
1683:[1m[INFO][0m:    mcgame: installing /home/runner/work/OGSR-AIMODE/OGSR-AIMODE/android-port/.buildozer/android/platform/build-arm64-v8a/build/other_builds/mcgame/arm64-v8a__ndk_target_24/mcgame/build/lib.linux-x86_64-cpython-314 into /home/runner/work/OGSR-AIMODE/OGSR-AIMODE/android-port/.buildozer/android/platform/build-arm64-v8a/build/python-installs/mcpython/arm64-v8a
1684:[1m[INFO][0m:    mcgame: pre-installing pure Python requirements into /home/runner/work/OGSR-AIMODE/OGSR-AIMODE/android-port/.buildozer/android/platform/build-arm64-v8a/build/python-installs/mcpython/arm64-v8a
pyx: 66  c: 33
```

## Failure (log has 10842 lines)
```
export JAVA_HOME_21_X64='/usr/lib/jvm/temurin-21-jdk-amd64'
export GITHUB_ENV='/home/runner/work/_temp/_runner_file_commands/set_env_f176a41e-06b3-4f6b-89a4-fb543883da7d'
export GITHUB_EVENT_PATH='/home/runner/work/_temp/_github_workflow/event.json'
export INVOCATION_ID='38d4670c071d4609b74e948053d01651'
export GITHUB_EVENT_NAME='push'
export GITHUB_RUN_ID='33278970756'
export JAVA_HOME_17_X64='/opt/hostedtoolcache/Java_Temurin-Hotspot_jdk/17.0.20-1/x64'
export ANDROID_NDK_HOME='/home/runner/.buildozer/android/platform/android-ndk-r28c'
export GITHUB_STEP_SUMMARY='/home/runner/work/_temp/_runner_file_commands/step_summary_f176a41e-06b3-4f6b-89a4-fb543883da7d'
export HOMEBREW_NO_AUTO_UPDATE='1'
export GITHUB_ACTOR='westd72882-glitch'
export NVM_DIR='/home/runner/.nvm'
export SGX_AESM_ADDR='1'
export GITHUB_RUN_ATTEMPT='1'
export ANDROID_HOME='/home/runner/.buildozer/android/platform/android-sdk'
export GITHUB_GRAPHQL_URL='https://api.github.com/graphql'
export ACCEPT_EULA='Y'
export USER='runner'
export PSModulePath='/root/.local/share/powershell/Modules:/usr/local/share/powershell/Modules:/opt/microsoft/powershell/7/Modules:/usr/share/az_15.6.1'
export GITHUB_SERVER_URL='https://github.com'
export PIPX_HOME='/opt/pipx'
export GECKOWEBDRIVER='/usr/local/share/gecko_driver'
export CHROMEWEBDRIVER='/usr/local/share/chromedriver-linux64'
export SHLVL='1'
export ANDROID_SDK_ROOT='/usr/local/lib/android/sdk'
export VCPKG_INSTALLATION_ROOT='/usr/local/share/vcpkg'
export GITHUB_ACTOR_ID='306517529'
export ACTIONS_ORCHESTRATION_ID='40c7b7e7-c57e-4af4-aa16-4e1704e183c5.apk.__default'
export RUNNER_TOOL_CACHE='/opt/hostedtoolcache'
export ImageVersion='20260823.283.1'
export Python3_ROOT_DIR='/opt/hostedtoolcache/Python/3.11.16/x64'
export DOTNET_NOLOGO='1'
export GITHUB_ARTIFACTS='/home/runner/work/_temp/_runner_file_commands/artifacts_f176a41e-06b3-4f6b-89a4-fb543883da7d'
export GITHUB_WORKFLOW_SHA='d26abf5d15a1ffed968176b2840bcb99eb2de0cb'
export GOROOT_1_24_X64='/opt/hostedtoolcache/go/1.24.13/x64'
export GITHUB_REF_NAME='claude/repo-analysis-build-7g4rq6'
export GITHUB_JOB='apk'
export LD_LIBRARY_PATH='/opt/hostedtoolcache/Python/3.11.16/x64/lib'
export XDG_RUNTIME_DIR='/run/user/1001'
export AZURE_EXTENSION_DIR='/opt/az/azcliextensions'
export GOROOT_1_26_X64='/opt/hostedtoolcache/go/1.26.7/x64'
export GITHUB_REPOSITORY='westd72882-glitch/OGSR-AIMODE'
export Python2_ROOT_DIR='/opt/hostedtoolcache/Python/3.11.16/x64'
export ANDROID_NDK_ROOT='/usr/local/lib/android/sdk/ndk/27.3.13750724'
export CHROME_BIN='/usr/bin/google-chrome'
export GITHUB_RETENTION_DAYS='90'
export JOURNAL_STREAM='9:14404'
export RUNNER_WORKSPACE='/home/runner/work/OGSR-AIMODE'
export GITHUB_ACTION_REPOSITORY=''
export HCA_CLOUD_PROVIDER='azure'
export PATH='/home/runner/.buildozer/android/platform/apache-ant-1.9.4/bin:/opt/hostedtoolcache/Java_Temurin-Hotspot_jdk/17.0.20-1/x64/bin:/opt/hostedtoolcache/Python/3.11.16/x64/bin:/opt/hostedtoolcache/Python/3.11.16/x64:/snap/bin:/home/runner/.local/bin:/opt/pipx_bin:/home/runner/.cargo/bin:/home/runner/.config/composer/vendor/bin:/usr/local/.ghcup/bin:/home/runner/.dotnet/tools:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/usr/games:/usr/local/games:/snap/bin'
export GITHUB_BASE_REF=''
export GHCUP_INSTALL_BASE_PREFIX='/usr/local'
export CI='true'
export SWIFT_PATH='/usr/share/swift/usr/bin'
export ImageOS='ubuntu24'
export GITHUB_REPOSITORY_OWNER='westd72882-glitch'
export GITHUB_HEAD_REF=''
export GITHUB_ACTION_REF=''
export ENABLE_RUNNER_TRACING='true'
export GITHUB_WORKFLOW='Android Port'
export DEBIAN_FRONTEND='noninteractive'
export GITHUB_OUTPUT='/home/runner/work/_temp/_runner_file_commands/set_output_f176a41e-06b3-4f6b-89a4-fb543883da7d'
export AGENT_TOOLSDIRECTORY='/opt/hostedtoolcache'
export _='/opt/hostedtoolcache/Python/3.11.16/x64/bin/buildozer'
export PACKAGES_PATH='/home/runner/.buildozer/android/packages'
export ANDROIDSDK='/home/runner/.buildozer/android/platform/android-sdk'
export ANDROIDNDK='/home/runner/.buildozer/android/platform/android-ndk-r28c'
export ANDROIDAPI='33'
export ANDROIDMINAPI='24'

[1m[INFO][0m:    [33mCOMMAND:[39m
cd /home/runner/work/OGSR-AIMODE/OGSR-AIMODE/android-port/.buildozer/android/platform/build-arm64-v8a/dists/mcpython && /home/runner/work/OGSR-AIMODE/OGSR-AIMODE/android-port/.buildozer/android/platform/build-arm64-v8a/dists/mcpython/gradlew clean assembleDebug

[1m[31m[WARNING][39m[0m: [31mERROR: /home/runner/work/OGSR-AIMODE/OGSR-AIMODE/android-port/.buildozer/android/platform/build-arm64-v8a/dists/mcpython/gradlew failed![39m
No setup.py/pyproject.toml used, copying full private data into .apk.
Applying Java source code patches...
Applying patch: src/patches/SDLActivity.java.patch
Applying patch: src/patches/SDLSurface.java.patch
[0m[1;31m# Command failed: ['/opt/hostedtoolcache/Python/3.11.16/x64/bin/python', '-m', 'pythonforandroid.toolchain', 'apk', '--bootstrap', 'sdl2', '--dist_name', 'mcpython', '--name', 'Minecraft Python Edition', '--version', '20100223', '--package', 'org.mcpython.mcpython', '--minsdk', '24', '--ndk-api', '24', '--private', '/home/runner/work/OGSR-AIMODE/OGSR-AIMODE/android-port/.buildozer/android/app', '--android-entrypoint', 'org.kivy.android.PythonActivity', '--android-apptheme', '@android:style/Theme.NoTitleBar', '--orientation', 'landscape', '--enable-androidx', '--copy-libs', '--local-recipes', '/home/runner/work/OGSR-AIMODE/OGSR-AIMODE/android-port/p4a-recipes', '--arch', 'arm64-v8a', '--color=always', '--storage-dir=/home/runner/work/OGSR-AIMODE/OGSR-AIMODE/android-port/.buildozer/android/platform/build-arm64-v8a', '--ndk-api=24', '--ignore-setup-py', '--debug'][0m
[0m[1;31m# ENVIRONMENT:[0m
```
