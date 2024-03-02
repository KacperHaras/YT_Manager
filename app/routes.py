from flask import Flask, render_template, request
from .utils import get_playlist_duration, get_resolution, combine_audio, get_description, get_captions
from pytube import YouTube, Playlist, Channel, exceptions
from werkzeug.utils import secure_filename 
import os
import re
from flask import current_app as app

@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')

@app.route('/get_info', methods=['GET', 'POST'])
def get_info():
    video_url = ''
    error_msg = None
    video_info = None
    if request.method == 'POST':
        video_url = request.form['video_url']
        try:
            if "list=" in video_url:
                pl = Playlist(video_url)
                first_video_url = None
                pl.length
                try:
                    first_video_url = pl.video_urls[0]
                except IndexError:
                    first_video_url = None

                if first_video_url:
                    ln = get_playlist_duration(video_url)
                       
                    video_info = {
                        'title': pl.title,
                        'thumbnail': YouTube(first_video_url).thumbnail_url,
                        'type': 'Playlist',
                        'length': ln,
                        'nb_videos': pl.length,
                    }
                    try:
                        video_info['owner'] = Channel(pl.owner_url).channel_name
                    except:
                        video_info['owner'] = "Unknown"
                else:
                    video_info = {
                        'title': '! Playlist is empty or unavailable !',
                        'owner': Channel(pl.owner_url).channel_name,
                        'thumbnail': '', 
                        'type': 'Playlist',

                    }
            elif "watch?v=" in video_url or "shorts" in video_url:
                yt = YouTube(video_url)

                stream = max(
                    filter(lambda s: get_resolution(s) <= 1080,
                    filter(lambda s: s.type == 'video', yt.fmt_streams)),
                    key=get_resolution
                )
                resolutions = list({stream.resolution for stream in yt.streams.filter(progressive=True, file_extension='mp4')})
                resolutions.append(stream.resolution)

                video_info = {
                    'title': yt.title,
                    'owner': Channel(yt.channel_url).channel_name,
                    'resolutions': resolutions,
                    'thumbnail': yt.thumbnail_url,
                    'views': yt.views,
                    'length': yt.length,
                    'type': (lambda x: 'Video' if "watch?v=" in video_url else 'Short_video')(video_url),
                    'keywords': yt.keywords,
                    'description': get_description(video_url),
                    'captions': get_captions(yt.captions.get_by_language_code(str(yt.captions.all()[0].code)).xml_captions, str(yt.captions.all()[0].code)) if (len(yt.captions) != 0) else None
                }
            else:
                raise ValueError("The URL does not correspond to a known YouTube video or playlist format.")
            
        
        except exceptions.PytubeError:
            error_msg = "Invalid YouTube link. Please try again."
        except ValueError as ve:
            error_msg = str(ve)
        except Exception as e:
            error_msg = f"An error occurred: {str(e)}"

    return render_template('get_info.html', video_url=video_url, video_info=video_info, error_msg=error_msg)


@app.route('/download', methods=['GET', 'POST'])
def download():
    video_url = ''
    error_msg = None
    video_info = None
    if request.method == 'POST':
        video_url = request.form['video_url']
        try:
            if "list=" in video_url:
                pl = Playlist(video_url)
                first_video_url = None
                try:
                    first_video_url = pl.video_urls[0]
                except IndexError:
                    first_video_url = None

                if first_video_url:
                    ln = get_playlist_duration(video_url)
                    
                    video_info = {
                        'title': pl.title,
                        'thumbnail': YouTube(first_video_url).thumbnail_url,
                        'type': 'Playlist',
                        'length': ln,
                        'nb_videos': pl.length,
                    }
                    try:
                        video_info['owner'] = Channel(pl.owner_url).channel_name
                    except:
                        video_info['owner'] = "Unknown"
                else:
                    video_info = {
                        'title': '! Playlist is empty or unavailable !',
                        'thumbnail': '', 
                        'type': 'Playlist'
                    }
                    try:
                        video_info['owner'] = Channel(pl.owner_url).channel_name
                    except:
                        video_info['owner'] = "Unknown"
            elif "watch?v=" in video_url or "shorts" in video_url:
                yt = YouTube(video_url)

                stream = max(
                    filter(lambda s: get_resolution(s) <= 1080,
                    filter(lambda s: s.type == 'video', yt.fmt_streams)),
                    key=get_resolution
                )
                resolutions = list({stream.resolution for stream in yt.streams.filter(progressive=True, file_extension='mp4')})
                resolutions.append(stream.resolution)
                video_info = {
                    'title': yt.title,
                    'resolutions': resolutions,
                    'thumbnail': yt.thumbnail_url,
                    'type': 'Video',
                    'length': yt.length,
                }
                try:
                    video_info['owner'] = Channel(pl.owner_url).channel_name
                except:
                    video_info['owner'] = "Unknown"
            else:
                raise ValueError("The URL does not correspond to a known YouTube video or playlist format.")

            return render_template('download.html', video_info=video_info, video_url=video_url)
        
        except exceptions.PytubeError:
            error_msg = "Invalid YouTube link. Please try again."
        except ValueError as ve:
            error_msg = str(ve)
        except Exception as e:
            error_msg = f"An error occurred: {str(e)}"

    return render_template('download.html', video_url=video_url, video_info=video_info, error_msg=error_msg)


