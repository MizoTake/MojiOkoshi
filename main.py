import speech_recognition as sr
from pydub import AudioSegment
import os
import ffmpeg


def convert_to_wav(file_path, output_path):
    """音声ファイルをWAV形式に変換します。"""
    output_file = os.path.join(output_path, os.path.basename(file_path).rsplit('.', 1)[0] + '.wav')
    if not os.path.exists(output_file):
        ffmpeg.input(file_path).output(output_file).run(quiet=True)
    return output_file


def transcribe_audio_segment(audio_segment, recognizer):
    """音声のセグメントを文字起こしします。"""
    audio_data = sr.AudioData(audio_segment.raw_data, audio_segment.frame_rate, audio_segment.sample_width)
    try:
        return recognizer.recognize_google(audio_data, language='ja-JP')  # 日本語で文字起こし
    except sr.UnknownValueError:
        return ""
    except sr.RequestError as e:
        print(f"Could not request results; {e}")
        return ""


def split_audio_to_paragraphs(audio, max_length=30):
    recognizer = sr.Recognizer()
    step = 5000  # 5秒ずつ処理
    start = 0
    duration = len(audio)
    paragraphs = []
    current_paragraph = ""
    paragraph_start_time = 0

    while start < duration:
        end = min(start + step, duration)
        audio_segment = audio[start:end]
        transcription = transcribe_audio_segment(audio_segment, recognizer)

        if transcription:
            sentences = transcription.split('。')  # 日本語では「。」で文を区切る
            for sentence in sentences:
                if len(current_paragraph) + len(sentence) + 1 <= max_length:
                    current_paragraph += sentence + '。'
                else:
                    paragraphs.append((paragraph_start_time, current_paragraph.strip()))
                    current_paragraph = sentence + '。'
                    paragraph_start_time = start / 1000  # 秒に変換

        start += step

    if current_paragraph:
        paragraphs.append((paragraph_start_time, current_paragraph.strip()))

    return paragraphs


def format_paragraphs_with_timestamps(paragraphs):
    formatted_paragraphs = []
    for start_time, paragraph in paragraphs:
        timestamp = f"[{int(start_time // 60):02}:{int(start_time % 60):02}]"
        formatted_paragraphs.append(f"{timestamp} {paragraph}")
    return formatted_paragraphs


def transcribe_and_format(input_folder, output_folder):
    for file_name in os.listdir(input_folder):
        if file_name.endswith('.wav') or file_name.endswith('.mp3'):
            input_path = os.path.join(input_folder, file_name)
            output_path = output_folder

            # Convert to WAV if needed
            if file_name.endswith('.mp3'):
                input_path = convert_to_wav(input_path, output_folder)

            # Load the audio file
            audio = AudioSegment.from_wav(input_path)

            # Split and transcribe the audio into paragraphs
            paragraphs = split_audio_to_paragraphs(audio)

            # Format paragraphs with timestamps
            paragraphs_with_timestamps = format_paragraphs_with_timestamps(paragraphs)

            # Save to file
            output_file = os.path.join(output_folder, file_name.rsplit('.', 1)[0] + '.txt')
            with open(output_file, 'w', encoding='utf-8') as f:  # UTF-8で保存
                for paragraph in paragraphs_with_timestamps:
                    f.write(paragraph + '\n\n')

            print(f"Transcription saved to {output_file}")


input_folder = 'input'  # 入力音声ファイルが保存されているフォルダ
output_folder = 'output'  # 文字起こし結果が保存されるフォルダ

if not os.path.exists(output_folder):
    os.makedirs(output_folder)

transcribe_and_format(input_folder, output_folder)
