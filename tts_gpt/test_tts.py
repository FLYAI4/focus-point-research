import os
import pytest

from tts import TTSManager
from exception import TTSError

NO_TOKEN_ID_KEY = os.environ.get("OEPNAI_NO_API_KEY", 'utf-8')
TOKEN_KEY = os.environ.get("OEPNAI_API_KEY", 'utf-8')

#MOCK DATA
MAIN_CONTENT = "This image appears to be a painting rendered in a naturalistic and somewhat impressionistic style, which draws from tradition but also reflects more modern, relaxed brushwork and an interest in capturing a moment in time rather than detailing photographic realism.  The medium appears to be either oil or acrylic paint on canvas, as indicated by the texture and the way the light reflects off the surface. The style is somewhat simplified, with broad areas of color delineating the sky, the greenery, and the upright forms of the trees. The influences could include aspects of Impressionism, as well as a more contemporary minimalistic approach to composition and detail.  The painting depicts a landscape dominated by a series of tall, narrow poplar trees that draw the eye upward. The background features a light blue sky with subtle cloud details, suggesting a calm atmospheric condition. Beneath the trees, we see a green field that may suggest a crop just before maturity. A small house or building is nestled between the trees, adding a human element to the otherwise natural scene. The artist plays with the contrast between the vertical lines of the trees and horizontal bands of sky and field.  Notable characteristics include the sense of serenity and solitude conveyed by the spacious composition and the limited palette, which relies on variations of blue and green with hints of white, suggesting an uncluttered rural landscape."
COORD_CONTENT ={
        "trees": {"coord" : [55, 75, 455, 390], "content" : "The style is somewhat simplified, with broad areas of color delineating the sky, the greenery, and the upright forms of the trees.  The painting depicts a landscape dominated by a series of tall, narrow poplar trees that draw the eye upward. Beneath the trees, we see a green field that may suggest a crop just before maturity. A small house or building is nestled between the trees, adding a human element to the otherwise natural scene. The artist plays with the contrast between the vertical lines of the trees and horizontal bands of sky and field"},
        "field": {"coord" : [0, 400, 517, 640] , "content" : "Beneath the trees, we see a green field that may suggest a crop just before maturity. The artist plays with the contrast between the vertical lines of the trees and horizontal bands of sky and field"},
        "sky": {"coord" : [0, 0, 517, 75] , "content" : "The style is somewhat simplified, with broad areas of color delineating the sky, the greenery, and the upright forms of the trees. The background features a light blue sky with subtle cloud details, suggesting a calm atmospheric condition. The artist plays with the contrast between the vertical lines of the trees and horizontal bands of sky and field"}
}

@pytest.mark.asyncio
async def test_cannot_generate_audio_with_no_token():
    # given : 유효한 데이터(json 데이터) + 계정에 토큰이 없는 경우
    # when : 생성 요청
    # then : 토큰이 없는 경우 TTSError 발생
    with pytest.raises(TTSError):
        content_generator = TTSManager(MAIN_CONTENT,COORD_CONTENT,NO_TOKEN_ID_KEY).generate_audio()
        await content_generator.__anext__()

@pytest.mark.asyncio
async def test_cannot_generate_audio_with_no_data():
        # given : 메인 해설 있음 + 키워드 해설 없는 경우
        # when : 생성 요청
        content_generator = TTSManager(MAIN_CONTENT).generate_audio()
        main_audio = await content_generator.__anext__()
        
        # then : 정상 응답
        assert main_audio

@pytest.mark.asyncio
async def test_cannot_generate_audio_with_no_data():
    # given : 빈 데이터 + 계정 토큰 존재
    # when : 생성 요청
    # then : 빈 데이터의 경우 TTSError 발생
    with pytest.raises(TTSError):
        content_generator = TTSManager(token=TOKEN_KEY).generate_audio()
        await content_generator.__anext__()

@pytest.mark.asyncio
async def test_can_generate_audio_with_valid():
    # given : 유효한 데이터(json 데이터)

    # when : 생성 요청
    content_generator = TTSManager(MAIN_CONTENT,COORD_CONTENT).generate_audio()
    main_audio = await content_generator.__anext__()
    key_audio = await content_generator.__anext__()

    # then : 정상 응답
    assert main_audio
    assert key_audio