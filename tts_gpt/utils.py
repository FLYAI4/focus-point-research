import re

#TTS전 텍스트 정제
def refine_text(content: str) -> str:
    # AI 변명, focus-pointing에서 걸러지지 않은 문장 제거
    words=["cannot", "AI", "do not", "can't", "json", "JSON", "{",]
    output = ""

    sentences = content.split(". ")
    for sentence in sentences:
        if not any(word in sentence for word in words) and not re.search(r'\d',sentence):
            output+=sentence

    if not output:
        return content
    
    else:
        return output

# mp3 형태로 오디오 파일 저장
def save_audio(audio):
    with open('output.mp3', 'wb') as f:
        f.write(audio)

    