한국어 | [English](README_en.md)

# MCP Naver News

![License](https://img.shields.io/github/license/ChangooLee/mcp-naver-news)
![PyPI Version](https://img.shields.io/pypi/v/mcp-naver-news)
![PyPI Downloads](https://img.shields.io/pypi/dm/mcp-naver-news)

Naver News API를 위한 Model Context Protocol(MCP) 서버입니다. 이 통합은 데이터 프라이버시와 보안을 유지하면서 Naver News와의 안전하고 맥락적인 AI 상호작용을 가능하게 합니다.

## 설치

### 필수 조건

- Python 3.8 이상
- Naver Developers API 키

### API 키 발급

먼저 Naver News API 키를 얻으세요:

1. [Naver Developers](https://developers.naver.com/)에 접속
2. 애플리케이션 등록
3. News 검색 API 사용 신청
4. 발급받은 Client ID와 Client Secret을 `.env` 파일에 설정

### 설치 방법

```bash
git clone https://github.com/ChangooLee/mcp-naver-news.git
cd mcp-naver-news
pip install -e .
```

## 사용 방법

### 환경 설정

`.env` 파일을 생성하고 다음 내용을 입력하세요:

```env
NAVER_NEWS_API_KEY=your_api_key_here
MCP_SERVER_NAME=mcp-naver-news
```

### IDE 통합

MCP Naver News는 IDE 통합을 통해 AI 어시스턴트와 함께 사용하도록 설계되었습니다.

#### VS Code 설정

`settings.json`에 다음을 추가하세요:

```json
"mcp.servers": {
    "mcp-naver-news": {
        "command": "YOUR_LOCATION/.venv/bin/mcp-naver-news",
        "env": {
            "NAVER_NEWS_API_KEY": "API-KEY",
            "MCP_SERVER_NAME": "mcp-naver-news"
        }
    }
}
```

> - `YOUR_LOCATION`: 가상환경이 설치된 경로
> - `API-KEY`: 발급받은 Naver News API 키로 변경

### 환경 변수

- `NAVER_NEWS_API_KEY`: Naver News API 키
- `NAVER_NEWS_BASE_URL`: API 기본 URL (기본값: 공식 URL)
- `MCP_SERVER_NAME`: MCP 서버 이름
- `MCP_HOST`: 서버 호스트 (기본값: localhost)
- `MCP_PORT`: 서버 포트 (기본값: 8000)
- `LOG_LEVEL`: 로그 레벨 (기본값: INFO)
- `LOG_FILE`: 로그 파일 경로 (기본값: naver_news.log)

### Naver News 도구

다음 도구들을 사용할 수 있습니다:

- 뉴스 검색
- 뉴스 상세 정보 조회
- 뉴스 카테고리별 검색
- 뉴스 정렬 및 필터링

## 문제 해결

### 로그 확인

문제가 발생하면 로그 파일을 확인하세요:

```bash
tail -f naver_news.log
```

### API 연결 테스트

API 연결을 테스트하려면:

```bash
python -m mcp_naver_news test-connection
```

## 기여하기

버그 리포트나 기능 요청은 GitHub 이슈를 통해 해주세요.

## 라이선스

이 프로젝트는 MIT 라이선스 하에 배포됩니다.

## 면책 조항

이 프로젝트는 공식 Naver 제품이 아닙니다. Naver는 Naver Corporation의 등록 상표입니다. 