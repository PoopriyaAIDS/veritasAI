import os
import tempfile

def extract_text_from_video(video_file):
    """Extract speech from uploaded video file using SpeechRecognition."""
    tmp_video = None
    tmp_audio = None

    try:
        import speech_recognition as sr
        from moviepy import VideoFileClip

        # Save uploaded video to temp file
        suffix     = os.path.splitext(video_file.filename)[1] or '.mp4'
        tmp_video  = tempfile.NamedTemporaryFile(delete=False, suffix=suffix)
        video_file.save(tmp_video.name)
        tmp_video.close()

        # Extract audio from video
        tmp_audio  = tempfile.NamedTemporaryFile(delete=False, suffix='.wav')
        tmp_audio.close()

        print(f"Extracting audio from video: {tmp_video.name}")
        clip = VideoFileClip(tmp_video.name)

        if clip.audio is None:
            clip.close()
            return None, "This video has no audio track."

        # Only use first 60 seconds to keep it fast
        duration = min(clip.duration, 60)
        clip     = clip.subclipped(0, duration)
        clip.audio.write_audiofile(tmp_audio.name, fps=16000, logger=None)
        clip.close()

        # Speech to text
        recognizer = sr.Recognizer()
        print("Converting speech to text...")

        with sr.AudioFile(tmp_audio.name) as source:
            recognizer.adjust_for_ambient_noise(source, duration=0.5)
            audio = recognizer.record(source)

        text = recognizer.recognize_google(audio)

        if len(text.strip()) < 20:
            return None, "Could not extract enough speech from the video."

        return text.strip(), None

    except sr.UnknownValueError:
        return None, "Could not understand the audio in the video. Please ensure the video has clear speech."
    except sr.RequestError as e:
        return None, f"Speech recognition service error: {str(e)}. Check your internet connection."
    except Exception as e:
        return None, f"Video processing failed: {str(e)}"

    finally:
        # Clean up temp files
        for f in [tmp_video, tmp_audio]:
            if f and os.path.exists(f.name):
                try:
                    os.unlink(f.name)
                except:
                    pass
