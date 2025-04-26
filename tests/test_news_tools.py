import pytest
import os
from mcp_naver_news.config import NaverNewsConfig
from mcp_naver_news.apis.client import NaverNewsClient
from mcp_naver_news.apis.news import NewsAPI
from mcp_naver_news.tools.news_tools import search_news
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

def test_search_news_with_content():
    """Test search_news tool with content extraction"""
    # 환경 변수 확인
    client_id = os.environ.get("X_NAVER_CLIENT_ID")
    client_secret = os.environ.get("X_NAVER_CLIENT_SECRET")
    
    if not client_id or not client_secret:
        pytest.skip("네이버 API 키가 설정되지 않았습니다")
    
    # 뉴스 검색 실행
    result = search_news(
        query="삼성카드",
        display=2,
        include_content=True
    )
    
    # 결과 검증
    assert result.type == "text"
    
    # JSON 파싱
    news_items = json.loads(result.text)
    assert isinstance(news_items, list)
    assert len(news_items) > 0
    
    # 첫 번째 기사 검증
    first_item = news_items[0]
    assert '제목' in first_item
    assert '링크' in first_item
    assert '원본링크' in first_item
    assert '요약' in first_item
    assert '발행일' in first_item
    assert '본문' in first_item
    
    # 결과 출력
    print("\n=== 검색 결과 ===")
    for i, item in enumerate(news_items, 1):
        print(f"\n기사 {i}:")
        print(f"제목: {item['제목']}")
        print(f"발행일: {item['발행일']}")
        print(f"본문 길이: {len(item['본문'])}자")
        print("\n=== 본문 전문 ===")
        print(f"{item['본문']}")
        print("\n=== 링크 ===")
        print(f"{item['링크']}")
        print("\n" + "="*80) 