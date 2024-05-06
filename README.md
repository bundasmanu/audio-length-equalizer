# audio-length-equalizer

- [audio-length-equalizer](#audio-length-equalizer)
  - [Description](#description)
    - [How the length equalizer works?](#how-the-length-equalizer-works)
  - [Usage](#usage)
    - [Install required packages](#install-required-packages)
    - [Arguments](#arguments)
    - [Run the script](#run-the-script)

## Description

In order to facilitate the audio manipulation process, with the aim to control the size of the audio and standardize datasets, a script was created to deal with this: `audio-length-equalizer.py`.

It's a very simple script that has very specific objectives, including:

- Recreating audio with a specific length;
- Keeping the current characteristics of the audio, without changing its bitrate, for example;
- Recreating audio with a customizable and incremental filename;
- Possibility of recreating files with another extension, for example, original audio: `mp3` converted to `wav`;

### How the length equalizer works?

The process of normalizing the size of the final audios is simplistic, based on the following premises:

- If `audio_duration < wanted_audio_length` then:
  - Added silence, until `audio_duration=wanted_audio_length`
- Otherwise:
  - Excess part of the audio is deleted, so that `audio_duration=wanted_audio_length`

## Usage

Below are the main points to consider regarding the use of the script.

### Install required packages

To use the script you need to install the necessary dependencies, in this case just the lib: `pydub`.
All you need to do is run the following:

```python
pip install -r requirements.txt
```

### Arguments

```bash
<source_folder>: Directory containing the original audio files.
<destination_folder>: Directory where the processed files will be saved.
<number_of_files>: Number of audio files to process.
<target_length_seconds>: Desired duration of each audio file in seconds.
--filename <base_filename>: (Optional) Base name for output files, defaults to "audio".
--input_extension <input_ext>: (Optional) File extension of input files, defaults to "mp3".
--output_extension <output_ext>: (Optional) File extension for output files, defaults to "mp3".
```

### Run the script

```python
python audio-length-equalizer.py <ORIGINAL_AUDIOS_FOLDER> <TARGET_AUDIOS_FOLDER> 5 300 --filename my_audio --input_extension mp3 --output_extension wav
```

This will create 5 audios with 5 minutes each and incremental filenames, starting with `my_audio_1.wav` until `my_audio_5.wav`.
