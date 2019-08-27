import argparse
import glob
import os
import subprocess

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Process input video")
    parser.add_argument(
        '--input-video', 
        help="Path to the input video file (include ext)",
        required=True
    )
    parser.add_argument(
        '--output-audio', 
        help="The name of the output folder to store the audio clip in.",
        required=True
    )
    parser.add_argument(
        '--output-images', 
        help="The name of the output image folder to store the output frames in.",
        required=True
    )

    args = parser.parse_args()

    os.makedirs(args.output_audio, exist_ok=True)
    os.makedirs(args.output_images, exist_ok=True)

    subprocess.run("ffmpeg -i {} {}/audio.aac"
                  .format(args.input_video, args.output_audio),
                   shell=True, check=True
                  )

    subprocess.run("ffmpeg -i {} {}/%05d_video.jpg -hide_banner"
                  .format(args.input_video, args.output_images),
                   shell=True, check=True
                  )
