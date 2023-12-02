import os
from pytube import YouTube 
import subprocess

def get_info(yt):
    # Get the title of the video
    name = yt.title
    # Get the length of the video in seconds
    video_length = yt.length
    # Convert the length to hours, minutes, seconds
    hours = video_length // 3600
    minutes = (video_length % 3600) // 60
    seconds = video_length % 60
    return name, hours, minutes, seconds

def download_video(yt, parent_dir):
    # Download the video
    stream = yt.streams.filter(file_extension='mp4').first()
    if stream:
        filename = stream.download(parent_dir)
        return filename
    else:
        return None

def convert_to_mp3(original_file, new_file, parent_dir):
    # Define the ffmpeg command for conversion to MP3
    command = [
        'ffmpeg', '-i', os.path.join(parent_dir, original_file),
        os.path.join(parent_dir, new_file)
    ]
    # Execute the command
    subprocess.run(command)
    # Remove the original file
    os.remove(os.path.join(parent_dir, original_file))

def crop_video(filename, duration, parent_dir, original_name):
    # Define the new filename for the cropped video
    cropped_filename = os.path.splitext(filename)[0] + '_cropped.mp4'
    # Define the ffmpeg command for cropping
    command = [
        'ffmpeg', '-i', os.path.join(parent_dir, filename),
        '-t', str(duration), '-c', 'copy',
        os.path.join(parent_dir, cropped_filename)
    ]
    # Execute the command
    subprocess.run(command)
    # Convert the cropped video to MP3
    mp3_filename = original_name + '.mp3'
    convert_to_mp3(cropped_filename, mp3_filename, parent_dir)

def delete_mp4_if_exists(song_name, parent_dir):
    # Construct the expected MP4 filename
    mp4_filename = song_name + '.mp4'
    mp4_file_path = os.path.join(parent_dir, mp4_filename)

    # Check if the file exists and delete it if it does
    if os.path.exists(mp4_file_path):
        os.remove(mp4_file_path)
        print(f"Deleted file: {mp4_file_path}")
    else:
        print(f"No MP4 file found for: {mp4_filename}")


# Define the URL and parent directory
        
vid = 'https://music.youtube.com/watch?v=q_hsw3ksmvM&si=71JVNisLLSGLLXvv'

yt_url = vid
parent_dir = '/Users/michael_adlerstein/Desktop/songs/downloads'

# Create a YouTube object
yt = YouTube(yt_url)

# Get video info
name, h, m, s = get_info(yt)

# Download the video
downloaded_filename = download_video(yt, parent_dir)
if downloaded_filename:
    # Crop the video to the length
    total_seconds = h * 3600 + m * 60 + s
    crop_video(downloaded_filename, total_seconds, parent_dir, name)

delete_mp4_if_exists(name, parent_dir)
