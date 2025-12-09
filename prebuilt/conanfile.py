from conan import ConanFile
from conan.errors import ConanInvalidConfiguration
from conan.tools.files import get
from pathlib import Path

required_conan_version = ">=2.0.6"


class PrebuiltGccPicolibc(ConanFile):
    name = "prebuilt-picolibc"
    settings = "os", "arch", "compiler", "build_type"
    package_type = "static-library"
    build_policy = "missing"
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

    def validate(self):
        if self.settings.compiler != "gcc":
            raise ConanInvalidConfiguration(
                "This package only works with GCC compiler")

    def package_id(self):
        self.info.clear()

    def package(self):
        get(self,
            **self.conan_data["sources"][self.version],
            destination=self.package_folder)

    def package_info(self):
        self.cpp_info.set_property("cmake_target_name", "picolibc")

        self.cpp_info.libs = []
        self.cpp_info.includedirs = []
        self.cpp_info.bindirs = []
        self.cpp_info.frameworkdirs = []
        self.cpp_info.libdirs = []
        self.cpp_info.resdirs = []

        SHORT_TO_LONG_VERSION = {
            "11.3": "11.3.1",
            "12.2": "12.2.1",
            "12.3": "12.3.1",
            "12":   "12.3.1",
            "13.2": "13.2.1",
            "13.3": "13.3.1",
            "13": "13.3.1",
            "14.2": "14.2.1",
            "14":   "14.2.1",
        }

        LONG_VERSION = SHORT_TO_LONG_VERSION[self.version]
        PREFIX = Path(self.package_folder) / 'arm-none-eabi'
        PICOLIB_CPP_SPECS = Path(self.package_folder) / 'lib' / 'gcc' / \
            'arm-none-eabi' / LONG_VERSION / 'picolibcpp.specs'

        self.cpp_info.exelinkflags = [
            f"-specs={PICOLIB_CPP_SPECS}",
            f"--picolibc-prefix={PREFIX}",
            f"-oslib={str(self.options.crt0)}",
        ]

        self.output.info(f"link flags: {self.cpp_info.exelinkflags}")
        self.output.info(f"crt0: {str(self.options.crt0)}")
