from conans import ConanFile, CMake, tools
import os
import shutil

class ENetConan(ConanFile):
    name = "enet"
    version = "1.3.14"
    generators = "cmake"
    settings = "os", "arch", "compiler", "build_type"

    options = {"shared": [True, False]}
    default_options = "shared=True"

    license = "Copyright (c) 2002-2019 Lee Salzman"
    description = "A thin, simple and robust network communication layer on top of UDP (User Datagram Protocol)."

    def source(self):
        basename = "enet-%s" % self.version
        fname = "%s.tar.gz" % basename
        tools.download("http://enet.bespin.org/download/%s" % fname, fname)
        tools.unzip(fname)
        shutil.move(basename, "source_folder")
        tools.replace_in_file(os.path.join("source_folder", "CMakeLists.txt"), "add_library(enet STATIC", "add_library(enet")
        os.remove(os.path.join("source_folder", "enet64.lib"))
        os.remove(os.path.join("source_folder", "enet.lib"))


    def build(self):
        cmake = CMake(self)
        cmake.configure(source_folder="source_folder")
        cmake.build()

    def package(self):
        self.copy(pattern="*.h", dst="include", src=os.path.join("source_folder", "include"))
        self.copy(pattern="*.so*", dst="lib", keep_path=False)
        self.copy(pattern="*.lib", dst="lib", keep_path=False)
        self.copy(pattern="*.dll", dst="bin", keep_path=False)
        
    def package_info(self):
        self.cpp_info.libs = tools.collect_libs(self)