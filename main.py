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


def get_layout_analyzer():

    layout_config_path = (dd.get_configs_dir_path() / "dd/d2/layout/CASCADE_RCNN_R_50_FPN_GN_nms_higher.yaml").as_posix()
    layout_weights_path = "/home/janis/Experiments/fine_tune_xrf_d2/pdocs_170223_2/model_0000199.pth"
    categories_layout={
                "1": dd.LayoutType.text,
                "2": dd.LayoutType.title,
                "3": dd.LayoutType.list,
                "4": dd.LayoutType.table,
                "5": dd.LayoutType.figure,
            }
    config_overwrite = [f"NMS_THRESH_CLASS_AGNOSTIC=0.2",
                        f"MODEL.ROI_HEADS.SCORE_THRESH_TEST=0.068",
                        f"MODEL.ROI_HEADS.NMS_THRESH_TEST=0.2"]
    d_layout = dd.D2FrcnnDetector(layout_config_path, layout_weights_path, categories_layout, config_overwrite, device="cuda")
    layout = dd.ImageLayoutService(d_layout, to_image=True,)
    tess_ocr_config_path = "/home/janis/Repos/bbf/pedocs/conf_tesseract.yaml"
    #d_tess_ocr = dd.TesseractOcrDetector(tess_ocr_config_path)
    d_tess_ocr = dd.TextractOcrDetector(text_lines=True)
    text = dd.TextExtractionService(d_tess_ocr)

    match = dd.MatchingService(
        parent_categories=[dd.LayoutType.text,
                           dd.LayoutType.title,
                           dd.LayoutType.list,
                           dd.LayoutType.table,
                           dd.LayoutType.figure],
        child_categories=dd.LayoutType.line,
        matching_rule="ioa",
        threshold=0.4,
    )

    order = dd.TextOrderService(
        text_container=dd.LayoutType.line,
        floating_text_block_names=[dd.LayoutType.title, dd.LayoutType.text, dd.LayoutType.list],
        text_block_names=[
            dd.LayoutType.title,
            dd.LayoutType.text,
            dd.LayoutType.list,
            dd.LayoutType.cell,
            dd.CellType.header,
            dd.CellType.body,
        ],
    )

    pipe = dd.DoctectionPipe(pipeline_component_list=[layout,text,match,order])
    pipe.page_parser = dd.PageParsingService(
            text_container=dd.LayoutType.line,
            top_level_text_block_names=[dd.LayoutType.title,
                                        dd.LayoutType.text,
                                        dd.LayoutType.list,
                                        dd.LayoutType.table],
        )

    return pipe




if __name__=="__main__":

    analyzer = get_layout_analyzer()

    df = analyzer.analyze(path="/home/janis/Data/full_cut_files/e353008060d8d539fc1824f3672251bf0522c599.pdf")
    df.reset_state()

    for dp in df:
        #page = dd.Page.from_image(dp,text_container=dd.LayoutType.line,top_level_text_block_names=[dd.LayoutType.title, dd.LayoutType.text, dd.LayoutType.list,dd.LayoutType.table,dd.LayoutType.figure])
        print(dp.text)

