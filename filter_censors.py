import os
import subprocess
import whisper
from pydub import AudioSegment
import argparse

# ADD YOUR LIST OF BAD WORDS HERE
BAD_WORDS = [
    "fuck",
    "shit",
    "bitch",
    "cunt",
    "dick",
]

def load_whisper_model():
    """Load the Whisper model."""
    return whisper.load_model("base")

def transcribe_audio(model, input_video):
    """Transcribe the audio from the video using Whisper with word-level timestamps."""
    return model.transcribe(input_video, word_timestamps=True)

def censor_audio_segments(audio, censor_sound, segments):
    """Censor specific words in the audio based on the segments provided by Whisper."""
    for segment in segments:
        for word_info in segment["words"]:
            word = word_info["word"].strip().lower()
            word_start = word_info["start"] * 1000
            word_end = word_info["end"] * 1000    

            if word in BAD_WORDS:
                print(f"Censoring '{word}' from {word_start / 1000 } to {word_end / 1000} s")
                # Replace the word's audio with the censor sound
                duration = word_end - word_start
                censor_segment = censor_sound[:duration]
                audio = audio[:word_start] + censor_segment + audio[word_end:]
    return audio

def save_censored_audio(audio, output_audio):
    """Export the censored audio to a file."""
    audio.export(output_audio, format="wav")

def replace_audio_in_video(input_video, output_audio, output_video):
    """Replace the original audio in the video with the censored audio using ffmpeg."""
    subprocess.run([
        "ffmpeg",
        "-i", input_video,
        "-i", output_audio,
        "-c:v", "copy",
        "-map", "0:v:0",
        "-map", "1:a:0",
        "-shortest", output_video
    ], check=True)

def get_output_video_name(input_video):
    """Generate the output video file name by appending '_edited' to the input file name."""
    base, ext = os.path.splitext(input_video)
    return f"{base}_edited{ext}"

def remove_tmp_files(files):
    """Removes all files in the list provided."""
    for file in files:
        os.remove(file)

def main(input_video):
    # Load Whisper model
    model = load_whisper_model()

    # Transcribe the audio with word-level timestamps
    result = transcribe_audio(model, input_video)

    # Load the original audio and censor sound
    audio = AudioSegment.from_file(input_video)
    censor_sound = AudioSegment.from_wav("./beep.wav")

    # Censor specific words in the audio
    censored_audio = censor_audio_segments(audio, censor_sound, result["segments"])

    # Save the censored audio to a temporary file
    tmp_audio_file = "./tmp_audio_file.wav"
    save_censored_audio(censored_audio, tmp_audio_file)

    # Generate output video file name
    output_video = get_output_video_name(input_video)

    # Replace the audio in the video with the censored audio
    replace_audio_in_video(input_video, tmp_audio_file, output_video)

    # Remove any tmp files
    files = [tmp_audio_file]
    remove_tmp_files(files)

    print(f"Finished processing. The edited video is saved as {output_video}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Censor bad words in a video file.")
    parser.add_argument("input_video", help="Path to the input video file.")

    args = parser.parse_args()
    main(args.input_video)
