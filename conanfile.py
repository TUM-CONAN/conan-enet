from conans import ConanFile, CMake, tools
import os


class ENetConan(ConanFile):
    name = "enet"
    version = "0.1"
    generators = "cmake"
    settings = "os", "arch", "compiler", "build_type"

    options = {"BUILD_SHARED_LIBS": [True, False]}
    default_options = "BUILD_SHARED_LIBS=False"
    exports_sources = "include*", "*.c", "CMakeLists.txt"

    exports = ["CMakeLists.txt"]

    license="Copyright (c) 2002-2019 Lee Salzman"
    description="A thin, simple and robust network communication layer on top of UDP (User Datagram Protocol)."

    scm = {
        "type": "git",
        "url": "https://github.com/lsalzman/enet.git",
        "revision": "master",
    }
    
    def build(self):
        cmake = CMake(self)
        cmake.definitions["BUILD_SHARED_LIBS"] = self.options.BUILD_SHARED_LIBS
        cmake.configure()
        cmake.build()

    def package(self):
        self.copy(pattern="*.h", dst="include", src="include")
        self.copy(pattern="*.so*", dst="lib", keep_path=False )
        self.copy(pattern="*.lib", dst="lib", keep_path=False)
        self.copy(pattern="*.dll", dst="bin", keep_path=False)
        
    def package_info(self):
        self.cpp_info.libs = tools.collect_libs(self)