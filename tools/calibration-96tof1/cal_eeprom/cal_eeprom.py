#
# BSD 3-Clause License
#
# Copyright (c) 2019, Analog Devices, Inc.
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
# 1. Redistributions of source code must retain the above copyright notice, this
#    list of conditions and the following disclaimer.
#
# 2. Redistributions in binary form must reproduce the above copyright notice,
#    this list of conditions and the following disclaimer in the documentation
#    and/or other materials provided with the distribution.
#
# 3. Neither the name of the copyright holder nor the names of its
#    contributors may be used to endorse or promote products derived from
#    this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
# FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
# DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
# SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
# OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#
'''
===================
Calibration Map
===================

This module contains functions for generating calibration map for storing in EEPROM, storing in file, reading it back from file and parsing the map.
'''

# import os
import logging
import logging.config
import click
import json
import os.path
from os import path
from pathlib import PurePath
from cal_map import cal_map
from cal_map_consts import get_cal_key, get_lf_key, LINEAR_CAL_FILE_NAME
from cal_map_utils import check_folder_structure


def setup_logging():
    with open('./../logger.json', 'r') as f:
        config = json.load(f)
        logging.config.dictConfig(config)


def generate_eeprom(source_folder_path, bin_file_path):
    load_file_folders = check_folder_structure(source_folder_path)
    cal = cal_map()
    cal.init_default_cal_map()
    for folder in load_file_folders:
        mode = PurePath(folder).parts[-1].lower()
        cal.add_load_files_to_map(get_lf_key(mode), folder)

        json_path = str(PurePath(folder, LINEAR_CAL_FILE_NAME))
        if (path.exists(json_path)):
            cal.add_json_to_map(get_cal_key(mode), json_path)
        else:
            print(json_path + " not found.")
    # cal.display_cal_map()
    cal.save_cal_map(bin_file_path)
    print("calibration map saved to " + bin_file_path)
    pass


@ click.command()
@ click.argument('source-folder-path', type=click.Path(exists=True))
@ click.argument('bin-file-name', type=click.Path(exists=False))
def run_tool(source_folder_path, bin_file_name, **kwargs):
    logger = logging.getLogger(__name__)
    generate_eeprom(source_folder_path, bin_file_name)


'''
Start point of program
---------------------------------
'''
if __name__ == "__main__":
    setup_logging()
    logger = logging.getLogger(__name__)
    run_tool()
