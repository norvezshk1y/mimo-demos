[app]
title = Kivy Demos
package.name = kivydemos
package.domain = org.kivy
source.dir = .
source.include_exts = py,png,jpg,kv,txt
version = 1.0.0
requirements = python3,kivy
orientation = portrait
fullscreen = 0
android.permissions = INTERNET
android.api = 31
android.minapi = 21
android.ndk = 25b
android.sdk = 33
android.archs = arm64-v8a
android.entrypoint = org.kivy.android.PythonActivity
android.compile_sdk_version = 31
android.gradle_dependencies =
android.enable_androidx = True
android.enable_jetifier = True
icon.filename = %(source.dir)s/icon.png

[buildozer]
log_level = 2
warn_on_root = 0
