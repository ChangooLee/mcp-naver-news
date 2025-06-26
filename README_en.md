[한국어](README.md) | English

# MCP Naver News

![License](https://img.shields.io/github/license/ChangooLee/mcp-naver-news)
![PyPI Version](https://img.shields.io/pypi/v/mcp-naver-news)
![PyPI Downloads](https://img.shields.io/pypi/dm/mcp-naver-news)

Model Context Protocol (MCP) server for Naver News API. This integration enables secure, contextual AI interactions with Naver News while maintaining data privacy and security.

## Example Usage

Ask your AI assistant to:

- **📰 News Search** - "Find recent news about Samsung Electronics"
- **🔍 News Analysis** - "Show me the latest technology news"
- **📊 News Trends** - "What are the trending topics in business news?"
- **⚡ Real-time Updates** - "Get the latest news about AI developments"

### Feature Demo

[Demo video will be added here]

### Compatibility

| Feature | Support Status | Description |
|---------|---------------|-------------|
| **News Search** | ✅ Fully supported | Search news articles with various parameters |
| **News Sorting** | ✅ Fully supported | Sort by date or relevance |
| **News Filtering** | ✅ Fully supported | Filter by date range and other criteria |

## Quick Start Guide

### 1. Authentication Setup

First, obtain your Naver News API credentials:

1. Go to [Naver Developers](https://developers.naver.com/)
2. Register your application
3. Apply for News Search API usage
4. Get your Client ID and Client Secret

### 2. Installation

```bash
# Clone repository
git clone https://github.com/ChangooLee/mcp-naver-news.git
cd mcp-naver-news

# [IMPORTANT] Ensure you are using Python 3.10 or higher. See: 'Checking and Installing Python 3.10+' below.

# Create virtual environment
python3.10 -m venv .venv
source .venv/bin/activate

# Install package
# python 3.10 >= required
python3 -m pip install --upgrade pip
pip install -e .
```

---

## Checking and Installing Python 3.10+

# Check Python version (must be 3.10 or higher)
python3 --version

# If your Python version is lower than 3.10, follow the instructions below to install Python 3.10 or higher:

### macOS
- Download the latest Python installer from the official website: https://www.python.org/downloads/macos/
- Or, if you use Homebrew:
  ```sh
  brew install python@3.10
  ```
  After installation, you may need to use `python3.10` instead of `python3`.

### Windows
- Download and run the latest Python installer from: https://www.python.org/downloads/windows/
- During installation, make sure to check "Add Python to PATH".
- After installation, restart your terminal and use `python` or `python3`.

### Linux (Ubuntu/Debian)
- Update package list and install Python 3.10:
  ```sh
  sudo apt update
  sudo apt install python3.10 python3.10-venv python3.10-distutils
  ```
- You may need to use `python3.10` instead of `python3`.

### Linux (Fedora/CentOS/RHEL)
- Install Python 3.10:
  ```sh
  sudo dnf install python3.10
  ```

## IDE Integration

MCP Naver News is designed to be used with AI assistants through IDE integration.

### Claude Desktop Configuration

1. Click hamburger menu (☰) > Settings > Developer > "Edit Config" button
2. Add the following configuration:

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
> - `YOUR_LOCATION`: Replace with the actual path where your virtual environment is installed
> - `YOUR_CLIENT_ID`: Replace with your Naver API Client ID
> - `YOUR_CLIENT_SECRET`: Replace with your Naver API Client Secret

### Environment Variables

- `X_NAVER_CLIENT_ID`: Your Naver API Client ID
- `X_NAVER_CLIENT_SECRET`: Your Naver API Client Secret
- `MCP_SERVER_NAME`: Server name (default: mcp-naver-news)
- `MCP_HOST`: Server host (default: 0.0.0.0)
- `MCP_PORT`: Server port (default: 8000)
- `LOG_LEVEL`: Logging level (INFO, DEBUG, etc.)
- `LOG_FILE`: Log file path (default: naver_news.log)

## Tools

### Naver News Tools

> **Recommended Analysis Strategy:**
> For efficient and deep news analysis, always use `search_news` first to quickly research, filter, and shortlist articles based on summaries and metadata. Only after identifying articles of interest should you use `search_news_detail` for robust, in-depth extraction and analysis of the full article content. This two-step workflow enables both broad exploration and targeted, in-depth insight, making your research process both fast and thorough.

- `search_news`: Quickly search news articles using the Naver News API and return only the API results (title, summary, link, etc.). This tool does NOT extract the full article content, making it fast and lightweight. Use this for initial exploration, filtering, and keyword-based summaries. **Always use this tool first!**
- `search_news_detail`: After filtering with `search_news`, use this tool to robustly extract and analyze the full article content from the web page. This tool is slower and more resource-intensive, but provides the full, accurate article text for in-depth analysis. **Use only for articles that require deep understanding.**

#### Typical Workflow

1. Use `search_news` to quickly browse and filter articles by summary and metadata.
2. For articles of interest, use `search_news_detail` to extract and analyze the full article content.

<details>
<summary>Tool Parameters</summary>

| Tool                | Parameter         | Type     | Description                                             |
|---------------------|------------------|----------|---------------------------------------------------------|
| search_news         | `query`          | string   | Search keyword                                          |
|                     | `display`        | integer  | Number of results to display (default: 10)              |
|                     | `start`          | integer  | Start position of results (default: 1)                  |
|                     | `sort`           | string   | Sort option (sim: relevance, date: date)                |
| search_news_detail  | `query`          | string   | Search keyword                                          |
|                     | `display`        | integer  | Number of results to display (default: 10)              |
|                     | `start`          | integer  | Start position of results (default: 1)                  |
|                     | `sort`           | string   | Sort option (sim: relevance, date: date)                |
|                     | `include_content`| bool     | Whether to extract full article content (default: true) |

</details>

## Troubleshooting & Debugging

### Common Issues

- **Authentication Failures**:
  - Check if your Client ID and Secret are valid
  - Verify your API credentials have the necessary permissions
  - Check if you've exceeded the API rate limit

- **Data Access Issues**:
  - Some data may require additional permissions
  - Check if the search parameters are valid
  - Ensure your query is properly formatted

- **Connection Problems**:
  - Verify your internet connection
  - Check if the Naver API service is available
  - Ensure your firewall isn't blocking the connection

### Debugging Tools

```bash
# Enable verbose logging
export LOG_LEVEL=DEBUG

# View logs
tail -f naver_news.log

# Test API connection
python -m mcp_naver_news test-connection
```

## Security

- Never share your API credentials
- Keep `.env` files secure and private
- Use appropriate rate limiting
- Monitor your API usage
- Store sensitive data in environment variables

## Contributing

We welcome contributions! If you'd like to contribute:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## License

This project is for non-commercial and personal use only. Commercial use, redistribution, or creation of derivative works for commercial purposes is strictly prohibited.

See the LICENSE file for full terms.

This is not an official Naver product. Naver is a registered trademark of Naver Corporation. 