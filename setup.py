from setuptools import setup, find_packages

setup(
    name="video-meme",
    version="1.0.0",
    description="A tool for analyzing videos, extracting clips, and transcribing audio with some word analysis.",
    author="Your Name",
    author_email="your.email@example.com",
    url="https://github.com/Nepomuceno/video-meme",
    packages=find_packages(),
    install_requires=[
        "moviepy",
        "faster-whisper",
        "tqdm",
        "transformers",
    ],
    entry_points={
        "console_scripts": [
            "video-meme=video_meme.main:entrypoint",
        ],
    },
    python_requires=">=3.12",
)
