from pydub import AudioSegment
import io
import os
from google.cloud import speech
from google.cloud.speech import enums
from google.cloud.speech import types
import wave
from google.cloud import storage
import subprocess
import math

filepath = os.getcwd() + "/"
output_filepath = filepath + "Transcripts/"


def run(html):
    htmlTags = [BeautifulSoup(item["snippet"], "html.parser").find() for item in html]
    video(htmlTags)


def video(htmlSnippets):
    for tag in htmlSnippets:
        video = tag.find("video")
        url = tag.find("video").get("src")
        google_transcribe(url)
        path = "transcript.txt"
        write_transcripts(path, transcript)
        video.append(
            tag.new_tag("source", src="path", label="English", srclang="en-us")
        )


def video_to_audio(url):
    print("Getting video")
    subprocess.call(["wget", "-O video.mp4", url], bufsize=0)
    print("Converting video to Wave")
    subprocess.call(["ffmpeg", "-i", " video.mp4", "audio.wav"], bufsize=0)


def mp3_to_wav(audio_file_name):
    if audio_file_name.split(".")[1] == "mp3":
        sound = AudioSegment.from_mp3(audio_file_name)
        audio_file_name = audio_file_name.split(".")[0] + ".wav"
        sound.export(audio_file_name, format="wav")


def frame_rate_channel(audio_file_name):
    with wave.open(audio_file_name, "rb") as wave_file:
        frame_rate = wave_file.getframerate()
        channels = wave_file.getnchannels()
        return frame_rate, channels


def stereo_to_mono(audio_file_name):
    print("Converting stereo to mono")
    sound = AudioSegment.from_wav(audio_file_name)
    sound = sound.set_channels(1)
    sound.export(audio_file_name, format="wav")


def upload_blob(bucket_name, source_file_name, destination_blob_name):
    print("Uploading the file to the bucket.")
    storage_client = storage.Client()
    bucket = storage_client.get_bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)

    blob.upload_from_filename(source_file_name)


def delete_blob(bucket_name, blob_name):
    print("Deleting the blob from the bucket.")
    storage_client = storage.Client()
    bucket = storage_client.get_bucket(bucket_name)
    blob = bucket.blob(blob_name)

    blob.delete()


def format_transcript(results, audio_file):
    def format_time(seconds, offset=0):  # time conversion/formatting for timestamps
        frac, whole = math.modf(seconds)
        f = frac * 1000
        m, s = divmod(whole, 60)
        h, m = divmod(m, 60)
        return "%d:%02d:%02d,%03d" % (h, m, s, (f + offset * 1000))

    """Used to break up large transcript sections to prevent multi-line subtitles"""

    def chunks(l, n):
        for i in range(0, len(l), n):
            yield l[i : i + n]

    file = open(audio_file + ".srt", "w")
    counter = 0  # Used for numbering lines in file

    for result in results:
        print(result)
        alternatives = result.alternatives
        for alternative in alternatives:
            print(alternative)
            words = alternative.words
            print(words)
            if len(words) < 14:
                transcript = alternative.transcript
                start_time = words[0].start_time
                end_time = words[-1].end_time
                start_time_seconds = start_time.seconds + start_time.nanos * 1e-9

                end_time_seconds = end_time.seconds + end_time.nanos * 1e-9

                counter += 1

                file.write(str(counter) + "\n")
                file.write(
                    format_time(start_time_seconds)
                    + " --> "
                    + format_time(end_time_seconds)
                    + "\n"
                )
                file.write(transcript + "\n\n")
            else:
                chunk = list(chunks(words, 14))
                for words in chunk:
                    start_time = words[0].start_time
                    end_time = words[-1].end_time

                    start_time_seconds = start_time.seconds + start_time.nanos * 1e-9

                    end_time_seconds = end_time.seconds + end_time.nanos * 1e-9

                    section = ""
                    for word_info in words:
                        section += word_info.word + " "

                    counter += 1
                    file.write(str(counter) + "\n")
                    file.write(
                        format_time(start_time_seconds)
                        + " --> "
                        + format_time(end_time_seconds)
                        + "\n"
                    )
                    file.write(section + "\n\n")
    file.close()


def google_transcribe(url):
    video_to_audio(url)

    audio_file_name = "audio.wav"
    file_name = filepath + audio_file_name
    # mp3_to_wav(file_name)

    # The name of the audio file to transcribe

    frame_rate, channels = frame_rate_channel(file_name)

    if channels > 1:
        stereo_to_mono(file_name)

    bucket_name = "awengine"
    source_file_name = filepath + audio_file_name
    destination_blob_name = audio_file_name

    upload_blob(bucket_name, source_file_name, destination_blob_name)

    gcs_uri = "gs://awengine/" + audio_file_name
    transcript = ""

    client = speech.SpeechClient()
    audio = types.RecognitionAudio(uri=gcs_uri)

    config = types.RecognitionConfig(
        encoding=enums.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=frame_rate,
        language_code="en-US",
        enable_word_time_offsets=True,
    )

    print("Detecting speech in the audio file")
    operation = client.long_running_recognize(config, audio)
    response = operation.result(timeout=10000)
    results = response.results

    raw_text_file = open(output_filepath + "transcript.txt", "w+")
    for result in results:
        for alternative in result.alternatives:
            raw_text_file.write(alternative.transcript + "\n")
    raw_text_file.close()
    format_transcript(results, output_filepath + "transcript")
    # output raw text file of transcription
    # for result in response.results:
    #    transcript += result.alternatives[0].transcript

    delete_blob(bucket_name, destination_blob_name)


# return transcript


def write_transcripts(transcript_filename, transcript):
    print("Writing the transcript")
    f = open(output_filepath + transcript_filename, "w+")
    f.write(transcript)
    f.close()
