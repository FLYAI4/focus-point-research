import os
import requests
import time
from utils import encode_image, extract_coord_keyword, refine_output, concat_all, make_json

apps_path = os.path.abspath(os.path.join(__file__, os.path.pardir))
img_path = os.path.abspath(os.path.join(apps_path, "images"))

API_KEY = ""
IMAGE_PATH = os.path.abspath(os.path.join(img_path, "landscape0.png"))

def focus_pointing():
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
                        "text" : "Descript this picture"
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

    #해설 정제후 추출 : 키워드/좌표 제거 
    content = refine_output(content)

    #해설/좌표/키워드 딕셔너리 생성    
    key_coord_description = concat_all(content,key_coord_pair)

    #딕셔너리 json 변환
    json_data = make_json(content, key_coord_description)

    return json_data

start = time.time()
print(focus_pointing())
end = time.time()

print("응답시간: {} 초".format(end-start))