# picolibc

Conan package for the picolibc library.

## Using `prebuilt-picolibc`

Currently only supports ARM GNU Toolchain. There are no plans to support
additional architectures unless the picolibc project decides to support
additional projects. The `picolibc` project will be buildable for any target
platform, solving the support issue.

To use this project:

```python
def build_requirements(self):
    self.tool_requires("arm-gnu-toolchain/12.2.1")

def requirements(self):
    self.requires("prebuilt-picolibc/12.2.1")
```

The `arm-gnu-toolchain` version must match the `prebuilt-picolibc` version exactly.
