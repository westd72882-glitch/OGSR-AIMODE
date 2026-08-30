# Build 33 — failure

commit: 4bb4f1ab1a860c534dd176edf593817955e6d53f
run: https://github.com/westd72882-glitch/OGSR-AIMODE/actions/runs/33297973252

## Diagnosis (log has 635 lines)
```
FAILURE: Build failed with an exception.

* Where:
Build file '/home/runner/work/OGSR-AIMODE/OGSR-AIMODE/android-port/.buildozer/android/platform/build-arm64-v8a/dists/mcpython/build.gradle' line: 30

* What went wrong:
A problem occurred evaluating root project 'mcpython'.
> Value is null

* Try:
> Run with --stacktrace option to get the stack trace.
> Run with --info or --debug option to get more log output.
> Run with --scan to get full insights.
> Get more help at https://help.gradle.org.

Deprecated Gradle features were used in this build, making it incompatible with Gradle 9.0.

You can use '--warning-mode all' to show the individual deprecation warnings and determine if they come from your own scripts or plugins.

For more on this, please refer to https://docs.gradle.org/8.14.3/userguide/command_line_interface.html#sec:command_line_warnings in the Gradle documentation.

BUILD FAILED in 27s


  STDERR:

[1m[INFO][0m:    STDOUT (last 20 lines of 41):
[33m	* Where:	
Build file '/home/runner/work/OGSR-AIMODE/OGSR-AIMODE/android-port/.buildozer/android/platform/build-arm64-v8a/dists/mcpython/build.gradle' line: 30	
	
* What went wrong:	
A problem occurred evaluating root project 'mcpython'.	
> Value is null	
	
* Try:	
> Run with --stacktrace option to get the stack trace.	
> Run with --info or --debug option to get more log output.	
> Run with --scan to get full insights.	
> Get more help at https://help.gradle.org.	
	
Deprecated Gradle features were used in this build, making it incompatible with Gradle 9.0.	
	
You can use '--warning-mode all' to show the individual deprecation warnings and determine if they come from your own scripts or plugins.	
	
For more on this, please refer to https://docs.gradle.org/8.14.3/userguide/command_line_interface.html#sec:command_line_warnings in the Gradle documentation.	
	
BUILD FAILED in 27s[39m
[1m[INFO][0m:    STDERR:
[31m	[39m
[1m[INFO][0m:    [33mENV:[39m
export SHELL='/bin/bash'
export SELENIUM_JAR_PATH='/usr/share/java/selenium-server.jar'
export CONDA='/usr/share/miniconda'
export GITHUB_WORKSPACE='/home/runner/work/OGSR-AIMODE/OGSR-AIMODE'
export JAVA_HOME_11_X64='/usr/lib/jvm/temurin-11-jdk-amd64'
export JAVA_HOME_25_X64='/usr/lib/jvm/temurin-25-jdk-amd64'
export PKG_CONFIG_PATH='/opt/hostedtoolcache/Python/3.11.16/x64/lib/pkgconfig'
export GITHUB_PATH='/home/runner/work/_temp/_runner_file_commands/add_path_ce464404-e737-4da3-ac98-9809b454931f'
export GITHUB_ACTION='__run_2'
export JAVA_HOME='/opt/hostedtoolcache/Java_Temurin-Hotspot_jdk/17.0.20-1/x64'
export GITHUB_RUN_NUMBER='33'
export RUNNER_NAME='GitHub Actions 1000000701'
export GRADLE_HOME='/usr/share/gradle-9.7.1'
export GITHUB_REPOSITORY_OWNER_ID='306517529'
export ACTIONS_RUNNER_ACTION_ARCHIVE_CACHE='/opt/actionarchivecache'
export XDG_CONFIG_HOME='/home/runner/.config'
export Python_ROOT_DIR='/opt/hostedtoolcache/Python/3.11.16/x64'
export MEMORY_PRESSURE_WRITE='c29tZSAyMDAwMDAgMjAwMDAwMAA='
export DOTNET_SKIP_FIRST_TIME_EXPERIENCE='1'
export ANT_HOME='/usr/share/ant'
export JAVA_HOME_8_X64='/usr/lib/jvm/temurin-8-jdk-amd64'
--- task/compile errors ---
```

## Recipe stage
```
c files: 33
```
