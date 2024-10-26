#! /bin/bash

cd "$(dirname $0)"
GEM5PATH=/home/jbcgames/mySimTools/gem5/build/ARM 
SCRIPTDIR=../../scripts/CortexA76_scripts_gem5
#MOREOPTIONS="--branch_predictor_type=X --issue_width=Y --rob_entries=Z"

$GEM5PATH/gem5.fast -d h264decResult $SCRIPTDIR/CortexA76.py --cmd=h264_dec --options="h264dec_testfile.264 h264dec_outfile.yuv" $MOREOPTIONS &
$GEM5PATH/gem5.fast -d h264encResult $SCRIPTDIR/CortexA76.py --cmd=h264_enc --options="h264enc_configfile.cfg" $MOREOPTIONS &
$GEM5PATH/gem5.fast -d hjgpdecResult $SCRIPTDIR/CortexA76.py --cmd=jpg2k_dec --options="-i jpg2kdec_testfile.j2k -o jpg2kdec_outfile.bmp" $MOREOPTIONS &
$GEM5PATH/gem5.fast -d hjgpencResult $SCRIPTDIR/CortexA76.py --cmd=jpg2k_enc --options="-i jpg2kenc_testfile.bmp -o jpg2kenc_outfile.j2k" $MOREOPTIONS &
$GEM5PATH/gem5.fast -d mp3decResult $SCRIPTDIR/CortexA76.py --cmd=mp3_dec --options="-w mp3dec_outfile.wav mp3dec_testfile.mp3 " $MOREOPTIONS &
$GEM5PATH/gem5.fast -d mp3encResult $SCRIPTDIR/CortexA76.py --cmd=mp3_enc --options="mp3enc_testfile.wav mp3enc_outfile.mp3" $MOREOPTIONS &
