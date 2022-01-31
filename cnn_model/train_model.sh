#!/bin/bash

conda activate openmmlab
cd mmdetection && python tools/train.py cascade_rcnn_r50_fpn_20e_coco.py --no-validate --work-dir .