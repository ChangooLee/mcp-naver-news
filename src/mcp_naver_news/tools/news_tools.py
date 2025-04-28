import logging
from typing import Any, Optional, List, Dict
from mcp_naver_news.server import mcp
from mcp.types import TextContent
from mcp_naver_news.utils.ctx_helper import with_context
import json

logger = logging.getLogger("mcp-naver-news")

@mcp.tool(
    name="search_news",
    description="""네이버 뉴스 검색 API를 통해 뉴스를 검색하고, 각 기사의 본문을 추출합니다. 반환값에는 뉴스 제목, 링크, 요약, 발행일, 본문 등의 항목이 포함됩니다.\n\n검색어(query)에는 네이버 검색 고급 옵션(예: |, +, - 등)을 사용할 수 있습니다.\n- | : 여러 키워드 중 하나라도 포함된 결과 (예: 삼성전자|LG전자)\n- + : 반드시 포함할 단어 (예: 삼성전자+반도체)\n- - : 제외할 단어 (예: 삼성전자-스마트폰)\n자세한 옵션은 네이버 검색 도움말을 참고하세요.\n\n효과적인 검색 전략:\n1. 점진적 접근: 일반 키워드로 시작해 구체적인 키워드로 좁혀가는 방식으로 여러 번 검색하세요.\n2. 다각적 분석: 동일 주제에 대해 다른 관점의 키워드로 여러 검색을 수행하세요.\n3. 시간 범위 지정: 최신 정보나 특정 시기의 정보를 찾을 때는 연도, 월, 분기 등 시간 키워드를 포함하세요.\n4. 전문용어 활용: 산업/분야별 전문용어를 포함시켜 더 관련성 높은 결과를 얻으세요.\n\n검색어(query)에는 네이버 검색 고급 옵션을 사용할 수 있습니다:\n- | : 여러 키워드 중 하나라도 포함된 결과 (예: 삼성전자|LG전자)\n- + : 반드시 포함할 단어 (예: 삼성전자+반도체)\n- - : 제외할 단어 (예: 삼성전자-스마트폰)\n- \" \" : 정확한 구문 검색 (예: \"2025년 1분기 실적\")\n\n검색 예시:\n- 기본 검색: \"기업명 최근 이슈\"\n- 구체화 검색: \"기업명+실적+분기 -해외\"\n- 비교 검색: \"기업명|경쟁사 \"산업용어\" 기간\"\n\n적절한 검색 시퀀스를 통해 일반적인 개요부터 구체적인 정보까지 단계적으로 수집하여 종합적인 분석을 제공하세요.""",
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
        query (str): 검색어 (필수).\n\n네이버 검색 고급 옵션을 사용할 수 있습니다:\n- | (파이프): 여러 키워드 중 하나라도 포함된 결과 (예: 삼성전자|LG전자)\n- + (플러스): 반드시 포함할 단어 (예: 삼성전자+반도체)\n- - (마이너스): 제외할 단어 (예: 삼성전자-스마트폰)\n더 많은 옵션은 네이버 검색 도움말(https://help.naver.com/service/5626/contents/959?lang=ko) 참고.
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