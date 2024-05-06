import os
import argparse
from pydub import AudioSegment
from pydub.generators import WhiteNoise
import random

# Setup argument parser
parser = argparse.ArgumentParser(description="Extract and normalize audio files.")
parser.add_argument('source_folder', type=str, help='Path to the source folder containing audio files')
parser.add_argument('destination_folder', type=str, help='Path to the destination folder where normalized audio files will be saved')
parser.add_argument('num_files', type=int, help='Number of audio files to process')
parser.add_argument('target_length', type=int, help='Target length for audio normalization in seconds')
parser.add_argument('--filename', type=str, default="audio", help='Base filename for processed files (default: "audio")')
parser.add_argument('--input_extension', type=str, default="mp3", help='File extension of the input files (default: "mp3")')
parser.add_argument('--output_extension', type=str, default="mp3", help='File extension for output files (default: "mp3")')

# Parse arguments
args = parser.parse_args()

source_folder = args.source_folder
destination_folder = args.destination_folder
num_files = args.num_files
target_length = args.target_length * 1000  # Convert seconds to milliseconds for pydub
base_filename = args.filename
input_extension = args.input_extension
output_extension = args.output_extension

# Create destination directory if it doesn't exist
os.makedirs(destination_folder, exist_ok=True)

def add_comfort_noise(audio_segment, duration_ms, volume=-20.0):
    """
    Adds comfort noise to an audio segment for a given duration and volume.
    """
    # Generate white noise
    noise = WhiteNoise().to_audio_segment(duration=duration_ms, volume=volume)
    return audio_segment.overlay(noise, position=0)

def normalize_audio(audio_path, output_path, target_length=30000):
    audio = AudioSegment.from_file(audio_path)
    original_bitrate = audio.frame_rate * audio.frame_width * 8 * audio.channels // 1000  # Simplistic bitrate calculation in kbps

    duration = len(audio)
    if duration < target_length:
        # Calculate the required duration of comfort noise
        silence_duration = target_length - duration
        # Generate and add comfort noise
        noise = add_comfort_noise(AudioSegment.silent(duration=silence_duration), silence_duration, volume=-20)
        audio += noise
    elif duration > target_length:
        # Cut down to target length if longer
        audio = audio[:target_length]

    # Export with the original bitrate and parameters
    audio.export(output_path, format=output_extension, bitrate=f"{original_bitrate}k")

# Gather all files with the specified input extension
all_files = []
for root, dirs, files in os.walk(source_folder):
    for file in files:
        if file.endswith('.' + input_extension):
            all_files.append(os.path.join(root, file))

# Randomize selection
random.shuffle(all_files)

# Process files up to the specified number
for i, file_path in enumerate(all_files[:num_files]):
    new_file_name = f"{base_filename}_{i+1}.{output_extension}"
    new_file_path = os.path.join(destination_folder, new_file_name)
    normalize_audio(file_path, new_file_path, target_length)

print(f"Processing complete. {num_files} files have been normalized and copied.")
