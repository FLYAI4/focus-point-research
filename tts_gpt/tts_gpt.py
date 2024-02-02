from IPython.display import display, Image, Audio

import base64
import time
import os
import requests
from utils import refine_text, save_audio

#MOCK DATA : focus-pointing으로 받아온 content
CONTENT = "As an AI art historian, I cannot provide a specific artist's biography, personal life, or achievements since the artist who created this artwork is not identified, and the work itself does not correspond to a recognizable style of a well-known artist whose biography I could summarize. Nevertheless, I will provide an analysis based on the visible characteristics of the image.  The artwork presented is a painting that utilizes a brightly colored, somewhat stylized approach to landscape depiction. The medium appears to be acrylic or oil paint, given the vibrancy of colors and the smooth texture of the surfaces.  The style of this painting is reminiscent of naïve art or might suggest an idyllic and harmonious view of the world, somewhat in line with folk art traditions. The use of bright colors, the absence of realistic perspective, and the simplified forms lend the artwork a serene and idealized quality, which is often found in works intended to evoke a sense of peace and nostalgia.  The painting depicts a lush, green landscape, featuring rolling hills or terraced fields, a lake snaking through the valleys, and a clear sky. There are several hot air balloons floating in the sky, suggesting a leisurely or whimsical atmosphere. A noticeable characteristic includes the rhythmical patterns of the terraced fields, which draw the viewer's eye across the canvas, creating a sense of movement and dynamism despite the stillness of the scene."
API_KEY = "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"

def tts(content: str):

    # 텍스트 정제
    content = refine_text(content)

    response = requests.post(
        "https://api.openai.com/v1/audio/speech",
        headers={
            "Authorization": f"Bearer {API_KEY}",
        },
        json={
            "model": "tts-1",
            "input": content,
            "voice": "nova",
        },
    )

    # 오디오 파일 이진 데이터로 변환
    audio = b""
    for chunk in response.iter_content(chunk_size=1024 * 1024):
        audio += chunk

    #.mp3로 오디오 파일 저장
    save_audio(audio)

    return audio

start = time.time()
audio = tts(CONTENT)
end = time.time()

print(f"응답시간: {end-start} 초")
