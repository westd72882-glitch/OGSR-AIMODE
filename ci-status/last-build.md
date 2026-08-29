# Build 30 — failure

commit: c3d2507b04ef98454713b8175255dfa1e079d305
run: https://github.com/westd72882-glitch/OGSR-AIMODE/actions/runs/33278392621

## Compile errors
```
591:[1m[90m[DEBUG][39m[0m:   	clang: error: no such file or directory: 'mc/JavaUtils.c'
630:clang: error: no such file or directory: 'mc/JavaUtils.c'
```

## Cythonise + recipe
```
702:[1m[INFO][0m:    Cythonize mc/net/minecraft/game/level/generator/LevelGenerator.pyx
705:[1m[INFO][0m:    Cythonize mc/net/minecraft/game/level/generator/noise/NoiseGeneratorOctaves.pyx
708:[1m[INFO][0m:    Cythonize mc/net/minecraft/game/level/generator/noise/NoiseGeneratorDistort.pyx
711:[1m[INFO][0m:    Cythonize mc/net/minecraft/game/level/generator/noise/NoiseGeneratorPerlin.pyx
714:[1m[INFO][0m:    Cythonize mc/net/minecraft/game/level/block/BlockFire.pyx
717:[1m[INFO][0m:    Cythonize mc/net/minecraft/game/level/block/BlockFluid.pyx
720:[1m[INFO][0m:    Cythonize mc/net/minecraft/game/level/block/BlockFlowing.pyx
723:[1m[INFO][0m:    Cythonize mc/net/minecraft/game/level/block/Block.pyx
726:[1m[INFO][0m:    Cythonize mc/net/minecraft/game/entity/Entity.pyx
729:[1m[INFO][0m:    Cythonize mc/net/minecraft/game/entity/EntityLiving.pyx
732:[1m[INFO][0m:    Cythonize mc/net/minecraft/game/entity/EntityCreature.pyx
735:[1m[INFO][0m:    Cythonize mc/net/minecraft/game/physics/AxisAlignedBB.pyx
907:[1m[INFO][0m:    mcgame: numpy headers at /home/runner/work/OGSR-AIMODE/OGSR-AIMODE/android-port/.buildozer/android/platform/build-arm64-v8a/build/python-installs/mcpython/arm64-v8a/numpy/_core/include
1683:[1m[INFO][0m:    mcgame: installing /home/runner/work/OGSR-AIMODE/OGSR-AIMODE/android-port/.buildozer/android/platform/build-arm64-v8a/build/other_builds/mcgame/arm64-v8a__ndk_target_24/mcgame/build/lib.linux-x86_64-cpython-314 into /home/runner/work/OGSR-AIMODE/OGSR-AIMODE/android-port/.buildozer/android/platform/build-arm64-v8a/build/python-installs/mcpython/arm64-v8a
1684:[1m[INFO][0m:    mcgame: pre-installing pure Python requirements into /home/runner/work/OGSR-AIMODE/OGSR-AIMODE/android-port/.buildozer/android/platform/build-arm64-v8a/build/python-installs/mcpython/arm64-v8a
pyx: 66  c: 33
```

