# 🎥 Video-Meme

A tool for turning videos into delightful memes, and fun clips.  
Analyze your videos, extract meaningful (or funny!) content, and create shareable clips with just a few commands.

With **Video-Meme**, your videos become your playground. It transcribes audio, searches for keywords, and creates video snippets seamlessly. Add a touch of fun or a sprinkle of productivity—your choice!

## 🎯 Features

- **📋 Transcription**: High-quality transcription of your video’s audio using **faster-whisper**.
- **🔍 Keyword Analysis**: Identify specific keywords or phrases with advanced matching (even for tricky cases like "co-pilot").
- **✂️ Clip Extraction**: Automatically extract video segments where keywords are mentioned.
- **📹 Combined Clips**: Merge all keyword-related segments into a single video with customizable transitions.
- **📊 Statistics**: Generate stats for keywords, including:
  - Longest gap between mentions.
  - Shortest duration of mentions.
  - Global stats across all keywords.
- **🎬 Sampling**: Work on a smaller sample of the video for quick testing.
- **⚡ Efficiency**: Uses GPU acceleration for fast transcription and processing.

---

## 🎉 Getting Started

### Installation

```bash
git clone https://github.com/Nepomuceno/video-meme.git
cd video-meme
pip install -e .
```

Ensure you have FFmpeg installed. [Download FFmpeg](https://ffmpeg.org/download.html) for your platform if it's not already available.

---

## 🚀 Usage

### Command-Line Interface

```bash
video-meme --video_path example.mp4 --words ai copilot --model_size base --sample
```

#### Arguments

- `--video_path`: Path to your video file.
- `--words`: Keywords or phrases to analyze (e.g., `"ai copilot"`).
- `--model_size`: Model size for transcription (`base`, `small`, `large`, etc.).
- `--device`: Compute device for faster transcription (e.g., `cuda`, `cpu`, `mps`).
- `--sample`: Extract a 5-minute sample from the video for testing.

---

## 🖼️ Examples

### Create a Fun Clip from Keywords

```bash
video-meme --video_path myvideo.mp4 --words "cat" "dog" --model_size large
```

Output:  
- A combined video of all segments mentioning "cat" and "dog".  
- Transcription and statistics in the output directory.

---

### What You’ll Get

1. **🎞️ Clips**: Video clips where keywords are mentioned, merged with 0.1-second black frames in between.
2. **📜 Transcription**: A complete transcription of the video in JSON and plain text formats.
3. **📊 Statistics**: Insights into how often keywords appear, their durations, and gaps.

---

## 🛠️ Development

### Clone the Repository

We do recomend the use of uv to manage dependiencies: [https://docs.astral.sh/uv/]

```bash
git clone https://github.com/Nepomuceno/video-meme.git
cd video-meme
pip install -e .
```

### Run Locally

```bash
python -m video_meme.cli --video_path myvideo.mp4 --words "machinelearning" --model_size base
```

---

## 📋 Roadmap

- Add speaker diarization support.

---

## 🛡️ Known Limitations

- **Large Videos**: Processing may be slow for very large videos on lower-end hardware.
- **Accent Sensitivity**: Transcription accuracy may vary for strong accents or noisy audio.

---

## 🌟 Fun Ideas

- **Highlight Reels**: Extract key moments from educational or gaming videos.
- **Memes**: Find and clip out funny phrases to share on social media.
- **Analytics**: Add more interesting stats about the words

---

## 📝 Documentation & Links

- [GitHub Repository](https://github.com/Nepomuceno/video-meme)

---

## 📚 Sources & Inspiration

- **faster-whisper**: High-performance Whisper implementation.
- **MoviePy**: Video editing made easy.
- **FFmpeg**: The workhorse of multimedia processing.

🎉 Happy Memeing!