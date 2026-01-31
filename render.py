import subprocess
import os
import sys
import argparse

def get_video_duration(video_path):
    """Get video duration in seconds using ffprobe."""
    cmd = [
        "ffprobe", 
        "-v", "error", 
        "-show_entries", "format=duration", 
        "-of", "default=noprint_wrappers=1:nokey=1", 
        video_path
    ]
    result = subprocess.run(cmd, capture_output=True, text=True)
    try:
        if result.returncode != 0:
            return None
        return float(result.stdout.strip())
    except ValueError:
        return None

def find_latest_video(scene_name, quality="480p15"):
    """Finds the rendered video file. Manim directory structure can be complex."""
    # Common Manim output structure: media/videos/<module_name>/<quality>/<scene_name>.mp4
    # We might need to search recursively if the path isn't obvious
    base_dir = os.path.join("media", "videos")
    
    # Try the standard path first: media/videos/<module_name>/<quality>/<scene_name>.mp4
    # But module name depends on input file.
    # Let's search for the scene file name in media/videos
    
    search_name = f"{scene_name}.mp4"
    for root, dirs, files in os.walk(base_dir):
        if search_name in files:
             # Check if it matches the quality folder if possible, or just take the first found
             if quality in root:
                 return os.path.join(root, search_name)
    
    return None

def main():
    parser = argparse.ArgumentParser(description="Render Manim scene with audio post-processing.")
    parser.add_argument("file", help="Path to the python file containing the Scene")
    parser.add_argument("scene", help="Name of the Scene class to render")
    parser.add_argument("--quality", "-q", default="l", choices=["l", "m", "h", "k"], 
                        help="Render quality (l=480p15, m=720p30, h=1080p60, k=2160p60)")
    parser.add_argument("--preview", "-p", action="store_true", help="Preview (open) file after render")
    parser.add_argument("--audio", "-a", help="Path to audio file", default="assets/ambient.mp3")
    
    args = parser.parse_args()

    # Map quality to Manim flags and folder names
    quality_map = {
        "l": "-pql", 
        "m": "-pqm", 
        "h": "-pqh", 
        "k": "-pqk"
    }
    
    # Run Manim Render
    print(f"🎥 Rendering {args.scene} from {args.file}...")
    manim_cmd = ["uv", "run", "manim", quality_map[args.quality], args.file, args.scene]
    
    if args.preview:
        # We handle preview manually after audio mix, so don't pass -p to manim?
        # Manim's -p will open the silent version. Let's let Manim do its thing?
        # Actually, user wants to see the FINAL version.
        pass

    subprocess.run(manim_cmd, check=True)

    # Find the output video
    # Manim quality folder names: 480p15, 720p30, 1080p60, 2160p60
    # This is a simplification; framerate depends on config.
    # We will search for the file.
    
    input_video = find_latest_video(args.scene)
    
    if not input_video:
        print(f"❌ Error: Could not find rendered video for {args.scene}")
        return

    print(f"Found input video: {input_video}")

    # Check Audio
    if not os.path.exists(args.audio):
        print(f"⚠️ Warning: Audio file not found at {args.audio}. Skipping audio processing.")
        if args.preview:
             if sys.platform == "darwin": subprocess.run(["open", input_video])
        return

    # Get Duration
    duration = get_video_duration(input_video)
    if duration is None:
        print("❌ Error: Could not determine video duration.")
        return
    
    print(f"⏱️ Video Duration: {duration} seconds")

    # Output filename
    video_dir = os.path.dirname(input_video)
    base_name = os.path.splitext(os.path.basename(input_video))[0]
    output_video = os.path.join(video_dir, f"{base_name}_Audio.mp4")

    # Fade out settings
    fade_duration = 2
    fade_start = max(0, duration - fade_duration)
    
    print("🎵 Adding audio with fade out...")
    
    ffmpeg_cmd = [
        "ffmpeg", "-y", "-v", "error",
        "-i", input_video,
        "-i", args.audio,
        "-map", "0:v",
        "-map", "1:a",
        "-c:v", "copy",
        "-af", f"afade=t=out:st={fade_start}:d={fade_duration}",
        "-shortest",
        output_video
    ]
    
    subprocess.run(ffmpeg_cmd, check=True)
    
    print(f"✅ Success! Output saved to: {output_video}")
    
    # Open the file if preview requested
    if args.preview:
        if sys.platform == "darwin":
            subprocess.run(["open", output_video])

if __name__ == "__main__":
    main()
