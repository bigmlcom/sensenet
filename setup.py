"""Setup for package sensenet
"""

import os
import platform
import sys

import pkg_resources
import setuptools

from sensenet import __tree_ext_prefix__, __version__

here = os.path.abspath(os.path.dirname(__file__))

TF_PACKAGES = ["tensorflow-gpu", "tensorflow-cpu"]
TF_VER = ">=2.16,<2.17"

deps = [
    "tf-keras~=2.16",
    "pillow>=10.2.0,<10.2.1",
    "scikit-learn>=1.4,<1.4.1",
    "pytest>=7.4.2,<7.5",
]

# The installation of `tensorflow-gpu` should be specific to canonical
# docker images distributed by the Tensorflow team.  If they've
# installed tensorflow-gpu, we shouldn't try to install tensorflow on
# top of them.
if not any(pkg.key in TF_PACKAGES for pkg in pkg_resources.working_set):
    # If we do have to grab tensorflow, pull in the correct package
    # for our architecture
    if platform.machine() == "aarch64" and platform.system() == "Linux":
        deps += ["tensorflow-aarch64%s" % TF_VER]
    else:
        deps += ["tensorflow%s" % TF_VER]

# Unfortunately, there's no tensorflowjs package on pypi for aarch64,
# as far as I can tell.  Also, it seems that the aarch64 build is
# quite picky about its numpy version, and you have to let it pull in
# the exact version that tensorflow was built with. We also avoid setting
# the tensorflowjs version to allow looking for the correct match.
if platform.machine() not in ["aarch64", "arm64"]:
    deps += ["tensorflowjs",
             "numpy>=1.26.3,<1.27"]

# Get the long description from the relevant file
with open(os.path.join(here, "README.md"), "r") as f:
    long_description = f.read()

if os.name == "nt":
    modules = []
else:
    try:
        import tensorflow as tf
    except ModuleNotFoundError:
        raise ImportError("Tensorflow is not in the build environment.")

    compile_args = ["-std=c++14", "-fPIC"] + tf.sysconfig.get_compile_flags()

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
    python_requires=">=3.9",
    ext_modules=modules,
    install_requires=deps,
)
