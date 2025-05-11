from conan import ConanFile
from conan.tools.files import get, copy
import os

required_conan_version = ">=2.16.1"


class PrebuiltPicolibc(ConanFile):
    name = "prebuilt-picolibc"
    settings = "os", "arch", "compiler", "build_type"
    package_type = "static-library"
    build_policy = "missing"
    short_paths = True
    options = {
        "crt0": [
            "semihost",
            "hosted",
            "minimal",
        ]
    }
    default_options = {
        "crt0": "semihost",
    }

    def package_id(self):
        self.info.clear()

    def build(self):
        get(self,
            **self.conan_data["sources"][self.version],
            destination=self.build_folder)

    def package(self):
        destination = os.path.join(self.package_folder, "")
        copy(self, pattern="arm-none-eabi/*", src=self.build_folder,
             dst=destination, keep_path=True)
        copy(self, pattern="bin/*", src=self.build_folder,
             dst=destination, keep_path=True)
        copy(self, pattern="lib/*", src=self.build_folder,
             dst=destination, keep_path=True)

    def package_info(self):
        self.cpp_info.set_property("cmake_target_name", "picolibc")

        self.cpp_info.libs = []
        self.cpp_info.includedirs = []
        self.cpp_info.bindirs = []
        self.cpp_info.frameworkdirs = []
        self.cpp_info.libdirs = []
        self.cpp_info.resdirs = []

        short_to_long_version = {
            "11.3": "11.3.1",
            "12.2": "12.2.1",
            "12.3": "12.3.1",
            "13.2": "13.2.1",
            "13.3": "13.3.1",
            "14.2": "14.2.1",
        }
        long_version = short_to_long_version[self.version]
        specs_path = f"lib/gcc/arm-none-eabi/{long_version}/picolibcpp.specs"
        prefix = os.path.join(self.package_folder, 'arm-none-eabi')
        picolibcpp_specs = os.path.join(self.package_folder, specs_path)

        self.cpp_info.exelinkflags = [
            f"-specs={picolibcpp_specs}",
            f"--picolibc-prefix={prefix}",
            f"-oslib={str(self.options.crt0)}",
        ]

        self.output.info(f"link flags: {self.cpp_info.exelinkflags}")
        self.output.info(f"crt0: {str(self.options.crt0)}")
