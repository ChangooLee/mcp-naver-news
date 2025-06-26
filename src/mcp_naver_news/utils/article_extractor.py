import os
import re
import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse
from datetime import datetime
import logging
from typing import Optional, Dict

logger = logging.getLogger("mcp-naver-news")

def extract_article_content(url: str, output_dir: Optional[str] = None, retry_mode: bool = False) -> Dict[str, str]:
    today = datetime.now().strftime("%Y%m%d")
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7',
            'Cache-Control': 'no-cache',
            'Pragma': 'no-cache',
        }
        domain = urlparse(url).netloc
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        title = soup.find('title').text.strip() if soup.find('title') else ''
        content = ''
        if 'news.naver.com' in domain:
            article = soup.find('div', id='newsct_article') or soup.find('div', id='articeBody')
            if article:
                for element in article.find_all(['script', 'style', 'iframe', 'ins']):
                    element.decompose()
                content = article.get_text(strip=True)
        elif 'nspna.com' in domain:
            article = (
                soup.find('div', id='articleBody') or
                soup.find('div', class_='article-body') or
                soup.find('div', class_='article-content') or
                soup.find('article')
            )
            if article:
                for element in article.find_all(['script', 'style', 'iframe', 'ins', 'div', 'class']):
                    element.decompose()
                content = article.get_text(strip=True)
        elif 'yna.co.kr' in domain:
            article = soup.find('article', class_='story-news')
            if article:
                content = article.get_text(strip=True)
        elif 'hankyung.com' in domain:
            article = soup.find('div', id='articletxt')
            if article:
                content = article.get_text(strip=True)
        else:
            article = soup.find('article') or soup.find('div', class_=re.compile('article|content|body'))
            if article:
                content = article.get_text(strip=True)
        if not content:
            article = soup.find('div', id='articleBody', class_=lambda x: x and 'view_con' in x)
            if article:
                for element in article.find_all(['script', 'style', 'iframe', 'ins']):
                    element.decompose()
                content = article.get_text(strip=True)
            if not content:
                candidate_selectors = [
                    {'id': 'articleBody'}, {'class_': 'article-body'}, {'class_': 'article-content'},
                    {'class_': 'view_con'}, {'id': 'news_content'}, {'id': 'content'}, {'id': 'textBody'},
                    {'id': 'article_content'}, {'id': 'article'}, {'class_': 'article'},
                    {'id': 'article-view-content-div'}, {'name': 'article'}, {'name': 'section', 'class_': 'article'},
                ]
                for sel in candidate_selectors:
                    if 'id' in sel and 'class_' in sel:
                        article = soup.find(sel.get('name', 'div'), id=sel['id'], class_=sel['class_'])
                    elif 'id' in sel:
                        article = soup.find(id=sel['id'])
                    elif 'class_' in sel:
                        article = soup.find(class_=sel['class_'])
                    elif 'name' in sel and 'class_' in sel:
                        article = soup.find(sel['name'], class_=sel['class_'])
                    elif 'name' in sel:
                        article = soup.find(sel['name'])
                    else:
                        article = None
                    if article:
                        for element in article.find_all(['script', 'style', 'iframe', 'ins']):
                            element.decompose()
                        content = article.get_text(strip=True)
                        if content:
                            break
        if content and len(content) < 100:
            content = ''
        if not content:
            error_msg = '본문 내용을 찾을 수 없습니다.'
            return {
                'title': title,
                'content': '',
                'error': error_msg
            }
        return {
            'title': title,
            'content': content,
            'error': ''
        }
    except requests.exceptions.RequestException as e:
        return {
            'title': '',
            'content': '',
            'error': f'기사 접근 중 오류 발생: {str(e)}'
        }
    except Exception as e:
        return {
            'title': '',
            'content': '',
            'error': f'기사 파싱 중 오류 발생: {str(e)}'
        } 