## Failure (log has 2021 lines)
```

  RAN: /usr/bin/bash -c 'source venv/bin/activate && pip install -U pip'

  STDOUT:
Traceback (most recent call last):
  File [35m"/home/runner/work/OGSR-AIMODE/OGSR-AIMODE/android-port/.buildozer/android/platform/build-arm64-v8a/build/venv/bin/pip"[0m, line [35m3[0m, in [35m<module>[0m
    from pip._internal.cli.main import main
  File [35m"/home/runner/work/OGSR-AIMODE/OGSR-AIMODE/android-port/.buildozer/android/platform/build-arm64-v8a/build/venv/lib/python3.14/site-packages/pip/_internal/cli/main.py"[0m, line [35m11[0m, in [35m<module>[0m
    from pip._internal.cli.autocompletion import autocomplete
  File [35m"/home/runner/work/OGSR-AIMODE/OGSR-AIMODE/android-port/.buildozer/android/platform/build-arm64-v8a/build/venv/lib/python3.14/site-packages/pip/_internal/cli/autocompletion.py"[0m, line [35m12[0m, in [35m<module>[0m
    from pip._internal.cli.main_parser import create_main_parser
  File [35m"/home/runner/work/OGSR-AIMODE/OGSR-AIMODE/android-port/.buildozer/android/platform/build-arm64-v8a/build/venv/lib/python3.14/site-packages/pip/_internal/cli/main_parser.py"[0m, line [35m9[0m, in [35m<module>[0m
    from pip._internal.build_env import get_runnable_pip
  File [35m"/home/runner/work/OGSR-AIMODE/OGSR-AIMODE/android-port/.buildozer/android/platform/build-arm64-v8a/build/venv/lib/python3.14/site-packages/pip/_internal/build_env/__init__.py"[0m, line [35m8[0m, in [35m<module>[0m
    from pip._internal.build_env.installer import (
    ...<2 lines>...
    )
  File [35m"/home/runner/work/OGSR-AIMODE/OGSR-AIMODE/android-port/.buildozer/android/platform/build-arm64-v8a/build/venv/lib/python3.14/site-packages/pip/_internal/build_env/installer.py"[0m, line [35m14[0m, in [35m<module>[0m
    from pip._internal.exceptions import (
    ...<4 lines>...
    )
[1;35mImportError[0m: [35mcannot import name 'BuildDependencyInstallError' from 'pip._internal.exceptions' (/home/runner/work/OGSR-AIMODE/OGSR-AIMODE/android-port/.buildozer/android/platform/build-arm64-v8a/build/venv/lib/python3.14/site-packages/pip/_internal/exceptions.py)[0m


  STDERR:

Traceback (most recent call last):
  File "<frozen runpy>", line 198, in _run_module_as_main
  File "<frozen runpy>", line 88, in _run_code
  File "/home/runner/work/OGSR-AIMODE/OGSR-AIMODE/android-port/.buildozer/android/platform/python-for-android/pythonforandroid/toolchain.py", line 1290, in <module>
    main()
  File "/home/runner/work/OGSR-AIMODE/OGSR-AIMODE/android-port/.buildozer/android/platform/python-for-android/pythonforandroid/entrypoints.py", line 18, in main
    ToolchainCL()
  File "/home/runner/work/OGSR-AIMODE/OGSR-AIMODE/android-port/.buildozer/android/platform/python-for-android/pythonforandroid/toolchain.py", line 721, in __init__
    getattr(self, command)(args)
  File "/home/runner/work/OGSR-AIMODE/OGSR-AIMODE/android-port/.buildozer/android/platform/python-for-android/pythonforandroid/toolchain.py", line 104, in wrapper_func
    build_dist_from_args(ctx, dist, args)
  File "/home/runner/work/OGSR-AIMODE/OGSR-AIMODE/android-port/.buildozer/android/platform/python-for-android/pythonforandroid/toolchain.py", line 163, in build_dist_from_args
    build_recipes(build_order, python_modules, ctx,
  File "/home/runner/work/OGSR-AIMODE/OGSR-AIMODE/android-port/.buildozer/android/platform/python-for-android/pythonforandroid/build.py", line 554, in build_recipes
    run_pymodules_install(
  File "/home/runner/work/OGSR-AIMODE/OGSR-AIMODE/android-port/.buildozer/android/platform/python-for-android/pythonforandroid/build.py", line 877, in run_pymodules_install
    shprint(sh.bash, '-c', (
  File "/home/runner/work/OGSR-AIMODE/OGSR-AIMODE/android-port/.buildozer/android/platform/python-for-android/pythonforandroid/logger.py", line 174, in shprint
    for line in output:
  File "/opt/hostedtoolcache/Python/3.11.16/x64/lib/python3.11/site-packages/sh/__init__.py", line 876, in __next__
    self.wait()
  File "/opt/hostedtoolcache/Python/3.11.16/x64/lib/python3.11/site-packages/sh/__init__.py", line 793, in wait
    self.handle_command_exit_code(exit_code)
  File "/opt/hostedtoolcache/Python/3.11.16/x64/lib/python3.11/site-packages/sh/__init__.py", line 820, in handle_command_exit_code
    raise exc
sh.ErrorReturnCode_1: 

  RAN: /usr/bin/bash -c 'source venv/bin/activate && pip install -U pip'

  STDOUT:
Traceback (most recent call last):
  File [35m"/home/runner/work/OGSR-AIMODE/OGSR-AIMODE/android-port/.buildozer/android/platform/build-arm64-v8a/build/venv/bin/pip"[0m, line [35m3[0m, in [35m<module>[0m
    from pip._internal.cli.main import main
  File [35m"/home/runner/work/OGSR-AIMODE/OGSR-AIMODE/android-port/.buildozer/android/platform/build-arm64-v8a/build/venv/lib/python3.14/site-packages/pip/_internal/cli/main.py"[0m, line [35m11[0m, in [35m<module>[0m
    from pip._internal.cli.autocompletion import autocomplete
  File [35m"/home/runner/work/OGSR-AIMODE/OGSR-AIMODE/android-port/.buildozer/android/platform/build-arm64-v8a/build/venv/lib/python3.14/site-packages/pip/_internal/cli/autocompletion.py"[0m, line [35m12[0m, in [35m<module>[0m
    from pip._internal.cli.main_parser import create_main_parser
  File [35m"/home/runner/work/OGSR-AIMODE/OGSR-AIMODE/android-port/.buildozer/android/platform/build-arm64-v8a/build/venv/lib/python3.14/site-packages/pip/_internal/cli/main_parser.py"[0m, line [35m9[0m, in [35m<module>[0m
    from pip._internal.build_env import get_runnable_pip
  File [35m"/home/runner/work/OGSR-AIMODE/OGSR-AIMODE/android-port/.buildozer/android/platform/build-arm64-v8a/build/venv/lib/python3.14/site-packages/pip/_internal/build_env/__init__.py"[0m, line [35m8[0m, in [35m<module>[0m
    from pip._internal.build_env.installer import (
    ...<2 lines>...
    )
  File [35m"/home/runner/work/OGSR-AIMODE/OGSR-AIMODE/android-port/.buildozer/android/platform/build-arm64-v8a/build/venv/lib/python3.14/site-packages/pip/_internal/build_env/installer.py"[0m, line [35m14[0m, in [35m<module>[0m
    from pip._internal.exceptions import (
    ...<4 lines>...
    )
[1;35mImportError[0m: [35mcannot import name 'BuildDependencyInstallError' from 'pip._internal.exceptions' (/home/runner/work/OGSR-AIMODE/OGSR-AIMODE/android-port/.buildozer/android/platform/build-arm64-v8a/build/venv/lib/python3.14/site-packages/pip/_internal/exceptions.py)[0m


  STDERR:


[0m[1;31m# Command failed: ['/opt/hostedtoolcache/Python/3.11.16/x64/bin/python', '-m', 'pythonforandroid.toolchain', 'create', '--dist_name=mcpython', '--bootstrap=sdl2', '--requirements=python3,kivy,numpy,pillow,nbtlib,mcgame', '--arch=arm64-v8a', '--copy-libs', '--local-recipes', '/home/runner/work/OGSR-AIMODE/OGSR-AIMODE/android-port/p4a-recipes', '--color=always', '--storage-dir=/home/runner/work/OGSR-AIMODE/OGSR-AIMODE/android-port/.buildozer/android/platform/build-arm64-v8a', '--ndk-api=24', '--ignore-setup-py', '--debug'][0m
[0m[1;31m# ENVIRONMENT:[0m
```
