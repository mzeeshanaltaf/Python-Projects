# This program make use of Python module (pytube) to download YouTube videos.
# It asks the user for the URL (link of YouTube video) as an input
# This program has the following functionality:
#     * Print video details like Title, Resolution, # of views, Length etc.
#     * Print video download progress
#     * Print video file name and output dir name once the video has been downloaded

from pytube import YouTube
import os

output_dir = "./download"


def download_progress_callback(stream, chunk, remaining_bytes):
    # Calculate the download percentage
    total_bytes = stream.filesize
    downloaded_bytes = total_bytes - remaining_bytes
    download_percentage = (downloaded_bytes / total_bytes) * 100

    print(f"Downloaded: {download_percentage:.2f}%")


def download_complete_callback(stream, fp):
    f_name = os.path.basename(fp)
    print(f"Download of file '{f_name}' has been completed at the following location: '{output_dir}'")


def format_views(views):
    if views < 1000:
        return views
    elif views < 1000000:
        return f"{views / 1000:.1f}K"
    else:
        return f"{views / 1000000:.1f}M"


def download_youtube_videos(v_url, output):
    # Create a YouTue object
    yt = YouTube(v_url)

    # Register callback function to print download progress and print
    # status when download get completed
    yt.register_on_progress_callback(download_progress_callback)
    yt.register_on_complete_callback(download_complete_callback)

    # Get the video stream
    yd = yt.streams.get_lowest_resolution()

    # Print YouTube video details
    print("Title:", yt.title)
    print("Resolution:", yd.resolution)
    print("Views:", format_views(yt.views))
    print(f"Length: {int(yt.length / 60)}:{yt.length % 60:02d}")
    print("Channel Name:", yt.author)
    print(f"File Size: {yd.filesize_mb:.1f}MB")

    # Download YouTube video
    yd.download(output)


# Ask the user for YouTube URL
video_url = input("Enter the link of youtube video to download: ")
download_youtube_videos(video_url, output_dir)
