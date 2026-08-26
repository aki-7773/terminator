"""
Peak AI - Utilities Module
Helper functions for various tasks including web search
"""

import random
import requests
from datetime import datetime
import os
import re

class Utils:
    """Utility functions for the AI assistant"""
    
    def __init__(self):
        # Internet search configuration
        self.internet_enabled = True
        self.search_api_key = os.getenv('SEARCH_API_KEY', '')
        self.search_api_url = os.getenv('SEARCH_API_URL', 'https://api.scavio.dev/api/v1/search')
        self.use_fallback_search = True if not self.search_api_key else False
        
    def execute_code(self, code):
        """Execute simple Python code (Caution: Security risk!)"""
        try:
            # Security check
            forbidden = ['import', 'open', 'file', 'system', 'exec', 'eval']
            if any(keyword in code for keyword in forbidden):
                return "⚠️ Security restriction: Unsafe code detected."
            
            result = eval(code)
            return f"✅ Result: {result}"
        except Exception as e:
            return f"❌ Error: {str(e)}"
    
    def search_web(self, query):
        """
        Search the web for current information
        Returns formatted search results as string
        """
        if not self.internet_enabled:
            return "Internet access is disabled. Enable it with '/internet on'"
        
        # Try API search first
        if self.search_api_key:
            try:
                response = requests.post(
                    self.search_api_url,
                    headers={
                        'x-api-key': self.search_api_key,
                        'Content-Type': 'application/json'
                    },
                    json={'query': query, 'country_code': 'us'},
                    timeout=10
                )
                
                if response.status_code == 200:
                    results = response.json().get('organic_results', [])[:5]
                    if results:
                        formatted = []
                        for r in results:
                            formatted.append(
                                f"📌 {r.get('title', 'No title')}\n"
                                f"📝 {r.get('snippet', 'No description')}\n"
                                f"🔗 Source: {r.get('link', 'No link')}\n"
                            )
                        return '\n'.join(formatted)
                    else:
                        return "No search results found. Try a different query."
                else:
                    return f"Search API error: {response.status_code}. Using fallback search..."
            except Exception as e:
                return f"Search failed: {str(e)}. Using fallback search..."
        
        # Fallback: Use a different approach
        return self._fallback_search(query)
    
    def _fallback_search(self, query):
        """
        Fallback search using DuckDuckGo HTML (no API key required)
        This is a simpler approach that actually works
        """
        try:
            # Use DuckDuckGo's HTML interface
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
            }
            
            response = requests.get(
                'https://html.duckduckgo.com/html/',
                params={'q': query},
                headers=headers,
                timeout=10
            )
            
            if response.status_code == 200:
                # Extract results using regex (simpler than BeautifulSoup)
                results = []
                
                # Find result titles and URLs using regex
                title_pattern = r'<a[^>]*class="result__a"[^>]*href="([^"]*)"[^>]*>(.*?)</a>'
                snippet_pattern = r'<a[^>]*class="result__snippet"[^>]*>(.*?)</a>'
                
                # Try to find titles
                titles = re.findall(title_pattern, response.text, re.DOTALL)
                
                # Clean up titles (remove HTML tags)
                for url, title in titles[:3]:
                    # Clean the title
                    clean_title = re.sub(r'<[^>]+>', '', title).strip()
                    if clean_title and '...' not in clean_title:
                        results.append(f"📌 {clean_title}\n🔗 {url}")
                
                # If no results with regex, try a simpler approach
                if not results:
                    # Look for any links that look like search results
                    link_pattern = r'<a[^>]*href="([^"]*)"[^>]*>([^<]*)</a>'
                    all_links = re.findall(link_pattern, response.text)
                    
                    for url, text in all_links[:5]:
                        if 'duckduckgo.com' not in url and text and len(text) > 10:
                            if 'http' in url or url.startswith('/'):
                                results.append(f"📌 {text.strip()}\n🔗 {url}")
                
                if results:
                    return '\n\n'.join(results[:3])
                
                # If still no results, try another approach
                return self._fallback_search_alternative(query)
            else:
                return f"Fallback search failed with status: {response.status_code}"
        except Exception as e:
            return f"Fallback search error: {str(e)}"
    
    def _fallback_search_alternative(self, query):
        """
        Another fallback approach using a different search endpoint
        """
        try:
            # Try using a different DuckDuckGo endpoint
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }
            
            # Use the lite version with different parameters
            response = requests.get(
                'https://lite.duckduckgo.com/lite/',
                params={'q': query, 'o': 'json'},
                headers=headers,
                timeout=10
            )
            
            if response.status_code == 200:
                # Look for result links
                results = []
                lines = response.text.split('\n')
                
                for line in lines:
                    if 'href="' in line and 'result' in line.lower():
                        # Try to extract a result
                        link_match = re.search(r'href="([^"]*)"', line)
                        text_match = re.search(r'>([^<]*)</a>', line)
                        
                        if link_match and text_match:
                            link = link_match.group(1)
                            text = text_match.group(1).strip()
                            if text and len(text) > 5 and 'duckduckgo' not in link:
                                results.append(f"📌 {text}\n🔗 {link}")
                
                if results:
                    return '\n\n'.join(results[:3])
            
            # If everything fails, return a helpful message
            return self._get_fallback_response(query)
            
        except Exception as e:
            return self._get_fallback_response(query)
    
    def _get_fallback_response(self, query):
        """
        Return a helpful response when search fails
        """
        responses = [
            f"I couldn't search for '{query}' right now. The search service is temporarily unavailable.",
            f"I had trouble searching for '{query}'. Please try again later or try a different query.",
            f"Search is currently not working for '{query}'. You can try asking me something else, or check your internet connection.",
            f"I can't access search results for '{query}' at the moment. Try using the 'scrape' command with a specific URL instead."
        ]
        return random.choice(responses)
    
    def get_grounded_response(self, question, search_results):
        """
        Generate a response grounded in search results
        """
        if not search_results:
            return f"🌐 I couldn't find any information on '{question}'. Please try a different search term!"
        
        if "couldn't search" in search_results.lower() or "unavailable" in search_results.lower() or "not working" in search_results.lower():
            return f"🔍 {search_results}\n\n💡 You can also try using 'scrape [URL]' to get information from a specific website."
        
        if "No search results" in search_results:
            return f"🔍 No search results found for '{question}'. Try being more specific or using different keywords."
        
        return f"🔍 **Search Results for: '{question}'**\n\n{search_results}\n\n💡 Based on these results, you can ask me specific questions about them!"
    
    def scrape_website(self, url):
        """
        Scrape a website for content
        """
        try:
            # First check if beautifulsoup is installed
            try:
                from bs4 import BeautifulSoup
            except ImportError:
                return "BeautifulSoup not installed. Install with: pip install beautifulsoup4\n\nThen try again."
            
            response = requests.get(
                url, 
                timeout=15, 
                headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
            )
            
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'html.parser')
                
                # Remove script and style tags
                for script in soup(["script", "style"]):
                    script.decompose()
                
                # Get text
                text = soup.get_text(separator='\n', strip=True)
                text = '\n'.join(line for line in text.split('\n') if line)
                
                # Return first 1500 characters
                if len(text) > 1500:
                    text = text[:1500] + '\n... (truncated)'
                
                return f"📄 **Content from {url}**\n\n{text}"
            else:
                return f"Failed to fetch {url}: Status {response.status_code}"
        except Exception as e:
            return f"Error fetching website: {str(e)}"
    
    def tell_joke(self):
        """Return a random joke"""
        jokes = [
            "Why don't scientists trust atoms? They make up everything! 😂",
            "What do you call a bear with no teeth? A gummy bear! 🐻",
            "Why did the math book look so sad? Too many problems! 📚",
            "What's the best thing about Switzerland? The flag is a big plus! 🇨🇭",
            "Why did the computer go to the doctor? It had a virus! 🖥️",
            "How do you make a tissue dance? Put a little boogie in it! 💃",
            "What do you call a fake noodle? An impasta! 🍝",
            "Why was the math student late? He took the rhombus! 🚌",
            "What do you call a sleeping dinosaur? A dino-snore! 🦕",
            "Why don't skeletons fight? They don't have the guts! 💀",
            "What did zero say to eight? Nice belt! 0️⃣➡️8️⃣",
            "Why is six afraid of seven? Because seven ate nine! 6️⃣7️⃣9️⃣"
        ]
        return random.choice(jokes)
    
    def get_quote(self):
        """Return an inspiring quote"""
        quotes = [
            "The only way to do great work is to love what you do. - Steve Jobs",
            "In the middle of difficulty lies opportunity. - Albert Einstein",
            "The future belongs to those who believe in their dreams. - Eleanor Roosevelt",
            "Success is not final, failure is not fatal: it is courage that counts. - Winston Churchill",
            "Mathematics is the music of reason. - James Joseph Sylvester",
            "The best way to predict the future is to create it. - Peter Drucker",
            "Life is 10% what happens and 90% how you react. - Charles R. Swindoll",
            "Innovation distinguishes leaders from followers. - Steve Jobs",
            "To be yourself in a changing world is the greatest accomplishment. - Ralph Waldo Emerson",
            "The greatest glory is not in never falling, but in rising every time we fall. - Nelson Mandela"
        ]
        return "💡 " + random.choice(quotes)
    
    def simulate_weather(self):
        """Simulate weather for different cities"""
        cities = ["Berlin", "Munich", "Hamburg", "Cologne", "Frankfurt", "London", "Paris", "Vienna"]
        weather = ["sunny ☀️", "partly cloudy ⛅", "cloudy ☁️", "rainy 🌧️", "windy 💨", "snowy ❄️"]
        temps = [5, 10, 12, 15, 18, 20, 22, 25, 28, 30]
        
        city = random.choice(cities)
        return f"📍 {city}: {random.choice(weather)}, {random.choice(temps)}°C"
    
    def get_time(self):
        """Get current time"""
        now = datetime.now()
        return now.strftime('%H:%M:%S')
    
    def get_date(self):
        """Get current date"""
        now = datetime.now()
        return now.strftime('%B %d, %Y')
    
    def toggle_internet(self, status):
        """Enable or disable internet access"""
        if status == 'on':
            self.internet_enabled = True
            return "🌐 Internet access enabled! I can now search the web for you."
        elif status == 'off':
            self.internet_enabled = False
            return "🚫 Internet access disabled. I'll only use my training data."
        else:
            return f"🌐 Internet access: {'Enabled' if self.internet_enabled else 'Disabled'}\n🔑 API Key: {'Set' if self.search_api_key else 'Not set'}"