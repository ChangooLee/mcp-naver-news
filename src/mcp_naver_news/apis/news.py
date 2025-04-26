from typing import Dict, Any, Optional, List
from ..apis.client import NaverNewsClient


class NewsAPI:
    """네이버 뉴스 검색 API"""
    
    def __init__(self, client: NaverNewsClient):
        self.client = client
    
    def search_news(
        self,
        query: str,
        display: Optional[int] = 10,
        start: Optional[int] = 1,
        sort: Optional[str] = "sim"
    ) -> Dict[str, Any]:
        """
        네이버 뉴스 검색
        https://developers.naver.com/docs/serviceapi/search/news/news.md
        
        Args:
            query (str): 검색어
            display (int, optional): 한 번에 표시할 검색 결과 개수 (기본값: 10)
            start (int, optional): 검색 시작 위치 (기본값: 1)
            sort (str, optional): 정렬 옵션 (sim: 정확도순, date: 날짜순, 기본값: sim)
            
        Returns:
            Dict[str, Any]: 검색 결과
        """
        endpoint = "news.json"
        params = {
            "query": query,
            "display": display,
            "start": start,
            "sort": sort
        }
        # None 값 제거
        params = {k: v for k, v in params.items() if v is not None}
        
        return self.client.get(endpoint, params) 