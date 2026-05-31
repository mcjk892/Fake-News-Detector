from bs4 import BeautifulSoup
from duckduckgo_search import DDGS
import os
from dotenv import load_dotenv
from groq import Groq
import requests

load_dotenv()

class NewsResearcher:
    def __init__(self):
        self.api_key = os.getenv("GROK_API_KEY")
        if self.api_key:
            self.api_key = self.api_key.strip("'\"")
        self.client = Groq(api_key=self.api_key) if self.api_key else None
        
        # Google Custom Search API configuration (Optional)
        self.google_api_key = os.getenv("GOOGLE_SEARCH_API_KEY")
        if self.google_api_key:
            self.google_api_key = self.google_api_key.strip("'\"")
        self.google_cse_id = os.getenv("GOOGLE_CSE_ID")
        if self.google_cse_id:
            self.google_cse_id = self.google_cse_id.strip("'\"")

    def get_search_results(self, query):
        """Perform search across Google Custom Search (if configured) or DuckDuckGo."""
        results = []
        
        # 1. Try Google Custom Search if API Key and CSE ID are provided
        if self.google_api_key and self.google_cse_id:
            try:
                print(f"Searching Google for: '{query}'")
                url = "https://www.googleapis.com/customsearch/v1"
                params = {
                    "q": query,
                    "key": self.google_api_key,
                    "cx": self.google_cse_id,
                    "num": 5
                }
                response = requests.get(url, params=params, timeout=10)
                if response.status_code == 200:
                    data = response.json()
                    items = data.get("items", [])
                    for item in items:
                        link = item.get("link")
                        if link:
                            results.append(link)
                    if results:
                        print(f"Google Search succeeded. Found {len(results)} results.")
                        return results
                else:
                    print(f"Google Search API returned status code {response.status_code}: {response.text}")
            except Exception as e:
                print(f"Google Search error: {e}")
        
        # 2. Fallback to DuckDuckGo search
        try:
            print(f"Searching DuckDuckGo for: '{query}'")
            with DDGS() as ddgs:
                ddgs_results = ddgs.text(query, max_results=5, backend='html')
                for r in ddgs_results:
                    results.append(r['href'])
            print(f"DuckDuckGo Search succeeded. Found {len(results)} results.")
        except Exception as e:
            print(f"DuckDuckGo Search error: {e}")
            
        return results

    def scrape_url(self, url):
        """Scrape content from a URL."""
        try:
            headers = {'User-Agent': 'Mozilla/5.0'}
            response = requests.get(url, headers=headers, timeout=10)
            soup = BeautifulSoup(response.text, 'html.parser')
            # Extract text from paragraphs
            paragraphs = soup.find_all('p')
            content = " ".join([p.get_text() for p in paragraphs[:5]]) # Get first 5 paragraphs
            return content[:1000] # Limit to 1000 chars
        except Exception as e:
            print(f"Scrape error for {url}: {e}")
            return ""

    def analyze(self, input_data):
        """
        Analyze text or link.
        Returns: { 'verdict': 'True'/'False'/'Uncertain', 'explanation': '...', 'right_answer': '...', 'sources': [...] }
        """
        is_url = input_data.startswith("http")
        query = input_data
        
        content = ""
        if is_url:
            # If it's a URL, try to get the content first
            content = self.scrape_url(input_data)
            # Use query for search if it's a link
            query = content[:200] if content else input_data

        # 1. Search for the topic
        search_urls = self.get_search_results(query)
        
        # 2. Research Conclusion
        if not self.api_key:
            # If no API key, let's at least show the search results clearly
            verdict = "Researching"
            explanation = "I found several sources related to this query. Please see the sources list below for details."
            if not search_urls:
                explanation = "No direct search results found. This could be a very recent or very specific claim."
            
            return {
                "verdict": "Analyzing...",
                "explanation": explanation,
                "right_answer": "Add your API key (GROK_API_KEY) in the .env file to get a definitive AI-powered verdict and fact-check.",
                "sources": search_urls
            }
        
        # 3. AI Powered Analysis (Using User's Specific Model & Client)
        try:
            if not self.client:
                return {"verdict": "Error", "explanation": "API client not initialized. Check your .env file.", "right_answer": "Add GROK_API_KEY to .env", "sources": search_urls}

            # Prepare search results for the LLM
            search_info = ""
            for i, url in enumerate(search_urls[:3]):
                snippet = self.scrape_url(url)
                search_info += f"Source {i+1} ({url}): {snippet}\n\n"

            prompt = f"""
            Analyze the following news claim or link content.
            Claim/Content: {input_data}
            
            Web Search Results:
            {search_info}
            
            Please provide:
            1. Verdict (True, False, or Uncertain)
            2. Concise Explanation (Why is it true/false based on search results?)
            3. The Right Answer (Fact-check correction)
            
            Return ONLY a JSON object with:
            {{ "verdict": "...", "explanation": "...", "right_answer": "..." }}
            """
            
            # Using user's specific model and client structure
            completion = self.client.chat.completions.create(
                model="openai/gpt-oss-120b",
                messages=[
                    {"role": "system", "content": "You are an expert fact-checker. You MUST NOT use or invoke any external tools, functions, or search commands. You do not have access to any tools (like web.run). Respond ONLY with a raw JSON object containing the verdict, explanation, and right_answer using the provided web search results."},
                    {"role": "user", "content": prompt}
                ],
                temperature=1,
                max_completion_tokens=1024,
                top_p=1,
                reasoning_effort="medium",
                stream=False
            )
            
            ai_data = completion.choices[0].message.content
            print(f"AI Response: {ai_data}")
            
            import json
            import re
            match = re.search(r'\{.*\}', ai_data, re.DOTALL)
            if match:
                result = json.loads(match.group())
                result['sources'] = search_urls
                return result
            
            return {
                "verdict": "Parse Error",
                "explanation": "Could not parse AI response",
                "right_answer": ai_data[:500],
                "sources": search_urls
            }

        except Exception as e:
            print(f"Analysis error: {e}")
            return {
                "verdict": "System Error",
                "explanation": str(e),
                "right_answer": "Something went wrong in the research engine.",
                "sources": search_urls
            }

researcher = NewsResearcher()
