import logging
from typing import Any, Optional, List, Dict
from mcp_naver_news.server import mcp
from mcp.types import TextContent
from mcp_naver_news.utils.ctx_helper import with_context
import json
from mcp_naver_news.utils.article_extractor import extract_article_content

logger = logging.getLogger("mcp-naver-news")

@mcp.tool(
    name="search_news",
    description="""
    [Always use this tool first for news research!]
    Quickly search news articles using the Naver News API and return only the API results (title, summary, link, etc.).
    This tool does NOT extract the full article content, making it fast and lightweight. Use this for initial exploration, filtering, and keyword-based summaries.
    Only after you have identified articles of interest should you use 'search_news_detail' for in-depth analysis.
    """,
    tags={"기사", "뉴스", "검색", "네이버뉴스", "요약"}
)
def search_news(
    query: str,
    display: Optional[int] = 10,
    start: Optional[int] = 1,
    sort: Optional[str] = "sim",
    ctx: Optional[Any] = None
) -> TextContent:
    """
    네이버 뉴스 검색 (본문 미포함, 반드시 먼저 사용)
    Args:
        query (str): 검색어
        display (Optional[int]): 결과 수 (기본값: 10)
        start (Optional[int]): 시작 위치 (기본값: 1)
        sort (Optional[str]): 정렬 옵션 (기본값: "sim")
    Returns:
        TextContent: 기사 요약 리스트
    """
    result = with_context(ctx, "search_news", lambda context: context.news.search_news(
        query=query,
        display=display,
        start=start,
        sort=sort
    ))
    formatted_result = []
    for item in result.get('items', []):
        formatted_item = {
            '제목': item.get('title', ''),
            '링크': item.get('link', ''),
            '원본링크': item.get('originallink', ''),
            '요약': item.get('description', ''),
            '발행일': item.get('pubDate', '')
        }
        formatted_result.append(formatted_item)
    return TextContent(
        type="text",
        text=json.dumps(formatted_result, ensure_ascii=False, indent=2)
    )

@mcp.tool(
    name="search_news_detail",
    description="""
    [Use this tool ONLY after using 'search_news' to filter articles.]
    This tool searches news articles and robustly extracts the actual article content from the web page.
    It is slower and more resource-intensive, but provides the full, accurate article text for in-depth analysis.
    Use this tool only for articles that require deep understanding or content analysis, after initial exploration with 'search_news'.
    """,
    tags={"기사", "뉴스", "검색", "네이버뉴스", "본문", "심층분석"}
)
def search_news_detail(
    query: str,
    display: Optional[int] = 10,
    start: Optional[int] = 1,
    sort: Optional[str] = "sim",
    include_content: Optional[bool] = True,
    ctx: Optional[Any] = None
) -> TextContent:
    """
    네이버 뉴스 검색 및 robust 본문 추출 (심층분석용, 반드시 search_news 이후 사용)
    Args:
        query (str): 검색어
        display (Optional[int]): 결과 수 (기본값: 10)
        start (Optional[int]): 시작 위치 (기본값: 1)
        sort (Optional[str]): 정렬 옵션 (기본값: "sim")
        include_content (Optional[bool]): 기사 본문 포함 여부 (기본값: True)
    Returns:
        TextContent: 기사 리스트 (본문 포함)
    """
    result = with_context(ctx, "search_news_detail", lambda context: context.news.search_news(
        query=query,
        display=display,
        start=start,
        sort=sort
    ))
    if include_content and result.get('items'):
        for item in result['items']:
            try:
                content_result = extract_article_content(item['link'])
                if not content_result.get('error'):
                    item['content'] = content_result['content']
                else:
                    item['content'] = f"본문 추출 실패: {content_result['error']}"
                    logger.warning(f"기사 본문 추출 실패: {item['link']} - {content_result['error']}")
            except Exception as e:
                item['content'] = f"본문 추출 중 오류 발생: {str(e)}"
                logger.error(f"기사 본문 추출 중 오류: {item['link']} - {str(e)}")
    formatted_result = []
    for item in result.get('items', []):
        formatted_item = {
            '제목': item.get('title', ''),
            '링크': item.get('link', ''),
            '원본링크': item.get('originallink', ''),
            '요약': item.get('description', ''),
            '발행일': item.get('pubDate', ''),
            '본문': item.get('content', '본문 없음')
        }
        formatted_result.append(formatted_item)
    return TextContent(
        type="text",
        text=json.dumps(formatted_result, ensure_ascii=False, indent=2)
    ) 