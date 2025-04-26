from typing import Dict, Any, Optional, List
from ..apis.client import NaverNewsClient
import requests
from bs4 import BeautifulSoup
import re
from urllib.parse import urlparse


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

    def extract_article_content(self, url: str) -> Dict[str, str]:
        """
        뉴스 기사 URL에서 본문 내용을 추출합니다.
        
        Args:
            url (str): 뉴스 기사 URL
            
        Returns:
            Dict[str, str]: {
                'title': 기사 제목,
                'content': 기사 본문,
                'error': 에러 메시지 (에러 발생 시)
            }
        """
        try:
            # User-Agent 설정
            headers = {
                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                'Accept-Language': 'ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7',
                'Cache-Control': 'no-cache',
                'Pragma': 'no-cache',
            }
            
            # URL에서 도메인 추출
            domain = urlparse(url).netloc
            
            # 요청 및 응답
            response = requests.get(url, headers=headers, timeout=10)
            response.raise_for_status()
            
            # HTML 파싱
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # 제목 추출
            title = soup.find('title').text.strip() if soup.find('title') else ''
            
            # 본문 추출 (도메인별 다른 선택자 적용)
            content = ''
            if 'news.naver.com' in domain:
                # 네이버 뉴스의 본문
                article = soup.find('div', id='newsct_article') or soup.find('div', id='articeBody')
                if article:
                    # 불필요한 요소 제거
                    for element in article.find_all(['script', 'style', 'iframe', 'ins']):
                        element.decompose()
                    content = article.get_text(strip=True)
            elif 'nspna.com' in domain:
                # 여러 선택자 시도
                article = (
                    soup.find('div', id='articleBody') or
                    soup.find('div', class_='article-body') or
                    soup.find('div', class_='article-content') or
                    soup.find('article')
                )
                if article:
                    # 불필요한 요소 제거
                    for element in article.find_all(['script', 'style', 'iframe', 'ins', 'div', 'class']):
                        element.decompose()
                    content = article.get_text(strip=True)
            elif 'yna.co.kr' in domain:
                article = soup.find('article', class_='story-news')
                if article:
                    content = article.get_text(strip=True)
            elif 'hankyung.com' in domain:
                article = soup.find('div', id='articletxt')
                if article:
                    content = article.get_text(strip=True)
            else:
                # 일반적인 뉴스 사이트 패턴
                article = soup.find('article') or soup.find('div', class_=re.compile('article|content|body'))
                if article:
                    content = article.get_text(strip=True)
            
            # 본문이 없으면 에러 반환
            if not content:
                return {
                    'title': title,
                    'content': '',
                    'error': '본문 내용을 찾을 수 없습니다.'
                }
            
            # 결과 반환
            return {
                'title': title,
                'content': content,
                'error': ''
            }
            
        except requests.exceptions.RequestException as e:
            return {
                'title': '',
                'content': '',
                'error': f'기사 접근 중 오류 발생: {str(e)}'
            }
        except Exception as e:
            return {
                'title': '',
                'content': '',
                'error': f'기사 파싱 중 오류 발생: {str(e)}'
            } 