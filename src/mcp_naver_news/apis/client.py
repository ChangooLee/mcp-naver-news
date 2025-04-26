import requests
from urllib.parse import urljoin
import json
import logging
from typing import Dict, Any, Optional
import zipfile
import io

from ..config import naver_news_config, NaverNewsConfig

# 로거 설정
logger = logging.getLogger(__name__)

class NaverNewsClient:
    """네이버 뉴스 API 클라이언트"""
    
    def __init__(self, config: NaverNewsConfig):
        self.config = config
        self.base_url = "https://openapi.naver.com/v1/search"
        self.headers = {
            "X-Naver-Client-Id": config.client_id,
            "X-Naver-Client-Secret": config.client_secret
        }
    
    def get(self, endpoint: str, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        GET 요청을 보내고 응답을 반환합니다.
        
        Args:
            endpoint (str): API 엔드포인트
            params (Dict[str, Any], optional): 쿼리 파라미터
            
        Returns:
            Dict[str, Any]: API 응답
        """
        url = f"{self.base_url}/{endpoint}"
        response = requests.get(url, headers=self.headers, params=params)
        response.raise_for_status()
        return response.json()
    
    def post(self, endpoint: str, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """POST 요청을 수행합니다."""
        return self._make_request(endpoint, params, "POST")

    def _make_request(self, endpoint: str, params: Optional[Dict[str, Any]] = None, method: str = "GET") -> Dict[str, Any]:
        """API 요청을 보내고 응답을 반환합니다."""
        if params is None:
            params = {}
        
        url = urljoin(self.base_url, endpoint)
        
        # 디버그 로깅 추가
        logger.debug(f"\n=== API 요청 정보 ===")
        logger.debug(f"URL: {url}")
        logger.debug(f"Method: {method}")
        logger.debug(f"Parameters: {params}")
        logger.debug("====================")
        
        headers = {
            "X-Naver-Client-Id": self.config.client_id,
            "X-Naver-Client-Secret": self.config.client_secret,
            "Accept": "application/json"
        }
        
        try:
            if method.upper() == "GET":
                response = requests.get(url, params=params, headers=headers)
            elif method.upper() == "POST":
                response = requests.post(url, data=params, headers=headers)
            else:
                raise ValueError(f"지원하지 않는 HTTP 메서드: {method}")
            
            # 응답 로깅 추가
            logger.debug(f"\n=== API 응답 정보 ===")
            logger.debug(f"상태 코드: {response.status_code}")
            logger.debug(f"Content-Type: {response.headers.get('Content-Type', '없음')}")
            if "application/json" in response.headers.get("Content-Type", ""):
                logger.debug(f"응답 내용: {response.text}")
            logger.debug("====================")
            
            response.raise_for_status()
            
            # 응답 형식에 따라 처리
            content_type = response.headers.get("Content-Type", "")
            if "application/json" in content_type:
                data: Dict[str, Any] = response.json()
                return data
            else:
                return {
                    "status": "000",
                    "message": "정상",
                    "content": response.text
                }
        
        except requests.RequestException as e:
            logger.error(f"API 요청 실패: {str(e)}")
            return {"error": str(e), "status_code": getattr(e.response, 'status_code', None)}