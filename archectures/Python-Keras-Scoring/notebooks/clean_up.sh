#!/bin/bash

# remove tmp files
rm -rf local_test_orangutan

# rm tmp dirs
rm -rf output_dir
rm -rf content_dir

# rm downloaded video and audio files
rm *.mp4
rm *.mp4.*
rm *.mp3

# rm jnl files from azcopy
rm -rf *.jnl
