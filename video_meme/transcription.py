import os
from tqdm import tqdm
from faster_whisper import WhisperModel
from moviepy import AudioFileClip



def transcribe_audio(audio_path, model_size="base", device="auto"):
    """
    Transcribes audio using the faster-whisper model.
    """
    if not os.path.exists(audio_path):
        raise FileNotFoundError(f"Audio file not found: {audio_path}")

    model = WhisperModel(model_size, device=device, compute_type="int8")
    segments, _ti = model.transcribe(
        audio_path, beam_size=5, word_timestamps=True, language="en"
    )
    audio_clip = AudioFileClip(audio_path)
    total_duration = audio_clip.duration
    progress_bar = tqdm(total=total_duration, desc="Transcribing audio")
    min = 0
    transcription = {"segments": []}
    for segment in segments:
        transcription["segments"].append(
            {
                "start": segment.start,
                "end": segment.end,
                "text": segment.text,
                "words": [
                    {"word": word.word, "start": word.start, "end": word.end}
                    for word in segment.words
                ],
            }
        )
        progress_bar.update(segment.end - min)
        min = segment.end
    progress_bar.close()
    return transcription

def advanced_phrase_match(words, target_phrases):
    """
    Given a list of words and a list of target phrases, returns the start and end timestamps along with the matched phrase.
    This should match if the word is in target words but also if the word + word+1 is in the target list of words.
    All matches are lower case and stripped of punctuation or spaces.
    """
    results = []

    for i, word in enumerate(words):
        word_text: str = word["word"].lower().strip(".,!?-").replace("-", "").strip()
        if word_text in target_phrases:
            results.append((word["start"], word["end"], word_text))
        if i < len(words) - 1:
            next_word_text = (
                words[i + 1]["word"].lower().strip(".,!?-").replace("-", "").strip()
            )
            combined_text = f"{word_text}{next_word_text}"
            if combined_text in target_phrases:
                results.append((word["start"], words[i + 1]["end"], combined_text))
    return results
