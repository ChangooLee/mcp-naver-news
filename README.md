English | [한국어](README.md)

# MCP Naver News

![License](https://img.shields.io/github/license/ChangooLee/mcp-naver-news)
![PyPI Version](https://img.shields.io/pypi/v/mcp-naver-news)
![PyPI Downloads](https://img.shields.io/pypi/dm/mcp-naver-news)

네이버 뉴스 API를 위한 Model Context Protocol (MCP) 서버입니다. 이 통합을 통해 데이터 프라이버시와 보안을 유지하면서 네이버 뉴스와 안전하고 컨텍스트 기반의 AI 상호작용이 가능합니다.

## 사용 예시

AI 어시스턴트에게 다음과 같이 요청할 수 있습니다:

- **📰 뉴스 검색** - "삼성전자 관련 최근 뉴스를 찾아줘"
- **🔍 뉴스 분석** - "최신 기술 뉴스를 보여줘"
- **📊 뉴스 트렌드** - "경제 뉴스에서 어떤 주제가 트렌드인가요?"
- **⚡ 실시간 업데이트** - "AI 개발 관련 최신 뉴스를 가져와줘"

### 기능 데모

[데모 영상이 여기에 추가될 예정입니다]

### 호환성

| 기능 | 지원 상태 | 설명 |
|------|-----------|------|
| **뉴스 검색** | ✅ 완전 지원 | 다양한 파라미터로 뉴스 기사 검색 |
| **뉴스 정렬** | ✅ 완전 지원 | 날짜 또는 관련도로 정렬 |
| **뉴스 필터링** | ✅ 완전 지원 | 날짜 범위 및 기타 기준으로 필터링 |

## 빠른 시작 가이드

### 1. 인증 설정

먼저 네이버 뉴스 API 인증 정보를 획득하세요:

1. [네이버 개발자 센터](https://developers.naver.com/) 방문
2. 애플리케이션 등록
3. 뉴스 검색 API 사용 신청
4. Client ID와 Client Secret 획득

### 2. 설치

```bash
# 저장소 클론
git clone https://github.com/ChangooLee/mcp-naver-news.git
cd mcp-naver-news

# [중요] Python 3.10 이상 사용 필수. 아래 'Python 3.10+ 설치 안내' 참고

# 가상 환경 생성
python3.10 -m venv .venv
source .venv/bin/activate

# 패키지 설치
# python 3.10 이상이 필요 
python3 -m pip install --upgrade pip
pip install -e .
```

---

## Python 3.10+ 설치 안내

# Python 버전 확인 (3.10 이상 필요)
python3 --version

# 만약 Python 버전이 3.10 미만이라면, 아래 안내에 따라 Python 3.10 이상을 설치하세요:

### macOS
- 공식 웹사이트에서 최신 Python 설치 파일을 다운로드: https://www.python.org/downloads/macos/
- 또는 Homebrew를 사용하는 경우:
  ```sh
  brew install python@3.10
  ```
  설치 후 `python3.10` 명령어를 사용해야 할 수 있습니다.

### Windows
- 공식 웹사이트에서 최신 Python 설치 파일을 다운로드 및 실행: https://www.python.org/downloads/windows/
- 설치 시 "Add Python to PATH" 옵션을 반드시 체크하세요.
- 설치 후 터미널을 재시작하고 `python` 또는 `python3` 명령어를 사용하세요.

### Linux (Ubuntu/Debian)
- 패키지 목록을 업데이트하고 Python 3.10 설치:
  ```sh
  sudo apt update
  sudo apt install python3.10 python3.10-venv python3.10-distutils
  ```
- `python3.10` 명령어를 사용해야 할 수 있습니다.

### Linux (Fedora/CentOS/RHEL)
- Python 3.10 설치:
  ```sh
  sudo dnf install python3.10
  ```

## IDE 통합

MCP Naver News는 IDE 통합을 통해 AI 어시스턴트와 함께 사용하도록 설계되었습니다.

### Claude Desktop 설정

1. 햄버거 메뉴 (☰) > 설정 > 개발자 > "설정 편집" 버튼 클릭
2. 다음 설정 추가:

```json
{
  "mcpServers": {
    "mcp-naver-news": {
      "command": "YOUR_LOCATION/.venv/bin/mcp-naver-news",
      "env": {
        "X_NAVER_CLIENT_ID": "YOUR_CLIENT_ID",
        "X_NAVER_CLIENT_SECRET": "YOUR_CLIENT_SECRET",
        "MCP_SERVER_NAME": "mcp-naver-news",
        "MCP_HOST": "0.0.0.0",
        "MCP_PORT": "8000",
        "TRANSPORT": "stdio",
        "LOG_LEVEL": "INFO"
      }
    }
  }
}
```

> [!NOTE]
> - `YOUR_LOCATION`: 가상 환경이 설치된 실제 경로로 교체
> - `YOUR_CLIENT_ID`: 네이버 API Client ID로 교체
> - `YOUR_CLIENT_SECRET`: 네이버 API Client Secret로 교체

### 환경 변수

- `X_NAVER_CLIENT_ID`: 네이버 API Client ID
- `X_NAVER_CLIENT_SECRET`: 네이버 API Client Secret
- `MCP_SERVER_NAME`: 서버 이름 (기본값: mcp-naver-news)
- `MCP_HOST`: 서버 호스트 (기본값: 0.0.0.0)
- `MCP_PORT`: 서버 포트 (기본값: 8000)
- `LOG_LEVEL`: 로깅 레벨 (INFO, DEBUG 등)
- `LOG_FILE`: 로그 파일 경로 (기본값: naver_news.log)

## 도구

### 네이버 뉴스 도구

- `search_news`: 다양한 파라미터로 뉴스 기사 검색

<details>
<summary>도구 파라미터</summary>

| 파라미터 | 타입 | 설명 |
|----------|------|------|
| `query` | string | 검색 키워드 |
| `display` | integer | 표시할 결과 수 (기본값: 10) |
| `start` | integer | 결과 시작 위치 (기본값: 1) |
| `sort` | string | 정렬 옵션 (sim: 관련도, date: 날짜) |

</details>

## 문제 해결 및 디버깅

### 일반적인 문제

- **인증 실패**:
  - Client ID와 Secret이 유효한지 확인
  - API 인증 정보에 필요한 권한이 있는지 확인
  - API 호출 제한을 초과했는지 확인

- **데이터 접근 문제**:
  - 일부 데이터는 추가 권한이 필요할 수 있음
  - 검색 파라미터가 유효한지 확인
  - 쿼리가 올바르게 포맷되었는지 확인

- **연결 문제**:
  - 인터넷 연결 확인
  - 네이버 API 서비스 가용성 확인
  - 방화벽이 연결을 차단하지 않는지 확인

### 디버깅 도구

```bash
# 상세 로깅 활성화
export LOG_LEVEL=DEBUG

# 로그 보기
tail -f naver_news.log

# API 연결 테스트
python -m mcp_naver_news test-connection
```

## 보안

- API 인증 정보를 절대 공유하지 마세요
- `.env` 파일을 안전하고 비공개로 보관하세요
- 적절한 속도 제한을 사용하세요
- API 사용량을 모니터링하세요
- 민감한 데이터는 환경 변수에 저장하세요

## 기여

기여를 환영합니다! 기여하려면:

1. 저장소를 포크하세요
2. 기능 브랜치를 생성하세요
3. 변경사항을 적용하세요
4. 풀 리퀘스트를 제출하세요

## 라이선스

이 프로젝트는 [MIT 라이선스](LICENSE)를 따릅니다.

이것은 공식 네이버 제품이 아닙니다. 네이버는 네이버 주식회사의 등록 상표입니다. 