@app.route('/download_video', methods=['POST'])
def download_video():
    video_url = request.form.get('video_url')
    download_type = request.form.get('download_type')
    resolution = request.form.get('resolution', None)

    yt = YouTube(video_url)
    target_folder = 'uploads/'

    if download_type == 'audio':
        stream = yt.streams.get_audio_only()
        filename = stream.download(output_path=target_folder, skip_existing=True)
        new_filename = os.path.join(target_folder, os.path.basename(filename).replace(" ", "_").replace('.mp4','_audio.mp4'))

        if not os.path.exists(new_filename):
            os.rename(filename, new_filename)
        else:
            os.remove(filename)
                          

    elif download_type == 'video':
        # Download video with audio if resolution is not 1080p, else download separately and combine
        if resolution != '1080p':
            stream = yt.streams.filter(res=resolution, progressive=True, file_extension='mp4').first()
            filename = stream.download(output_path=target_folder, skip_existing=True)
            new_filename = os.path.join(target_folder, os.path.basename(filename).replace(" ", "_").replace('.mp4','_video.mp4'))
    
            if not os.path.exists(new_filename):
                os.rename(filename, new_filename)
            else:
                os.remove(filename)
            
        else:
            video_stream = yt.streams.filter(res='1080p', progressive=False, file_extension='mp4').first()
            video_filename = video_stream.download(output_path=target_folder, skip_existing=True, filename_prefix='video_')
            audio_stream = yt.streams.get_audio_only()
            audio_filename = audio_stream.download(output_path=target_folder, skip_existing=True, filename_prefix='audio_')

            output_filename = yt.title.replace(' ','_') + "_HQ_video.mp4"
            combine_audio(video_filename, audio_filename, output_filename)

            os.remove(video_filename)
            os.remove(audio_filename)
            os.replace(output_filename, os.path.join(target_folder, output_filename))

    return render_template('download.html', video_url=video_url)


@app.route('/download_playlist', methods=['POST'])
def download_playlist():
    playlist_url = request.form.get('video_url')
    download_type = request.form.get('download_type')    

    pl = Playlist(playlist_url)
    target_folder = 'uploads/'
 
    if download_type == 'audio':
        for yt in pl.videos:
            stream = yt.streams.get_audio_only()
            filename = stream.download(output_path=target_folder, skip_existing=True)
            new_filename = os.path.join(target_folder, os.path.basename(filename).replace(" ", "_").replace('.mp4','_audio.mp4'))

            if not os.path.exists(new_filename):
                os.rename(filename, new_filename)
            else:
                os.remove(filename)

    elif download_type == 'video':
        for yt in pl.videos:
            ma = max(
                    filter(lambda s: get_resolution(s) <= 1080,
                    filter(lambda s: s.type == 'video', yt.fmt_streams)),
                    key=get_resolution
                )
            if ma.resolution != '720p':
                ma.resolution = '360p'

            stream = yt.streams.filter(res=ma.resolution, progressive=True, file_extension='mp4').first()
            filename = stream.download(output_path=target_folder, skip_existing=True)
            new_filename = os.path.join(target_folder, os.path.basename(filename).replace(" ", "_").replace('.mp4','_video.mp4'))
    
            if not os.path.exists(new_filename):
                os.rename(filename, new_filename)
            else:
                os.remove(filename)
            
    return render_template('download.html', video_url=playlist_url)



@app.route('/download_desc_links', methods=['POST'])
def download_desc_links():
    video_url = request.form.get('video_url')
    yt = YouTube(video_url)
    stream = yt.streams.first() # required to get following portions to work

    text = ''
    desc = yt.description.split('\n')
    
    for line in desc:
        line = line.strip()
        if re.search('http', line):
            text += line
            text += '\n'

    if desc:
        filename = yt.title.replace(' ', '_') + "_links.txt"
        filename = secure_filename(filename)  

        with open(os.path.join(app.config['UPLOAD_FOLDER'], filename), 'w', encoding='utf-8') as f:
                f.write(text)

    return get_info()


@app.route('/download_captions', methods=['POST'])
def download_captions():
    video_url = request.form.get('video_url')
    yt = YouTube(video_url)
    stream = yt.streams.first() # required to get following portions to work
   
    captions = get_captions(yt.captions.get_by_language_code(str(yt.captions.all()[0].code)).xml_captions, str(yt.captions.all()[0].code))

    if captions:
        filename = yt.title.replace(' ', '_') + "_captions.txt"
        filename = secure_filename(filename)  

        with open(os.path.join(app.config['UPLOAD_FOLDER'], filename), 'w', encoding='utf-8') as f:
            f.write(captions)

    return get_info()