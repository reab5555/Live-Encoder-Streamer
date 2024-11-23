<img src="appendix/icon.png" alt="Alt text for image1" width="100"/>

# Live Encoder-Streamer

This is a Python-based tool for live streaming video and audio using **FFmpeg**. This script supports streaming to **UDP/TCP** and/or **RTMP/RTSP** endpoints with customizable configurations for video and audio devices. It is compatible with both **Windows** and **Linux** platforms.

------------------------------------------------------------------------------------

<img src="appendix/workflow.png" alt="Alt text for image1" width="400"/>

## Features

- **Multi-Platform Support**:
  - Uses `dshow` for Windows and `v4l2/alsa` for Linux to handle video and audio devices.
- **Multiple Streaming Outputs**:
  - Stream simultaneously to **UDP/TCP** and **RTMP/RTSP** or choose one based on your preference.
- **Customizable Streaming Options**:
  - Adjust video resolution, frame rate, audio bitrate, and more.
- **Device Listing**:
  - Easily list available video and audio devices.
- **Error Monitoring**:
  - Captures and displays FFmpeg errors in real-time.

## Prerequisites
**FFmpeg**: Make sure FFmpeg is installed and added to your system's PATH or provide its installation path in the script

Linux:   
```bash
sudo apt install ffmpeg
```

Windows:   
[https://www.ffmpeg.org/download.html](https://www.ffmpeg.org/download.html#build-windows)

## Usage

### Step 1: Clone this repository

```bash
git clone https://github.com/reab5555/ffmpeg-streaming-tool.git
cd ffmpeg-streaming-tool
```

### Step 2: Install the required dependencies
```bash
pip install -r requirements.txt
```

### Step 3: Configure the script
Edit the config section in the script to provide:   

- Path to FFmpeg binary (if on Windows).   
- UDP and RTMP URLs for streaming.   

### Step 4: Run the script
```bash
python streamer.py
```

Step 5: Follow on-screen prompts
1. List available devices.   
2. Choose video and audio devices.   
3. Select the desired streaming option (UDP, RTMP, or both).   
