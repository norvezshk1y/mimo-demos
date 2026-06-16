[app]
title = Kivy Demos
package.name = kivydemos
package.domain = org.kivy
source.dir = .
source.include_exts = py,png,jpg,kv,txt
version = 1.0.0
requirements = python3==3.11.9,kivy==2.3.0
orientation = portrait
fullscreen = 0
android.permissions = INTERNET
android.api = 34
android.minapi = 24
android.ndk = 25b
android.sdk = 34
android.archs = arm64-v8a
android.entrypoint = org.kivy.android.PythonActivity
android.compile_sdk_version = 34
android.gradle_dependencies =
android.enable_androidx = True
android.enable_jetifier = True
icon.filename = %(source.dir)s/icon.png
p4a.python_version = 3.11.9

[buildozer]
log_level = 2
warn_on_root = 0
