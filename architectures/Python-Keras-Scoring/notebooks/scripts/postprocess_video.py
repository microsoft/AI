import argparse
import os
import subprocess

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Process input video")
    parser.add_argument(
        '--video',
        help="Name of the output video (excluding ext)"
    )
    parser.add_argument(
        '--images-dir', 
        help="The input image directory of frames to stitch together.",
        required=True
    )
    parser.add_argument(
        '--input-audio', 
        help="The input audio directory containing the audio file.",
        required=True
    )
    parser.add_argument(
        '--output-dir', 
        help="The output directory to save the stitched-together video into.",
        required=True
    )

    args = parser.parse_args()

    os.makedirs(args.output_dir, exist_ok=True)

    subprocess.run("ffmpeg -framerate 30 -i {}/%05d_video.jpg -c:v libx264 -profile:v high -crf 20 -pix_fmt yuv420p "
                   "-y {}/video_without_audio.mp4"
                   .format(args.images_dir, args.output_dir),
                   shell=True, check=True
                  )

    video_name = args.video or 'video'

    subprocess.run("ffmpeg -i {}/video_without_audio.mp4 -i {}/audio.aac -map 0:0 -map 1:0 -vcodec "
                   "copy -acodec copy -y {}/{}_processed.mp4"
                   .format(args.output_dir, args.input_audio, args.output_dir, video_name),
                   shell=True, check=True
                  )
