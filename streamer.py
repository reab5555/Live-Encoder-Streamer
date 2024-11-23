import subprocess
import os
import platform
from typing import Optional


def get_ffmpeg_binary(ffmpeg_path: Optional[str] = None) -> str:
    """Returns the path to the FFmpeg binary based on the OS."""
    if platform.system() == "Windows":
        if not ffmpeg_path:
            raise ValueError("FFmpeg path must be specified on Windows.")
        return os.path.join(ffmpeg_path, "bin", "ffmpeg.exe")
    else:
        return "ffmpeg"  # Assume FFmpeg is in the PATH on Linux


def create_stream_command(video_device: str, audio_device: str, udp_url: Optional[str],
                          rtmp_url: Optional[str], ffmpeg_path: Optional[str] = None) -> list:

    ffmpeg_bin = get_ffmpeg_binary(ffmpeg_path)

    # Base command with input devices
    command = [
        ffmpeg_bin,
        # Video input
        "-f", "dshow" if platform.system() == "Windows" else "v4l2",
        "-rtbufsize", "1024M",
        "-i", f"video={video_device}" if platform.system() == "Windows" else video_device,
        # Audio input
        "-f", "dshow" if platform.system() == "Windows" else "alsa",
        "-i", f"audio={audio_device}" if platform.system() == "Windows" else audio_device,
    ]

    # Add UDP output if URL is provided
    if udp_url:
        command.extend([
            # Video settings for UDP
            "-c:v", "libx264",
            "-preset", "ultrafast",
            "-tune", "zerolatency",
            "-s", "1920x1080",
            "-r", "25",
            # Audio settings for UDP
            "-c:a", "aac",
            "-b:a", "128k",
            "-ar", "44100",
            # UDP output
            "-f", "mpegts",
            "-muxdelay", "0.1",
            udp_url,
        ])

    # Add RTMP output if URL is provided
    if rtmp_url:
        command.extend([
            # Video settings for RTMP
            "-c:v", "libx264",
            "-preset", "veryfast",
            "-s", "1920x1080",
            "-r", "25",
            "-b:v", "2500k",
            # Audio settings for RTMP
            "-c:a", "aac",
            "-b:a", "128k",
            "-ar", "44100",
            # RTMP output
            "-f", "flv",
            rtmp_url
        ])

    return command


def stream_media(video_device: str, audio_device: str, udp_url: Optional[str],
                 rtmp_url: Optional[str], ffmpeg_path: Optional[str] = None) -> None:

    ffmpeg_bin = get_ffmpeg_binary(ffmpeg_path)

    command = create_stream_command(video_device, audio_device, udp_url, rtmp_url, ffmpeg_path)

    try:
        print("\nStarting stream:")
        if udp_url:
            print(f"UDP: {udp_url}")
        if rtmp_url:
            print(f"RTMP: {rtmp_url}")

        print(f"\nUsing devices:")
        print(f"Video: {video_device}")
        print(f"Audio: {audio_device}")
        print(f"\nPress Ctrl+C to stop streaming")

        process = subprocess.Popen(
            command,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )

        # Monitor FFmpeg output
        while True:
            output = process.stderr.readline()
            if output == '' and process.poll() is not None:
                break
            if output:
                if "Error" in output or "error" in output:
                    print(f"FFmpeg Error: {output.strip()}")
                else:
                    print(output.strip())

    except KeyboardInterrupt:
        print("\nStreaming interrupted by user.")
    except Exception as e:
        print(f"Streaming error: {e}")
    finally:
        if 'process' in locals():
            process.terminate()
            process.wait()
        print("Stream ended.")


def list_devices(ffmpeg_path: Optional[str] = None) -> None:
    """List available video and audio devices."""
    ffmpeg_bin = get_ffmpeg_binary(ffmpeg_path)
    try:
        result = subprocess.run(
            [ffmpeg_bin, "-list_devices", "true", "-f", "dshow" if platform.system() == "Windows" else "v4l2", "-i", "dummy"],
            capture_output=True,
            text=True
        )
        print("Available devices:\n", result.stderr)
    except Exception as e:
        print(f"Error listing devices: {e}")


if __name__ == "__main__":
    # Configuration
    config = {
        "ffmpeg_path": r"C:\path\to\ffmpeg" if platform.system() == "Windows" else None,
        "udp_url": "udp://000.0.0.1:0000",  # Set your UDP URL
        "rtmp_url": "rtmp://localhost:1935/live/stream"  # Set your RTMP URL
    }

    # List available devices
    list_devices(config["ffmpeg_path"])

    # Set the video and audio devices
    video_device = "your-video-device-to-stream"  # Replace with your video source
    audio_device = "your-audio-device-to-stream"  # Replace with your audio source

    # Ask user for streaming option
    print("\nChoose streaming option:")
    print("1. Stream to both UDP and RTMP")
    print("2. Stream to UDP only")
    print("3. Stream to RTMP only")
    option = input("Enter option (1/2/3): ").strip()

    udp_url = None
    rtmp_url = None

    if option == "1":
        udp_url = config["udp_url"]
        rtmp_url = config["rtmp_url"]
    elif option == "2":
        udp_url = config["udp_url"]
    elif option == "3":
        rtmp_url = config["rtmp_url"]
    else:
        print("Invalid option selected. Exiting.")
        exit(1)

    # Start streaming
    try:
        stream_media(
            video_device,
            audio_device,
            udp_url,
            rtmp_url,
            config["ffmpeg_path"]
        )
    except Exception as e:
        print(f"Error: {e}")
