# LLaVa
### **Description**

이미지 url + prompting → 키워드 → 키워드 prompting → 좌표 → (키워드,좌표) 표시

### **Model**

- **llava : 이미지에서 좌표 추출 후 따로 그려줘야 함. 상대적으로 느림.**
- **CogAgent : 좌표 없이 키워드로 bbox 그리기 가능, 빠름. api 사용 여부 확인 필요**

### Research

**1. LLAVA**

- **이미지 url 입력**
    
    > 위키피디아/나무위키 이미지 Byte error → bing ai 와의 연동 고려
    일반 웹 이미지는 잘 됨
    > 
- **이미지에서 키워드 추출 prompting**
    
    - 키워드 수 3개 제한 → 불필요한 키워드 제거 필요(키워드 1개인 경우 등)
    - 그림 종류별 prompting 필요
    - 감상 포인트 < 객체
    
    
    ```python
    # 프롬프트 답변
    prompt = "USER: <image>\nWhat are the main objects in this picture? Just pick 3 WORDs\nASSISTANT:"
    outputs = pipe(image, prompt=prompt, generate_kwargs={"max_new_tokens": 500})
    
    # 키워드 추출
    keywords = outputs[0]["generated_text"].split('ASSISTANT: ')[1].split(', ')
    
    #결과
    **['Leaves', 'branches', 'and blue paint.']**
    ```
    
    - 일반 그림 ⇒ good
    - 풍경화 ⇒ good
        
        [0] : Dolphins, ocean, mountains

        [1] : Balloons, mountains, and trees.
        
        [2] : Trees, sky, and grass
        
    - 추상화
        
        [0] : Leaves, branches, and blue paint.
        
        [1] : Paint, canvas, colors
        
        [2] : Circle, sphere, and triangle.
        
        ⇒ paint, canvas, colors(?)  : 키워드 추출할 거 없을 때 출력됨
        
    - 인물화
        
        [0] :  Woman, Painting, Art
        
        [1] : Nails, lips, and eyes
        
        [2] : Man, glasses, and shirt.
        
        ⇒ painting, art : 키워드 추출할 거 없을 때 출력됨
        
- **이미지에서 키워드 기반 좌표 추출 prompting**
    ```
    - 좌표 자체의 정확성 문제  
    - 키워드에 해당하는 객체가 이미지에 없을 때  
    - 답변 형식 일관되지 않음 → 키워드/좌표 추출 문제 → 시드 고정..?  
    - 시간(대략 10~20초)
    ```
    
    
    ```python
    # prompting
    prompt_for_coord =  "USER: <image>\nTell me the each one coordinate of {}. For example, if the keyword is 'woman', the output must be 'woman: (x1, y1, x2, y2)'.\nASSISTANT:".format(", ".join(keywords))
    outputs_coord = pipe(image, prompt=prompt_for_coord, generate_kwargs={"max_new_tokens": 500})
    
    # 출력
    USER:  
    Tell me the each one coordinate of Leaves, branches, and blue paint.. For example, if the keyword is 'woman', the output must be 'woman: (x1, y1, x2, y2)'.
    ASSISTANT: Leaves: (0.18, 0.48, 0.32, 0.61)
    Branches: (0.39, 0.45, 0.58, 0.66)
    Blue paint: (0.28, 0.64, 0.44, 0.81)
    
    # 좌표 추출
    def extract_coordinates(text):
        text = text[0]["generated_text"]
        dic={}
    
        # 좌표 추출
        coord_pattern = r'\((.*?)\)' # 괄호 안 모든 문자 패턴
        coord_matches = re.findall(coord_pattern, text)[1:]
        coordinates = [tuple(map(float, m.split(', '))) for m in coord_matches]
    
        # 키워드 추출
        keyword_pattern = r'(\b\w+):'  # '단어:' 패턴
        keyword_matches = re.findall(keyword_pattern, text)[3:]
    
        # 키워드-좌표 딕셔너리 생성
        for i in range(len(coordinates)):
          dic[keyword_matches[i]] = coordinates[i]
    
        return dic
    
    dic = extract_coordinates(outputs_coord)
    
    # 키워드 : 좌표 추출
    {'Leaves': (0.18, 0.48, 0.32, 0.61), 'Branches': (0.39, 0.45, 0.58, 0.66), 'paint': (0.28, 0.64, 0.44, 0.81)}
    ```
    
    <image src="../images/Untitled (42).png" />
    <image src="../images/Untitled (43).png" />
    

- **이미지에 좌표 표시**
    
    > 이미지와, 키워드-좌표 딕셔너리 입력
    > 
    
    ```python
    def draw_box(dic,image):
      coords = [c for c in dic.values()]
      img = copy.deepcopy(image)
      width, height = img.size  
    
      print(coords)
      # 이미지 크기에 맞게 좌표 변환
      coords = [[c*width if i%2==0 else c*height for i, c in enumerate(sublist)] for sublist in coords]
      print(coords)
    
      # 박스 그리기
      draw = ImageDraw.Draw(img)
      for i, c in enumerate(coords):
        colors = [random.randint(0, 255) for _ in range(3)]
        draw.rectangle(c, outline=(colors[0],colors[1],colors[2]), width=3)
        draw.text(c, keywords[i], colors[i]) 
    
      img.show()
      img
    
    draw_box(dic,image)
    ```
    
    <img src="../images/Untitled (46).png" />



