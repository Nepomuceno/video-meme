import os
import subprocess
import hashlib
import json
import argparse
import random
import datetime

def setup_output_dir(video_hash):
    """
    Sets up the output directory using the video hash and current timestamp.
    """
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    output_dir = os.path.join("outputs", f"{video_hash}_{timestamp}")
    os.makedirs(output_dir, exist_ok=True)
    return output_dir

def save_transcription(output_dir, transcription):
    """
    Saves the transcription to a JSON file.
    """
    transcript_path = os.path.join(output_dir, "transcription.json")
    with open(transcript_path, "w") as f:
        json.dump(transcription, f, indent=4)
    return transcript_path

def save_full_text(output_dir, transcription):
    """
    Saves the full text of the transcription to a plain text file.
    """
    text_path = os.path.join(output_dir, "transcription.txt")
    full_text_s = "\n".join([segment["text"] for segment in transcription["segments"]])
    with open(text_path, "w") as f:
        f.write(full_text_s)
    return text_path

def save_statistics(output_dir, stats):
    """
    Saves word statistics to a JSON file.
    """
    stats_path = os.path.join(output_dir, "statistics.json")
    with open(stats_path, "w") as f:
        json.dump(stats, f, indent=4)
    return stats_path
