# README (English)

## Introduction to Fast-Whisper

Fast-Whisper is a reimplementation of OpenAI's Whisper model using CTranslate2. CTranslate2 is a high-speed inference engine for transformer models, offering up to 4 times faster performance and reduced memory usage compared to the original Whisper model. By applying 8-bit quantization on both CPU and GPU, performance efficiency is further enhanced.

**This program utilizes the user's computer performance. If the specifications are low, consider using Whisper-WebUI or another transcription program.**

[Go to Fast-Whisper GitHub page](https://github.com/SYSTRAN/faster-whisper)

---

## Prerequisites

### 1. Python Installation

To use Fast-Whisper, Python 3.8 or higher is required. To check your Python version, run the following command in the terminal:

```bash
python --version
```

or

```bash
python3 --version
```

**Recommended Version:** Python 3.10 or higher

[Python Official Download Page](https://www.python.org/downloads/)

### 2. NVIDIA Library Installation (Required for GPU Use)

To improve speech recognition processing speed with GPU, you need to install NVIDIA cuBLAS and cuDNN libraries. If you don't have a GPU or installing these libraries is difficult, the program can also run using CPU-only mode, although with slower performance.

#### cuBLAS Installation Steps

1. Go to [cuBLAS for CUDA 11](https://developer.nvidia.com/cublas)
2. Click **Download Now**
3. Select the version suitable for your operating system and install it.
   - **Note:** Windows is not supported.

#### cuDNN Installation Steps

1. Go to [cuDNN 8 for CUDA 11](https://developer.nvidia.com/cudnn)
2. Check the **Download Library** list.
3. Select the library for your operating system and install it.

---

## Installation Guide

### 1. Install Library

Open the terminal and run the following command to install the `faster-whisper` library:

```bash
pip install faster-whisper
```

### 2. Prepare Working Directory

Navigate to your desired working directory, create the `transcribe_audio.py` file, and create a folder where the generated subtitles will be saved.

### 3. Create `transcribe_audio.py` File

Copy the code below to create the `transcribe_audio.py` file:

```python
from faster_whisper import WhisperModel
import sys
import os

def seconds_to_srt_time(seconds):
    """Convert time in seconds to SRT file format."""
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    seconds = seconds % 60
    milliseconds = int((seconds - int(seconds)) * 1000)
    return f"{hours:02}:{minutes:02}:{int(seconds):02},{milliseconds:03}"

def process_audio_to_srt(audio_file, model, srt_folder):
    """Process audio file and convert to SRT file format."""
    base_name = os.path.splitext(os.path.basename(audio_file))[0]  # Remove the file extension from the file name.
    srt_file_name = f"{srt_folder}/{base_name}.srt"

    # Transcribe audio file
    segments, info = model.transcribe(audio_file, beam_size=5, language="en")

    with open(srt_file_name, "w", encoding="utf-8") as file:
        i = 0  # Variable to track segment numbers
        for segment in segments:
            start_time = seconds_to_srt_time(segment.start)
            end_time = seconds_to_srt_time(segment.end)
            i += 1  # Increment segment number
            file.write(f"{i}\n")
            file.write(f"{start_time} --> {end_time}\n")
            file.write(f"{segment.text}\n\n")

            sys.stdout.write(f"\rProcessing segment {i}...")
            sys.stdout.flush()

    print(f"\n'{audio_file}' conversion complete! Saved to '{srt_file_name}'")

model_size = "large-v3"
# Run on GPU with FP16
model = WhisperModel(model_size, device="cuda", compute_type="float16")

audio_folder = "Video"  # Process audio files in the specified folder.
srt_folder = "SRT"  # Folder to save SRT files

# Create SRT folder if it doesn't exist
if not os.path.exists(srt_folder):
    os.makedirs(srt_folder)

# Process all MP3 files in the folder
for file in os.listdir(audio_folder):
    if file.endswith(".mp3"):
        audio_file = os.path.join(audio_folder, file)
        process_audio_to_srt(audio_file, model, srt_folder)
```

---

## Language Settings

The default language is English (`language="en"`). You can set the desired language code to perform speech recognition in various languages:

- `en`: English
- `ja`: Japanese
- `ko`: Korean

Example:

```python
segments, info = model.transcribe(audio_file, beam_size=5, language="ko")
```

---

## Usage Instructions

Place the audio files for subtitle generation in the directory containing the `transcribe_audio.py` file, and follow these steps:

### Run the following command in the terminal:

```bash
python transcribe_audio.py
```

This command generates SRT subtitles for all `.mp3` files in the specified directory and saves them to the `SRT` folder.

---

## Notes

- When using GPU, make sure `cuBLAS` and `cuDNN` are correctly installed.
- To use CPU only, set `device="cpu"`:

```python
model = WhisperModel(model_size, device="cpu", compute_type="float32")
```

- For additional customization and the latest updates, refer to the [Fast-Whisper GitHub page](https://github.com/SYSTRAN/faster-whisper).

---

## Supported Language Codes

Various language codes are supported. Check and apply the desired language code:

- `es`: Spanish
- `fr`: French
- `de`: German
