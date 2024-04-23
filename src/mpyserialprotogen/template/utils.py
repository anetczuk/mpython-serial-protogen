# Copyright (c) 2022, Arkadiusz Netczuk <dev.arnet@gmail.com>
# All rights reserved.
#
# This source code is licensed under the BSD 3-Clause license found in the
# LICENSE file in the root directory of this source tree.
#

import os
import shutil


SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

ROOT_DIR = os.path.join(SCRIPT_DIR, os.pardir)


def copy_file(source_file_path, target_dir_path):
    source_path = os.path.join(ROOT_DIR, source_file_path)
    shutil.copy(source_path, target_dir_path)
