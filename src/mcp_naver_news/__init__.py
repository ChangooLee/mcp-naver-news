# Naver News MCP Python 패키지 초기화
import importlib
import click
from mcp_naver_news.server import mcp

# 도구 모듈 등록 (모든 @mcp.tool decorator)
for module_name in [
    "news_tools",
]:
    importlib.import_module(f"mcp_naver_news.tools.{module_name}")

@click.command()
def main():
    """Naver News MCP 서버를 실행합니다."""
    mcp.run()

if __name__ == "__main__":
    main()
