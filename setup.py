"""Setup for package sensenet
"""

try:
    import tensorflow as tf
except ModuleNotFoundError:
    raise ImportError("Tensorflow is not in the build environment.")

import os
import sys
import pkg_resources
import setuptools

from sensenet import __version__, __tree_ext_prefix__

here = os.path.abspath(os.path.dirname(__file__))

TF_PACKAGES = ["tensorflow-gpu", "tensorflow-cpu"]
TF_VER = ">=2.8,<2.9"
M1 = "sys_platform=='Darwin' and platform_machine=='arm64'"
OTHER = "sys_platform!='Darwin' or platform_machine!='arm64'"

deps = [
    "importlib-resources>=5.4,<5.5",
    "numpy>=1.21,<1.22",
    "pillow>=9.0,<9.1",
    "tensorflowjs>=3.13,<3.14",
]

# The installation of `tensorflow-gpu` should be specific to canonical
# docker images distributed by the Tensorflow team.  If they've
# installed tensorflow-gpu, we shouldn't try to install tensorflow on
# top of them.
if not any(pkg.key in TF_PACKAGES for pkg in pkg_resources.working_set):
    deps += [
        # MacOS running on the M1 has a specific tensorflow build
        "tensorflow-macos%s;%s" % (TF_VER, M1),
        "tensorflow%s;%s" % (TF_VER, OTHER),
    ]

# Get the long description from the relevant file
with open(os.path.join(here, "README.md"), "r") as f:
    long_description = f.read()

if os.name == "nt":
    modules = []
else:
    compile_args = ["-std=c++14", "-fPIC"] + tf.sysconfig.get_compile_flags()
    sys.stderr.write(tf.sysconfig.get_lib() + "\n")
    sys.stderr.flush()
    tree_module = setuptools.Extension(
        __tree_ext_prefix__,
        define_macros=[("MAJOR_VERSION", "1"), ("MINOR_VERSION", "1")],
        include_dirs=[tf.sysconfig.get_include()],
        library_dirs=[tf.sysconfig.get_lib()],
        extra_compile_args=compile_args,
        extra_link_args=tf.sysconfig.get_link_flags(),
        sources=["cpp/tree_op.cc"],
    )

    modules = [tree_module]

setuptools.setup(
    name="bigml-sensenet",
    version=__version__,
    author="BigML Team",
    author_email="team@bigml.com",
    url="http://bigml.com/",
    description="Network builder for bigml deepnet topologies",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(),
    package_data={"sensenet": ["sensenet_metadata.json.gz"]},
    ext_modules=modules,
    install_requires=deps,
)
