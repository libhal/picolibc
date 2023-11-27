from conan import ConanFile
from conan.tools.files import get, copy, download, mkdir, chdir
from conan.errors import ConanInvalidConfiguration
from conan.tools.meson import Meson, MesonToolchain
import os


required_conan_version = ">=2.0.6"


class picolibc(ConanFile):
    name = "picolibc"
    license = ("GPL-2.0-only")
    homepage = "https://keithp.com/picolibc"
    description = ("Conan installer for the GNU Arm Embedded Toolchain")
    topics = ("picolibc", "libstdc", "embedded", "arm", "riscv", "xtensa")
    settings = "os", "arch", "compiler", "build_type"
    package_type = "static-library"
    generators = "VirtualBuildEnv"
    short_paths = True

    @property
    def _settings_build(self):
        return getattr(self, "settings_build", self.settings)

    def build_requirements(self):
        self.tool_requires("ninja/1.11.1")
        self.tool_requires("meson/1.3.0")

    def package_id(self):
        del self.info.settings.build_type

    def validate(self):
        pass

    def generate(self):
        build_path = os.path.join(self.build_folder, "build")
        mkdir(self, build_path)
        tc = MesonToolchain(self)
        is_baremetal = str(self.settings.os) == "baremetal"
        if is_baremetal and str(self.settings.arch).startswith("cortex-"):
            print("BAREMETAL ARM NONE EABI")
            arch = "arm-none-eabi"
            tc.preprocessor_definitions["includedir"] = f"picolibc/{arch}/include"
            tc.preprocessor_definitions["libdir"] = f"picolibc/{arch}/lib"
            tc.generate()
        # #!/bin/sh
        # ARCH=riscv64-unknown-elf
        # DIR=`dirname $0`
        # meson "$DIR" \
        #     -Dincludedir=picolibc/$ARCH/include \
        #     -Dlibdir=picolibc/$ARCH/lib \
        #     --cross-file "$DIR"/cross-$ARCH.txt \
        #     "$@"

    def build(self):
        get(self,
            **self.conan_data.get("sources", {}).get(self.version),
            destination=self.build_folder, strip_root=True)
        build_path = os.path.join(self.build_folder, "build")
        with chdir(self, build_path):
            meson = Meson(self)
            meson.configure()
            meson.build()
            # os.system("../scripts/do-arm-configure")
            # os.system("ninja")

    def package(self):
        copy(self, "*",
             src=os.path.join(self.build_folder, "build"),
             dst=self.package_folder)

    def package_info(self):
        self.cpp_info.includedirs = []
        spec_file = os.path.join(self.package_folder, "bin/picolibc.specs")
        self.cpp_info.exelinkflags = ["--specs=" + spec_file]
