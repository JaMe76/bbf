# -*- coding: utf-8 -*-
# File: xxx.py

# Copyright 2022 Dr. Janis Meyer. All rights reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import deepdoctection as dd





if __name__=="__main__":

    path = "/home/janis/Data/full_cut_files/2a9b309dbd5214bab227451ef39235e7e17fc921.pdf"
    analyzer = get_layout_analyzer()
    df = analyzer.analyze(path=path)
    df.reset_state()

    for dp in df:
        print(dp.text)
        dp.viz(interactive=True)



