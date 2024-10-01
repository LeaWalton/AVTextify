import whisper
import ffmpeg
import csv
import sys
import os
import time
import tkinter as tk
from tkinter import filedialog

def select_Files():
    tk.Tk().withdraw()

    selectedFilePaths = filedialog.askopenfilenames(
        title = "Select MP4 video files",
        filetypes = [("MP4 Files", "*.mp4")],
    )

    return selectedFilePaths;

def processFiles(fileList):
    for videoFile in fileList:
        print(f"Processing {videoFile}")
        audio_file = os.path.splitext(videoFile)[0] + ".wav"
        extract_audio(videoFile,audio_file)

        csvOutput = os.path.splitext(videoFile)[0] + ".csv"
        transcribe_audio(audio_file,csvOutput)
        os.remove(audio_file)

def extract_audio(mp4_file, output_audio):
    start_time = time.time()
    print(f"Extracting audio from {mp4_file}...")

    # Extract audio from video using ffmpeg, and overwrite the output file if it exists
    try:
        ffmpeg.input(mp4_file).output(output_audio).overwrite_output().run()
    except Exception as e:
        print(f"Error during audio extraction: {e}")
        sys.exit(1)

    end_time = time.time()
    print(f"Audio extracted to {output_audio}. Time taken: {end_time - start_time:.2f} seconds.")

def transcribe_audio(audio_file, output_csv):
    start_time = time.time()
    print(f"Starting transcription of {audio_file}...")

    # Load Whisper model
    try:
        model = whisper.load_model("base")
        print("Whisper model loaded successfully.")
    except Exception as e:
        print(f"Error loading Whisper model: {e}")
        sys.exit(1)

    # Transcribe audio
    try:
        result = model.transcribe(audio_file, verbose=True)
        print("Transcription complete.")
    except Exception as e:
        print(f"Error during transcription: {e}")
        sys.exit(1)

    # Prepare CSV output
    try:
        segments = result['segments']
    
        # Open the output CSV file
        with open(output_csv, mode='w', newline='', encoding='utf-8') as csv_file:
            csv_writer = csv.writer(csv_file)
        
            # Write the header row
            csv_writer.writerow(['start', 'end', 'text'])
        
            # Write each segment's data as a row
            for segment in segments:
                csv_writer.writerow([segment['start'], segment['end'], segment['text']])
    
        print(f"CSV saved to {output_csv}")
    except Exception as e:
        print(f"Error saving CSV: {e}")
        sys.exit(1)

    end_time = time.time()
    print(f"Transcription completed. Time taken: {end_time - start_time:.2f} seconds.")

if __name__ == "__main__":

    print("Select files to transcribe...")
    mp4_files = select_Files()
    
    processFiles(mp4_files)

