import logging
from typing import Any, Optional, List, Dict
from mcp_naver_news.server import mcp
from mcp.types import TextContent
from mcp_naver_news.utils.ctx_helper import with_context
import json

logger = logging.getLogger("mcp-naver-news")

@mcp.tool(
    name="search_news",
    description="네이버 뉴스 검색 API를 통해 뉴스를 검색하고, 각 기사의 본문을 추출합니다. 반환값에는 뉴스 제목, 링크, 요약, 발행일, 본문 등의 항목이 포함됩니다.",
    tags={"기사", "뉴스", "검색", "네이버뉴스", "본문"}
)
def search_news(
    query: str,
    display: Optional[int] = 10,
    start: Optional[int] = 1,
    sort: Optional[str] = "sim",
    include_content: Optional[bool] = True,
    ctx: Optional[Any] = None
) -> TextContent:
    """
    네이버 뉴스 검색 및 본문 추출

    Args:
        query (str): 검색어 (필수)
        display (Optional[int]): 한 번에 표시할 검색 결과 수 (선택, 기본값: 10)
        start (Optional[int]): 검색 시작 위치 (선택, 기본값: 1)
        sort (Optional[Literal["sim", "date"]]): 정렬 옵션 (선택, 기본값: "sim").
            - "sim" : 정확도순
            - "date" : 날짜순
        include_content (Optional[bool]): 기사 본문 포함 여부 (선택, 기본값: True)

    참고: https://developers.naver.com/docs/serviceapi/search/news/news.md
    """
    # 뉴스 검색
    result = with_context(ctx, "search_news", lambda context: context.news.search_news(
        query=query,
        display=display,
        start=start,
        sort=sort
    ))

    # 기사 본문 추출
    if include_content and result.get('items'):
        for item in result['items']:
            try:
                content_result = with_context(ctx, "extract_article_content", 
                    lambda context: context.news.extract_article_content(item['link']))
                
                if not content_result.get('error'):
                    item['content'] = content_result['content']
                else:
                    item['content'] = f"본문 추출 실패: {content_result['error']}"
                    logger.warning(f"기사 본문 추출 실패: {item['link']} - {content_result['error']}")
            except Exception as e:
                item['content'] = f"본문 추출 중 오류 발생: {str(e)}"
                logger.error(f"기사 본문 추출 중 오류: {item['link']} - {str(e)}")

    # 결과 포맷팅
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