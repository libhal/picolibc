from conan import ConanFile
from conan.tools.cmake import CMake, cmake_layout


class Demo(ConanFile):
    settings = "os", "arch", "compiler", "build_type"
    generators = "CMakeDeps", "CMakeToolchain", "VirtualBuildEnv"
    options = {
        "version": [
            "12.2.1",
            "12.3.1",
        ]
    }

    def build_requirements(self):
        self.tool_requires("cmake/3.27.1")
        self.tool_requires(f"arm-gnu-toolchain/{self.options.version}")

    def requirements(self):
        self.requires(f"prebuilt-picolibc/{self.options.version}")

    def layout(self):
        cmake_layout(self)

    def build(self):
        cmake = CMake(self)
        cmake.configure()
        cmake.build()
