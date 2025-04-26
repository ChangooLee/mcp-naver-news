import os
import pytest
from mcp_naver_news.config import NaverNewsConfig
from mcp_naver_news.apis.client import NaverNewsClient
from mcp_naver_news.apis.news import NewsAPI
import json

@pytest.fixture
def news_api():
    """Initialize NewsAPI instance for testing"""
    config = NaverNewsConfig(
        client_id=os.environ.get("X_NAVER_CLIENT_ID"),
        client_secret=os.environ.get("X_NAVER_CLIENT_SECRET")
    )
    client = NaverNewsClient(config=config)
    return NewsAPI(client)

def test_search_news_response_structure(news_api):
    """Test the structure of the news search response"""
    # 검색 실행
    response = news_api.search_news(
        query="삼성전자",
        display=1,
        sort="date"
    )
    
    # 응답 결과 출력
    print("\n=== 응답 결과 ===")
    print(json.dumps(response, ensure_ascii=False, indent=2))
    
    # 응답 구조 검증
    assert isinstance(response, dict)
    assert "items" in response
    assert "lastBuildDate" in response
    assert "total" in response
    assert "start" in response
    assert "display" in response
    
    # items 배열의 첫 번째 항목 구조 검증
    if response["items"]:
        news_item = response["items"][0]
        assert "title" in news_item
        assert "originallink" in news_item
        assert "link" in news_item
        assert "description" in news_item
        assert "pubDate" in news_item

def test_search_news_parameters(news_api):
    """Test different parameter combinations"""
    # 기본 파라미터로 검색
    response1 = news_api.search_news(query="테스트")
    assert response1["display"] <= 10  # 기본값
    
    # display 파라미터 테스트
    response2 = news_api.search_news(query="테스트", display=5)
    assert response2["display"] <= 5
    
    # sort 파라미터 테스트
    response3 = news_api.search_news(query="테스트", sort="date")
    assert response3  # 날짜순 정렬 요청이 성공적으로 처리되었는지 확인

def test_search_news_error_handling(news_api):
    """Test error handling for invalid parameters"""
    with pytest.raises(Exception):  # 구체적인 예외 타입으로 수정 가능
        news_api.search_news(query="")  # 빈 쿼리

    with pytest.raises(Exception):
        news_api.search_news(query="테스트", display=0)  # 잘못된 display 값

def test_search_news_content_validation(news_api):
    """Test the content of news search results"""
    query = "파이썬"
    response = news_api.search_news(query=query)
    
    if response["items"]:
        news_item = response["items"][0]
        # HTML 태그가 제거되었는지 확인
        assert "<" not in news_item["title"]
        assert ">" not in news_item["title"]
        
        # 링크가 유효한 URL 형식인지 확인
        assert news_item["link"].startswith("http")
        
        # pubDate가 올바른 형식인지 확인
        assert len(news_item["pubDate"]) > 0 