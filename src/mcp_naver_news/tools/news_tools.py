import logging
from typing import Any, Optional
from mcp_naver_news.server import mcp
from mcp.types import TextContent
from mcp_naver_news.utils.ctx_helper import with_context

logger = logging.getLogger("mcp-naver-news")

@mcp.tool(
    name="search_news",
    description="네이버 뉴스 검색 API를 통해 뉴스를 검색합니다. 반환값에는 뉴스 제목, 링크, 요약, 발행일 등의 항목이 포함됩니다.",
    tags={"기사", "뉴스", "검색", "네이버뉴스"}
)
def search_news(
    query: str,
    display: Optional[int] = 10,
    start: Optional[int] = 1,
    sort: Optional[str] = "sim",
    ctx: Optional[Any] = None
) -> TextContent:
    """
    네이버 뉴스 검색

    Args:
        query (str): 검색어 (필수)
        display (Optional[int]): 한 번에 표시할 검색 결과 수 (선택, 기본값: 10)
        start (Optional[int]): 검색 시작 위치 (선택, 기본값: 1)
        sort (Optional[Literal["sim", "date"]]): 정렬 옵션 (선택, 기본값: "sim").
            - "sim" : 정확도순
            - "date" : 날짜순

    참고: https://developers.naver.com/docs/serviceapi/search/news/news.md
    """
    result = with_context(ctx, "search_news", lambda context: context.news.search_news(
        query=query,
        display=display,
        start=start,
        sort=sort
    ))
    return TextContent(type="text", text=str(result)) 