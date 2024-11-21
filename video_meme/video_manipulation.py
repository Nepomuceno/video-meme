import os
import subprocess
import random
from tqdm import tqdm
from moviepy import VideoFileClip
from moviepy.video.io.VideoFileClip import VideoFileClip
from moviepy.video.io.ffmpeg_tools import ffmpeg_extract_subclip
from moviepy.video.compositing.CompositeVideoClip import concatenate_videoclips
from moviepy.video.VideoClip import ColorClip


def sample_video(video_path, output_dir, sample_length=300):
    """
    Extracts a random sample of specified length (default 5 minutes).
    """
    with VideoFileClip(video_path) as video:
        duration = int(video.duration)
        if sample_length >= duration:
            print("Sample length exceeds video duration; using full video.")
            return 0, duration, video_path

        start = random.randint(0, duration - sample_length)
        end = start + sample_length
        sample_path = os.path.join(output_dir, "sample_video.mp4")
        ffmpeg_extract_subclip(video_path, start, end, targetname=sample_path)
        print(f"Sample video created from {start}s to {end}s.")
        return start, end, sample_path

   
def save_combined_clip(video_path, output_dir, video_segments):
    """
    Saves a single combined video clip for all segments containing the target words,
    adding a 0.1-second blank frame between each segment.
    """
    clip_dir = os.path.join(output_dir, "clips")
    os.makedirs(clip_dir, exist_ok=True)

    clips = []
    for start, end in tqdm(video_segments, desc="Extracting clips"):
        clip = VideoFileClip(video_path).with_subclip(start, end)
        clips.append(clip)

        # Add a 0.1-second blank (black) clip
        blank_clip = ColorClip(size=clip.size, color=(0, 0, 0), duration=0.01)
        clips.append(blank_clip)

    if clips:
        combined_clip = concatenate_videoclips(clips, method="compose")
        output_clip_path = os.path.join(clip_dir, "combined_mentions.mp4")
        combined_clip.write_videofile(
            output_clip_path, codec="libx264", audio_codec="aac"
        )
        print(f"Combined clip saved at: {output_clip_path}")
        return output_clip_path
    else:
        print("No clips were combined.")
        return None
    
    
def extract_audio(video_path, audio_path):
    """
    Extracts audio from a video file using ffmpeg.
    """
    command = ["ffmpeg", "-y", "-i", video_path, "-ac", "1", "-ar", "16000", audio_path]
    result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if result.returncode != 0:
        print("Error extracting audio with ffmpeg:")
        print(result.stderr.decode())
        raise Exception("ffmpeg failed to extract audio")


def save_clips(video_path, output_dir, video_segments):
    """
    Saves video clips for each segment containing the target words.
    """
    clip_dir = os.path.join(output_dir, "clips")
    os.makedirs(clip_dir, exist_ok=True)

    clips = []
    for idx, (start, end) in enumerate(tqdm(video_segments, desc="Extracting clips")):
        clip_path = os.path.join(clip_dir, f"clip_{idx}.mp4")
        ffmpeg_extract_subclip(video_path, start, end, targetname=clip_path)
        clips.append(clip_path)

    return clips


def save_individual_word_clips(video_path, output_dir, phrase_occurrences):
    """
    Saves combined clips for each target word, containing all its occurrences.
    """
    for phrase, segments in phrase_occurrences.items():
        if segments:
            sanitized_phrase = "".join(c if c.isalnum() else "_" for c in phrase)
            output_filename = f"{sanitized_phrase}_mentions.mp4"
            print(f"Creating clip for word/phrase: {phrase}")
            save_combined_clip(video_path, output_dir, segments, output_filename)