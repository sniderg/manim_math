import subprocess
import os
import sys
import shutil

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
        return float(result.stdout.strip())
    except ValueError:
        return None

def main():
    # 1. Run Manim Render
    print("🎥 Rendering animation...")
    manim_cmd = ["uv", "run", "manim", "-pql", "holt_winters.py", "HoltWintersExplained"]
    subprocess.run(manim_cmd, check=True)

    # Defined paths
    # Note: These paths are specific to the current project structure/defaults
    video_dir = "media/videos/holt_winters/480p15"
    video_name = "HoltWintersExplained.mp4"
    input_video = os.path.join(video_dir, video_name)
    audio_file = "assets/ambient.mp3"
    output_video = os.path.join(video_dir, "HoltWintersExplained_Audio.mp4")

    if not os.path.exists(input_video):
        print(f"❌ Error: Input video not found at {input_video}")
        return

    if not os.path.exists(audio_file):
        print(f"⚠️ Warning: Audio file not found at {audio_file}. Skipping audio processing.")
        return

    # 2. Get Duration
    duration = get_video_duration(input_video)
    if duration is None:
        print("❌ Error: Could not determine video duration.")
        return
    
    print(f"⏱️ Video Duration: {duration} seconds")

    # 3. Add Audio with Fade Out
    # Fade out starts 2 seconds before end
    fade_duration = 2
    fade_start = max(0, duration - fade_duration)
    
    print("🎵 Adding audio with fade out...")
    
    # ffmpeg command:
    # -i input_video -i audio_file
    # -map 0:v -map 1:a
    # -c:v copy (copy video stream without re-encoding)
    # -af "afade=t=out:st={fade_start}:d={fade_duration}" (audio filter)
    # -shortest (cut audio to video length)
    
    ffmpeg_cmd = [
        "ffmpeg", "-y",
        "-i", input_video,
        "-i", audio_file,
        "-map", "0:v",
        "-map", "1:a",
        "-c:v", "copy",
        "-af", f"afade=t=out:st={fade_start}:d={fade_duration}",
        "-shortest",
        output_video
    ]
    
    subprocess.run(ffmpeg_cmd, check=True)
    
    print(f"✅ Success! Output saved to: {output_video}")
    
    # Open the file
    if sys.platform == "darwin":
        subprocess.run(["open", output_video])

if __name__ == "__main__":
    main()
