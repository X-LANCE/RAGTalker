import os
import subprocess
from pathlib import Path

def convert_for_web_playback(input_dir='.'):
    """
    Convert all video files in the specified directory to web-compatible format.
    Ensures videos can be played online in all major browsers.
    
    Args:
        input_dir (str): Directory containing video files to convert
    """
    # Common video extensions
    video_extensions = ['.mp4', '.avi', '.mov', '.mkv', '.webm', '.flv']
    
    # Get all files in the directory
    files = [f for f in Path(input_dir).glob('**/*') if f.is_file() and f.suffix.lower() in video_extensions]
    
    for file_path in files:
        input_file = str(file_path)
        output_file = f"{os.path.splitext(input_file)[0]}_web{os.path.splitext(input_file)[1]}"
        
        # Skip if already converted
        if os.path.exists(output_file):
            print(f"Skipping {input_file} (already converted)")
            continue
        
        print(f"Converting {input_file} for web playback...")
        
        # FFmpeg command optimized for web compatibility across browsers
        cmd = [
            'ffmpeg',
            '-i', input_file,
            '-c:v', 'libx264',  # H.264 codec for wide compatibility
            '-profile:v', 'baseline',  # Most compatible H.264 profile
            '-level', '3.0',
            '-pix_fmt', 'yuv420p',  # Required for browser compatibility
            '-preset', 'medium',  # Balance between speed and quality
            '-crf', '23',  # Constant Rate Factor (quality)
            '-c:a', 'aac',  # AAC audio codec for browser compatibility
            '-ar', '44100',  # Standard audio sample rate
            '-b:a', '128k',  # Audio bitrate
            '-movflags', '+faststart',  # Optimize for web playback
            '-y',  # Overwrite output file if it exists
            output_file
        ]
        
        try:
            subprocess.run(cmd, check=True)
            print(f"Successfully converted {input_file} to web-compatible format: {output_file}")
        except subprocess.CalledProcessError as e:
            print(f"Error converting {input_file}: {e}")

if __name__ == "__main__":
    convert_for_web_playback()
