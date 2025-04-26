import logging
import sys
import asyncio
from starlette.requests import Request
from collections.abc import AsyncGenerator, Sequence
from contextlib import asynccontextmanager
from dataclasses import dataclass
from typing import Annotated, Any, Literal, Optional

from fastmcp import FastMCP
from mcp.types import TextContent
from mcp.server.session import ServerSession
from pydantic import Field

from .config import NaverNewsConfig, MCPConfig
from .apis.client import NaverNewsClient
from .apis.news import NewsAPI

# 로거 설정
logger = logging.getLogger("mcp-naver-news")

@dataclass
class NaverNewsContext(ServerSession):
    """Naver News API 컨텍스트"""
    
    client: Optional[NaverNewsClient] = None
    news : Any = None
    
    def __post_init__(self):
        if self.client is None:
            from .config import NaverNewsConfig, MCPConfig
            config = NaverNewsConfig.from_env()
            self.client = NaverNewsClient(config=config)

        if self.news is None:
            from .apis.news import NewsAPI
            self.news = NewsAPI(self.client)
    
    async def __aenter__(self):
        """컨텍스트 진입 시 호출됩니다."""
        logger.info("🔁 NaverNewsContext entered (Claude requested tool execution)")
        return self
    
    async def __aexit__(self, *args):
        """컨텍스트 종료 시 호출됩니다."""
        logger.info("🔁 NaverNewsContext exited")

naver_news_client = NaverNewsClient(config=NaverNewsConfig.from_env())
naver_news_context = NaverNewsContext(
    client=naver_news_client,
    news=NewsAPI(naver_news_client)
)

ctx = naver_news_context

@asynccontextmanager
async def naver_news_lifespan(app: FastMCP) -> AsyncIterator[NaverNewsContext]:
    """Lifespan manager for the Naver News FastMCP server.
    
    Creates and manages the NaverNewsClient instance and API modules.
    """
    logger.info("Initializing Naver News FastMCP server...")
    
    try:
        # Naver News 설정 로드
        naver_news_config = NaverNewsConfig.from_env()
        mcp_config = MCPConfig.from_env()
        
        # Naver News API 클라이언트 초기화
        client = NaverNewsClient(config=naver_news_config)
        
        # API 초기화
        ctx = NaverNewsContext(
            client=client,
            news=NewsAPI(client)
        )
        
        logger.info("Naver News client and API modules initialized successfully.")
        yield ctx
        
    except Exception as e:
        logger.error(f"Failed to initialize Naver News client: {e}", exc_info=True)
        raise
    
    finally:
        logger.info("Shutting down Naver News FastMCP server...")

# MCP 서버 인스턴스 생성
mcp = FastMCP(
    "Naver News MCP",
    description="Naver News tools and resources for interacting with news data",
    lifespan=naver_news_lifespan
)

# 도구 모듈 동적 로드
import importlib
for module_name in [
    "news_tools",
]:
    try:
        importlib.import_module(f"mcp_naver_news.tools.{module_name}")
    except ImportError as e:
        logger.warning(f"Failed to import tool module {module_name}: {e}")

def main():
    logger.info("✅ Initializing Naver News FastMCP server...")
    transport = mcp_config.transport
    port = mcp_config.port

    if transport == "sse":
        asyncio.run(run_server(transport="sse", port=port))
    else:
        mcp.run()

async def run_server(
    transport: Literal["stdio", "sse"] = "stdio", 
    port: int = 8000
) -> None:
    """Run the MCP Naver News server.
    
    Args:
        transport: The transport to use for the server.
        port: The port to use for the server.
    """
    if transport == "stdio":
        await mcp.run_stdio_async()
    elif transport == "sse":
        await mcp.run_sse_async(host="0.0.0.0", port=port)
    else:
        raise ValueError(f"Invalid transport: {transport}")
