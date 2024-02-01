import os
import pytest
import requests
from utils import encode_image, extract_coord_keyword, refine_output, concat_all, make_json

apps_path = os.path.abspath(os.path.join(__file__, os.path.pardir))
img_path = os.path.abspath(os.path.join(apps_path, "images"))
 
# MOCK data
API_KEY = ""
IMAGE_PATH = os.path.abspath(os.path.join(img_path, "landscape0.png"))

# Tood : 로컬 이미지가 들어왔을 때 설명 / 키워드 / 좌표 추출 
@pytest.mark.asyncio
async def test_focus_pointing():
    # TODO : 이미지 bse64인코딩 -> 이미지 설명 +키워드 + 좌표 추출  -> 좌표 반환
    # given : 유효한 데이터(이미지)

    base64_image = encode_image(IMAGE_PATH)
    
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {API_KEY}"
    }

    payload = {
        "model": "gpt-4-vision-preview",
        "messages": [
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text" : "You are an expert art historian with vast knowledge about artists throughout history who revolutionized their craft. You will begin by briefly summarizing the personal life and achievements of the artist. Then you will go on to explain the medium, style, and influences of their works. Then you will provide short descriptions of what they depict and any notable characteristics they might have. Fianlly identify THREE keywords in the picture and provide each coordinate of the keywords in the last sentence. For example if the keyword is woman, the output must be 'woman':[[x0,y0,x1,y1]] ",
                    },
                    {
                        "type": "image_url",
                        "image_url": {  
                            "url": f"data:image/jpeg;base64,{base64_image}"
                        }
                    }
                ]
            }
        ],
        "max_tokens": 800
    }   

    response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload)
    
    #응답에서 해설 추출
    content = response.json()['choices'][0]['message']['content']

    #해설에서 키워드/좌표 딕셔너리 추출
    key_coord_pair = extract_coord_keyword(content)

    #해설 정제후 추출 
    content = refine_output(content)

    #키워드/좌표/키워드 해설 추출    
    key_coord_description = concat_all(content,key_coord_pair)

    #output(json)
    json_data = make_json(content, key_coord_description)

    assert response.status_code == 200
    assert json_data
