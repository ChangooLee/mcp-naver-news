import logging
import sys
import asyncio
from starlette.requests import Request
from collections.abc import AsyncGenerator, Sequence
from contextlib import asynccontextmanager
from dataclasses import dataclass
from typing import Annotated, Any, Literal, Optional

from fastmcp import FastMCP, ServerSession
from mcp.types import TextContent
from mcp.server.session import ServerSession
from pydantic import Field

from .config import NaverNewsConfig, MCPConfig
from .apis.client import NaverNewsClient
from .apis import ds001, ds002, ds003, ds004, ds005, ds006
from typing import AsyncIterator

# 로거 설정
logger = logging.getLogger("mcp-naver-news")

class NaverNewsContext(ServerSession):
    """Naver News API 컨텍스트"""
    
    client: Optional[NaverNewsClient] = None
    
    def __init__(self, client: NaverNewsClient):
        self.client = client
    
    async def __aenter__(self):
        """컨텍스트 진입 시 호출됩니다."""
        logger.info("🔁 NaverNewsContext entered (Claude requested tool execution)")
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """컨텍스트 종료 시 호출됩니다."""
        logger.info("🔁 NaverNewsContext exited")

# Naver News API 클라이언트 초기화
naver_news_client = NaverNewsClient(config=NaverNewsConfig.from_env())

# 1. NaverNewsContext 정의
naver_news_context = NaverNewsContext(
    client=naver_news_client
)

# 2. FastMCP 서버 생성
mcp = FastMCP(
    "Naver News MCP",
    description="Naver News tools and resources for interacting with news data",
    lifespan=naver_news_lifespan,
)

# 3. 도구 모듈 동적 로드
for module_name in [
    "news_tools",
]:
    try:
        importlib.import_module(f"mcp_naver_news.tools.{module_name}")
    except ImportError as e:
        logger.warning(f"Failed to import tool module {module_name}: {e}")

logger.info("✅ Initializing Naver News FastMCP server...")

async def naver_news_lifespan(app: FastMCP) -> AsyncIterator[NaverNewsContext]:
    """Lifespan manager for the Naver News FastMCP server.
    
    Creates and manages the NaverNewsClient instance and API modules.
    """
    logger.info("Initializing Naver News FastMCP server...")
    
    try:
        # Naver News 설정 로드
        naver_news_config = NaverNewsConfig.from_env()
        
        # Naver News API 클라이언트 초기화
        client = NaverNewsClient(config=naver_news_config)
        
        # 컨텍스트 생성
        ctx = NaverNewsContext(
            client=client
        )
        
        logger.info("Naver News client and API modules initialized successfully.")
        yield ctx
        
    except Exception as e:
        logger.error(f"Failed to initialize Naver News client: {e}", exc_info=True)
        raise
    
    finally:
        logger.info("Shutting down Naver News FastMCP server...")

def run_server():
    """Run the MCP Naver News server."""
    mcp.run()
