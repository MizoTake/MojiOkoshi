import os
import speech_recognition as sr

# 入力および出力ディレクトリが存在しない場合に作成する関数
def create_directories(input_dir, output_dir):
    os.makedirs(input_dir, exist_ok=True)
    os.makedirs(output_dir, exist_ok=True)

# 音声ファイルをテキストに変換する関数
def transcribe_audio(file_path):
    recognizer = sr.Recognizer()
    try:
        with sr.AudioFile(file_path) as source:
            audio = recognizer.record(source)
            text = recognizer.recognize_google(audio, language='ja-JP')
            return text
    except Exception as e:
        print(f"Error transcribing {file_path}: {e}")
        return None

# テキストを指定されたパスに保存する関数
def save_transcription(output_path, text):
    # スペースを改行に置き換える
    formatted_text = text.replace(' ', '\n')
    
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(formatted_text)
    print(f"Saved transcription to {output_path}")

# 入力ディレクトリ内のすべてのWAVファイルをテキストに変換し、出力ディレクトリに保存する関数
def transcribe_all_wav_files(input_dir, output_dir):
    for file_name in os.listdir(input_dir):
        if file_name.lower().endswith(".wav"):
            input_file_path = os.path.join(input_dir, file_name)
            output_file_name = os.path.splitext(file_name)[0] + ".txt"
            output_file_path = os.path.join(output_dir, output_file_name)

            print(f"transcribing {input_file_path}...")
            text = transcribe_audio(input_file_path)

            if text:
                save_transcription(output_file_path, text)
            else:
                print(f"Failed to transcribe {input_file_path}")

if __name__ == "__main__":
    INPUT_DIR = "input"
    OUTPUT_DIR = "output"

    create_directories(INPUT_DIR, OUTPUT_DIR)
    transcribe_all_wav_files(INPUT_DIR, OUTPUT_DIR)
