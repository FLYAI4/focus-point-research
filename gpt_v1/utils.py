import re
import base64
import json

# 이미지 base64 인코딩
def encode_image(image_path: str) -> str:
  with open(image_path, "rb") as image_file:

    return base64.b64encode(image_file.read()).decode('utf-8')
  

# 설명 정제(키워드-좌표 쌍 제거)
def refine_output(content: str) -> str:
    '''
    Args:
        content (str): 키워드, 좌표 쌍이 포함된 텍스트

    Returns:
        str: 키워드와 좌표 쌍이 제거된 텍스트
    '''

    keyword = ':'
    if keyword in content:
        content = content[:content.find(keyword)].strip()
    content = content.replace('\n', ' ').strip()
    return content


# 설명에서 키워드, 좌표 추출
def extract_coord_keyword(content: str) -> dict[str, list[int]]:
    '''
    Args:
        content (str): 키워드와 좌표를 추출할 텍스트

    Returns:
        dict: 키워드를 키로, 좌표를 값으로 갖는 딕셔너리
    ''' 

    #'문자열': [[숫자, 공백, 콤마의 조합]] 패턴
    pattern = r"'([^']+)':\s*\[\[([\d\s,]+)\]\]"
    matches = re.findall(pattern, content)
    dic = {}
    for match in matches:
        word, coordinates = match
        coordinates = list(map(int, coordinates.replace(" ", "").split(',')))
        if all(isinstance(item,int) for item in coordinates): 
            dic[word] = [coordinates]

    return dic


#최종 아웃풋 딕셔너리 생성
def concat_all(content: str, dic: dict) -> dict[str,list[list[int],str]]:
    '''
    Args:
        content (str): 텍스트
        dic (dict): 키워드와 좌표를 담은 딕셔너리

    Returns:
        dict: 각 키워드에 대한 설명을 추가한 새로운 딕셔너리
    '''

    for k,v in dic.items():
        dic[k].append("")
 
    sentences = content.split('. ')
    for sentence in sentences:
        #키워드 포함된 문장 추출
        for key in dic.keys():
            if key in sentence:
                tmp = dic[key][1]
                if tmp:
                    tmp = tmp + ". " + sentence
                else:
                    tmp += sentence
                dic[key][1] = tmp

    return dic


def make_json(content: str, key_coord_pair: dict) -> str:
    dic={}
    dic["content"] = content
    dic["key_coord_pair"] = key_coord_pair        

    json_data = json.dumps(dic)

    return json_data
   
