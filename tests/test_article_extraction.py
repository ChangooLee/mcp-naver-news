import pytest
from mcp_naver_news.config import NaverNewsConfig
from mcp_naver_news.apis.client import NaverNewsClient
from mcp_naver_news.apis.news import NewsAPI
import os

@pytest.fixture
def news_api():
    """Initialize NewsAPI instance for testing"""
    config = NaverNewsConfig(
        client_id = os.environ.get("X_NAVER_CLIENT_ID"),
        client_secret = os.environ.get("X_NAVER_CLIENT_SECRET")
    )
    client = NaverNewsClient(config=config)
    return NewsAPI(client)

def test_extract_article_content(news_api):
    """Test article content extraction"""
    # 환경 변수 확인
    client_id = os.environ.get("X_NAVER_CLIENT_ID")
    client_secret = os.environ.get("X_NAVER_CLIENT_SECRET")
    
    if not client_id or not client_secret:
        pytest.skip("네이버 API 키가 설정되지 않았습니다")
    
    # API 클라이언트 초기화
    config = NaverNewsConfig(client_id=client_id, client_secret=client_secret)
    client = NaverNewsClient(config=config)
    news_api = NewsAPI(client)
    
    # 뉴스 검색을 수행하여 네이버 뉴스 링크 획득
    search_result = news_api.search_news(query="삼성전자", display=1)
    
    if not search_result['items']:
        pytest.skip("검색 결과가 없습니다")
    
    # 네이버 뉴스 링크 사용
    test_url = search_result['items'][0]['link']
    print(f"\n테스트 URL: {test_url}")
    
    # 기사 내용 추출
    result = news_api.extract_article_content(test_url)
    
    # 결과 검증
    assert isinstance(result, dict)
    assert 'title' in result
    assert 'content' in result
    assert 'error' in result
    
    # 에러가 없어야 함
    assert not result['error'], f"에러 발생: {result['error']}"
    
    # 제목과 본문이 비어있지 않아야 함
    assert result['title'], "제목이 비어있습니다"
    assert result['content'], "본문이 비어있습니다"
    
    # 결과 출력
    print("\n=== 추출된 기사 내용 ===")
    print(f"제목: {result['title']}")
    print(f"본문 길이: {len(result['content'])}자")
    print("\n=== 본문 전문 ===")
    print(f"{result['content']}") 