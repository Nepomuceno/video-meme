import os
import hashlib
import argparse
from collections import defaultdict

from .transcription import advanced_phrase_match, transcribe_audio
from .video_manipulation import save_combined_clip, sample_video, extract_audio
from .file_manipulation import save_transcription, save_full_text, save_statistics, setup_output_dir


def compute_video_hash(video_path):
    """
    Computes a SHA256 hash of the video file to uniquely identify it.
    """
    sha256_hash = hashlib.sha256()
    with open(video_path, "rb") as f:
        for byte_block in iter(lambda: f.read(4096), b""):
            sha256_hash.update(byte_block)
    return sha256_hash.hexdigest()

def analyze_transcription(transcription, target_phrases):
    """
    Analyzes the transcription for exact matches of target phrases and collects statistics.
    Includes longest and shortest durations between occurrences.
    """
    stats = defaultdict(
        lambda: {
            "count": 0,
            "timestamps": [],
            "longest_gap": 0,
            "shortest_presence": float("inf"),
        }
    )
    video_segments = []
    all_occurrences = []

    for segment in transcription["segments"]:
        matches = advanced_phrase_match(segment["words"], target_phrases)
        for start, end, phrase_found in matches:
            phrase = phrase_found
            stats[phrase]["count"] += 1
            stats[phrase]["timestamps"].append((start, end))
            video_segments.append((max(start - 0.2, 0), end + 0.2))
            all_occurrences.append((start, end, phrase))

    # Sort timestamps to analyze gaps
    for phrase, data in stats.items():
        timestamps = sorted(data["timestamps"])
        for i in range(1, len(timestamps)):
            gap = timestamps[i][0] - timestamps[i - 1][1]
            data["longest_gap"] = max(data["longest_gap"], gap)
        for start, end in timestamps:
            duration = end - start
            data["shortest_presence"] = min(data["shortest_presence"], duration)

    # Calculate collective statistics for all words
    all_occurrences.sort()
    global_longest_gap = 0
    global_shortest_presence = float("inf")

    for i in range(1, len(all_occurrences)):
        gap = all_occurrences[i][0] - all_occurrences[i - 1][1]
        global_longest_gap = max(global_longest_gap, gap)

    for start, end, _ in all_occurrences:
        duration = end - start
        global_shortest_presence = min(global_shortest_presence, duration)

    stats["__overall__"] = {
        "longest_gap": global_longest_gap,
        "shortest_presence": global_shortest_presence,
    }

    return stats, video_segments

def main(args):
    video_path = args.video_path
    words = args.words
    model_size = args.model_size
    device = args.device
    sample = args.sample
    video_hash = compute_video_hash(video_path)
    output_dir = setup_output_dir(video_hash)

    if sample:
        start, end, video_path = sample_video(video_path, output_dir)
        print(f"Sample range: {start}s to {end}s")

    audio_path = os.path.join(output_dir, "audio.wav")
    print("Extracting audio...")
    extract_audio(video_path, audio_path)

    print("Transcribing audio...")
    transcription = transcribe_audio(audio_path, model_size=model_size, device=device)
    save_transcription(
        output_dir, transcription
    )  # Save the transcription only if it was created

    print("Saving transcription and full text...")
    save_transcription(output_dir, transcription)
    save_full_text(output_dir, transcription)

    print("Analyzing transcription for target words...")
    stats, video_segments = analyze_transcription(transcription, words)
    save_statistics(output_dir, stats)

    if video_segments:
        print("Saving clips...")
        save_combined_clip(video_path, output_dir, video_segments)
    else:
        print("No clips to save for the given words.")

    print(f"All files saved to: {output_dir}")





def parse_arguments():
    parser = argparse.ArgumentParser(
        description="Analyze video for specific words and save results."
    )
    parser.add_argument("--video_path", required=True, help="Path to the video file.")
    parser.add_argument(
        "--words", nargs="+", required=True, help="List of words or phrases to analyze."
    )
    parser.add_argument(
        "--model_size",
        default="distil-small.en",
        help="Whisper model size (default: distil-small.en).",
    )
    parser.add_argument(
        "--device", default="auto", help="Device for inference (e.g., 'cpu', 'cuda')."
    )
    parser.add_argument(
        "--sample",
        action="store_true",
        help="Use a 5-minute random sample for testing.",
    )
    # Show help if no arguments are provided

    return parser.parse_args()


def entrypoint():
    args = parse_arguments()
    main(args)


if __name__ == "__main__":
    args = parse_arguments()
    main(args)
