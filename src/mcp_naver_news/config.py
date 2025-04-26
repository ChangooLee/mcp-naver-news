import os
import logging
from typing import Literal, cast
from dataclasses import dataclass
from dotenv import load_dotenv

# .env 파일 로드
load_dotenv()

# 로거 설정
logger = logging.getLogger(__name__)

@dataclass
class NaverNewsConfig:
    """Naver News API configuration."""
    
    client_id: str
    client_secret: str
    base_url: str = "https://openapi.naver.com/v1/search/news.json"
    log_file: str = "naver_news.log"
    
    @classmethod
    def from_env(cls) -> "NaverNewsConfig":
        """Create a NaverNewsConfig with values from environment variables
        
        Returns:
            NaverNewsConfig: Configuration object with values from environment variables
        """
        client_id = os.getenv("X_NAVER_CLIENT_ID")
        client_secret = os.getenv("X_NAVER_CLIENT_SECRET")
        
        if not client_id or not client_secret:
            raise ValueError("Naver News API 클라이언트 ID와 시크릿이 설정되지 않았습니다. .env 파일을 확인하세요.")
        
        return cls(
            client_id=client_id,
            client_secret=client_secret,
            base_url=os.getenv("NAVER_NEWS_BASE_URL", "https://openapi.naver.com/v1/search/news.json"),
            log_file=os.getenv("LOG_FILE", "naver_news.log")
        )
 
@dataclass
class MCPConfig:
    """MCP 서버 설정"""
    
    server_name: str = "naver-news-mcp"
    host: str = "0.0.0.0"
    port: int = 8000
    log_level: str = "INFO"
    
    @classmethod
    def from_env(cls) -> "MCPConfig":
        """Create a MCPConfig with values from environment variables"""
        return cls(
            server_name=os.getenv("MCP_SERVER_NAME", "naver-news-mcp"),
            host=os.getenv("MCP_HOST", "localhost"),
            port=int(os.getenv("MCP_PORT", "8000")),
            log_level=os.getenv("LOG_LEVEL", "INFO")
        )

# 설정 인스턴스 생성
naver_news_config = NaverNewsConfig.from_env()
mcp_config = MCPConfig.from_env()