"""Namespace just for importing other namespaces to avoid spamming of
various messages on import.

"""
import glob
import logging
import os
import sys
import warnings

from sensenet import __tree_ext_prefix__

logging.getLogger("tensorflow").setLevel(logging.ERROR)

warnings.filterwarnings("ignore", message=".*binary incompatibility.*")
warnings.filterwarnings("ignore", message=".*in favour of importlib.*")
warnings.filterwarnings("ignore", message=".*alias for the builtin.*")
warnings.filterwarnings("ignore", message=".*Pillow 10.*Resampling.*")
warnings.filterwarnings("ignore", message=".*distutils Version classes.*")


import numpy  # noqa: E402

with warnings.catch_warnings():
    warnings.filterwarnings("ignore", message=".*as a synonym of type.*")
    warnings.filterwarnings("ignore", message=".*binary incompatibility.*")
    warnings.filterwarnings("ignore", message=".*details.*")

    import tensorflow
    import tensorflow.keras.layers  # type: ignore

    # tensoflowjs is not available in all architectures (see setup.py)
    # but it is not mandatory for Sensenet to work
    try:
        import tensorflowjs
    except:  # noqa: E722
        tensorflowjs = None

bigml_tf_module = None

for path in sys.path:
    treelib = glob.glob(os.path.join(path, ("*%s*" % __tree_ext_prefix__)))
    if treelib:
        bigml_tf_module = tensorflow.load_op_library(treelib[0])


def import_tensorflow():
    return tensorflow


def import_bigml_treelib():
    return bigml_tf_module


def import_keras_layers():
    return tensorflow.keras.layers


def import_numpy():
    return numpy


def import_tfjs():
    return tensorflowjs
