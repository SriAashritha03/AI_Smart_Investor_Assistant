import yfinance as yf
import matplotlib.pyplot as plt
from moviepy.editor import ImageClip, AudioFileClip
from gtts import gTTS
import os
import uuid


def generate_market_video(ticker: str) -> str:
    try:
        print(f"Generating video for: {ticker}")

        # ---------------- FETCH DATA ----------------
        data = yf.download(ticker, period="5d")

        if data.empty:
            raise Exception("No data found")

        # ---------------- CREATE CHART ----------------
        img_path = f"chart_{uuid.uuid4().hex}.png"

        plt.figure(figsize=(6, 4))
        data["Close"].plot(title=f"{ticker} Price Movement")
        plt.xlabel("Date")
        plt.ylabel("Price")
        plt.tight_layout()
        plt.savefig(img_path)
        plt.close()

        # ---------------- CREATE AUDIO ----------------
        last_price = round(data["Close"].iloc[-1], 2)
        text = f"{ticker} latest price is {last_price}"

        audio_path = f"audio_{uuid.uuid4().hex}.mp3"
        tts = gTTS(text)
        tts.save(audio_path)

        # ---------------- CREATE VIDEO ----------------
        video_path = f"video_{uuid.uuid4().hex}.mp4"

        clip = ImageClip(img_path).set_duration(6)
        audio = AudioFileClip(audio_path)

        video = clip.set_audio(audio)
        video.write_videofile(video_path, fps=24)

        # ---------------- CLEANUP ----------------
        os.remove(img_path)
        os.remove(audio_path)

        return video_path

    except Exception as e:
        print("VIDEO ERROR:", str(e))
        raise