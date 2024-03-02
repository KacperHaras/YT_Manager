from pytube import YouTube, Playlist
from moviepy.editor import VideoFileClip, AudioFileClip
import re

# Get available resolutions for a video
def get_resolution(stream):
    return int(stream.resolution.replace('p', ''))

# Combine audio and video files for 1080p videos
def combine_audio(vidname, audname, outname, fps=25):
    my_clip = VideoFileClip(vidname)
    audio_background = AudioFileClip(audname)
    final_clip = my_clip.set_audio(audio_background)
    final_clip.write_videofile(outname, fps=fps)
    final_clip.close()   

# Get the description of a video
def get_description(url):
    yt = YouTube(url)
    for n in range(6):
        try:
            description =  yt.initial_data["engagementPanels"][n]["engagementPanelSectionListRenderer"]["content"]["structuredDescriptionContentRenderer"]["items"][1]["expandableVideoDescriptionBodyRenderer"]["attributedDescriptionBodyText"]["content"]            
            return description
        except:
            continue
    return False

# Get the captions of a video
def get_captions(xml, code):
    if code == 'en':
        mask = '<.*?>'
        stripped_text = re.sub(mask, '', xml).strip()

    else:
        text = re.sub(r'</p>', '\n', xml)

        text = re.sub(r'<.*?>', '', text)

        stripped_text = re.sub(r'\n\s*\n', '\n', text).strip()


    clean_text = stripped_text.replace('&amp;', '&').replace('&lt;', '<').replace('&gt;', '>')
    clean_text = clean_text.replace('&quot;', '"').replace('&#39;', "'").replace('&nbsp;', ' ')
    clean_text = clean_text.replace('&copy;', '©').replace('&reg;', '®').replace('&trade;', '™')
    clean_text = clean_text.replace('&euro;', '€').replace('&pound;', '£')

    return clean_text


# Get the duration of a playlist
def get_playlist_duration(playlist_url):
    playlist = Playlist(playlist_url)
    total_duration_seconds = 0

    for video_url in playlist.video_urls:
        try:
            video = YouTube(video_url)
            video_duration = video.length
            total_duration_seconds += video_duration
        except Exception as e:
            print(f"Error processing video {video_url}: {e}")

    return total_duration_seconds