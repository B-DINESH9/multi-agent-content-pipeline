import requests
from bs4 import BeautifulSoup
from crewai.tools import BaseTool
from duckduckgo_search import DDGS

class ImageSearchTool(BaseTool):
    name: str = "image_search_tool"
    description: str = (
        "Search the internet for an image related to a specific query. "
        "Use this tool when you need to include a visual representation, figure, or map in the report. "
        "It returns a direct URL to the image, which you must embed in the Markdown using the syntax: "
        "![Description](image_url)"
    )

    def _run(self, query: str) -> str:
        """Search for an image using DuckDuckGo."""
        try:
            results = DDGS().images(query, max_results=1)
            if results and len(results) > 0:
                image_url = results[0].get('image')
                if image_url:
                    return f"Found image URL: {image_url} (Embed this using Markdown: ![alt text]({image_url}))"
            return "No images found for this query. Do not include an image in the report."
        except Exception as e:
            return f"Error searching for images: {e}"

class WebSearchTool(BaseTool):
    name: str = "web_search_tool"
    description: str = (
        "Search the internet for information on a given topic. "
        "Use this tool to find facts, articles, and references."
    )

    def _run(self, query: str) -> str:
        """Search for text results using DuckDuckGo."""
        try:
            results = DDGS().text(query, max_results=5)
            if not results:
                return "No results found."
            
            output = []
            for r in results:
                output.append(f"Title: {r.get('title')}\nURL: {r.get('href')}\nSnippet: {r.get('body')}\n---")
            return "\n".join(output)
        except Exception as e:
            return f"Error performing web search: {e}"

class WebsiteScraperTool(BaseTool):
    name: str = "website_scraper_tool"
    description: str = (
        "Scrape text content from a specific website URL. "
        "Pass the exact URL to scrape. Returns a maximum of 2000 characters to conserve AI context limits."
    )

    def _run(self, url: str) -> str:
        try:
            headers = {'User-Agent': 'Mozilla/5.0'}
            response = requests.get(url, headers=headers, timeout=10)
            response.raise_for_status()
            soup = BeautifulSoup(response.content, 'html.parser')
            text = soup.get_text(separator=' ', strip=True)
            # Truncate to 2000 chars to avoid blowing up Groq's small free-tier token limits
            return text[:2000] + "\n...[Truncated to conserve tokens]"
        except Exception as e:
            return f"Failed to scrape {url}: {str(e)}"
