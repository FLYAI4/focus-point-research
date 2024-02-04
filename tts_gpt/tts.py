import requests
import os
from exception import TTSError
from error_code import TTSErrorCode

class TTSManager:
    def __init__(self, main_content: str = None, coord_content: dict = None, token: str = os.environ.get("OPENAI_API_KEY","utf-8")) -> None:
        self.headers = {
            "Authorization" : f"Bearer {token}"
        }
        self.main_content = main_content
        self.coord_content = coord_content 

    async def generate_audio(self) -> dict[str,str]:
        try:
            # 메인 해설 오디오 생성
            main_audio = await self.tts("main_content",self.main_content) 
            if not main_audio:
                raise TTSError(**TTSErrorCode.APIError.value)
            yield {"main_content" : main_audio}

            # 키워드 해설 오디오 생성
            if self.coord_content:
                key_audio={}
                keyword_content = {k : v["content"] for k,v in self.coord_content.items()}# 키워드,해설만 추출
                for k,v in keyword_content.items(): 
                    key_content_audio = await self.tts(k,v)
                    key_audio[k] = key_content_audio
                yield key_audio

        except Exception as e:
            raise TTSError(**TTSErrorCode.APIError.value,err=e)
    
    async def tts(self, title: str, content: str) -> str:
        payload = {
            "model": "tts-1",
            "input": content,
            "voice": "nova", #목소리 변경 가능
        }

        response = requests.post("https://api.openai.com/v1/audio/speech",
                                headers=self.headers,
                                json=payload,)
        print("\n",response.status_code)
        if response.status_code == 200:
            audio = self.__audio_to_binary(response)
            audio = self.__audio_to_mp3(title, audio)
            return audio
        
        elif response.status_code == 401:
            # print(response.json()["error"])
            raise TTSError(**TTSErrorCode.NonTokenError.value,
                                  err=response.json()["error"])            

    @staticmethod
    #음성 데이터 binary로 변환
    def __audio_to_binary(response) -> bytes: 
        audio = b""

        for chunk in response.iter_content(chunk_size=1024*1024):
            audio+=chunk

        return audio
    
    @staticmethod
    #binary 음성 데이터 mp3파일로 저장. 저장 경로 반환
    def __audio_to_mp3(title: str, audio: bytes) -> str: 
        filename = f'{title}.mp3'

        with open(filename, 'wb') as f:
            f.write(audio)
        
        return os.path.abspath(filename)