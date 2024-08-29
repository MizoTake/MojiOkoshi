import speech_recognition as sr
from pydub import AudioSegment
import os
import ffmpeg


def convert_to_wav(file_path, output_path):
    """Convert audio files to WAV format using ffmpeg."""
    output_file = os.path.join(output_path, os.path.basename(file_path).rsplit('.', 1)[0] + '.wav')
    if not os.path.exists(output_file):
        ffmpeg.input(file_path).output(output_file).run(quiet=True)
    return output_file


def transcribe_audio(audio_file):
    recognizer = sr.Recognizer()
    with sr.AudioFile(audio_file) as source:
        audio = recognizer.record(source)
    try:
        return recognizer.recognize_google(audio, language='ja-JP')
    except sr.UnknownValueError:
        return ""
    except sr.RequestError as e:
        print(f"Could not request results; {e}")
        return ""


def split_text_to_paragraphs(text, max_length=20):
    sentences = text.split(' ')
    paragraphs = []
    current_paragraph = ""

    for sentence in sentences:
        if len(current_paragraph) + len(sentence) + 1 <= max_length:
            current_paragraph += sentence + '. '
        else:
            paragraphs.append(current_paragraph.strip())
            current_paragraph = sentence + '. '

    if current_paragraph:
        paragraphs.append(current_paragraph.strip())

    return paragraphs


def add_timestamps_to_paragraphs(paragraphs, duration):
    paragraph_timestamps = []
    interval = duration / len(paragraphs)
    current_time = 0.0

    for paragraph in paragraphs:
        timestamp = f"[{int(current_time // 60):02}:{int(current_time % 60):02}]"
        paragraph_timestamps.append(f"{timestamp} {paragraph}")
        current_time += interval

    return paragraph_timestamps


def transcribe_and_format(input_folder, output_folder):
    for file_name in os.listdir(input_folder):
        if file_name.endswith('.wav') or file_name.endswith('.mp4'):
            input_path = os.path.join(input_folder, file_name)
            output_path = output_folder

            # Convert to WAV if needed
            if file_name.endswith('.mp4'):
                input_path = convert_to_wav(input_path, output_folder)

            # Transcribe the audio
            transcription = transcribe_audio(input_path)

            # Split transcription into paragraphs
            paragraphs = split_text_to_paragraphs(transcription)

            # Get audio duration
            audio = AudioSegment.from_wav(input_path)
            duration = len(audio) / 1000  # in seconds

            # Add timestamps to paragraphs
            paragraphs_with_timestamps = add_timestamps_to_paragraphs(paragraphs, duration)

            # Save to file
            output_file = os.path.join(output_folder, file_name.rsplit('.', 1)[0] + '.txt')
            with open(output_file, "w", encoding="utf-8") as f:
                for paragraph in paragraphs_with_timestamps:
                    f.write(paragraph + '\n\n')

            print(f"Transcription saved to {output_file}")


# Example usage:
input_folder = 'input'  # Folder containing the input audio files
output_folder = 'output'  # Folder where the transcriptions will be saved

if not os.path.exists(output_folder):
    os.makedirs(output_folder)

transcribe_and_format(input_folder, output_folder)
