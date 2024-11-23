# Live Encoder-Streamer Tool

This is a Python-based tool for live streaming video and audio using **FFmpeg**. This script supports streaming to **UDP/TCP** and/or **RTMP/RTSP** endpoints with customizable configurations for video and audio devices. It is compatible with both **Windows** and **Linux** platforms.

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

1. **FFmpeg**: Make sure FFmpeg is installed and added to your system's PATH or provide its installation path in the script

Linux:   
```bash
sudo apt install ffmpeg
```

Windows:   
[https://www.ffmpeg.org/download.html](https://www.ffmpeg.org/download.html#build-windows)

4. **Python**: Python 3.6 or later.

## Usage

### Step 1: Clone this repository

```bash
git clone https://github.com/your-username/ffmpeg-streaming-tool.git
cd ffmpeg-streaming-tool

Step 2: Install the required dependencies

pip install -r requirements.txt

Step 3: Configure the script

Edit the config section in the script to provide:

    Path to FFmpeg binary (if on Windows).
    UDP and RTMP URLs for streaming.

Step 4: Run the script

python ffmpeg_streaming_tool.py

Step 5: Follow on-screen prompts

    List available devices.
    Choose video and audio devices.
    Select the desired streaming option (UDP, RTMP, or both).

Configuration Example

config = {
    "ffmpeg_path": r"C:\path\to\ffmpeg" if platform.system() == "Windows" else None,
    "udp_url": "udp://000.0.0.1:0000",  # Replace with your UDP URL
    "rtmp_url": "rtmp://localhost:1935/live/stream"  # Replace with your RTMP URL
}

How It Works

    Device Listing:
        Use the list_devices function to identify available video and audio devices.
    Command Generation:
        Dynamically generates an FFmpeg command based on user preferences.
    Streaming:
        Streams video and audio to the specified endpoints with real-time monitoring.

Example Command

For dual streaming to UDP and RTMP:

ffmpeg -f dshow -rtbufsize 1024M -i video="Camera" -f dshow -i audio="Microphone" \
-c:v libx264 -preset ultrafast -tune zerolatency -s 1920x1080 -r 25 -c:a aac \
-b:a 128k -ar 44100 -f mpegts udp://000.0.0.1:0000 \
-c:v libx264 -preset veryfast -s 1920x1080 -r 25 -b:v 2500k -c:a aac \
-b:a 128k -ar 44100 -f flv rtmp://localhost:1935/live/stream
