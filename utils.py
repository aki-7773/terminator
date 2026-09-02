"""
Peak AI - Utilities Module
Multi-API support: Tavily (web search), Qdrant (vector DB), Weather (free)
"""

import random
import requests
import os
import re
import time
import json
from datetime import datetime

class Utils:
    """Utility functions with multiple API support"""
    
    def __init__(self):
        # Internet search configuration
        self.internet_enabled = True
        
        # ---- TAVILY API (Web Search) ----
        self.tavily_api_key = os.getenv('TAVILY_API_KEY', '')
        self.tavily_api_url = 'https://api.tavily.com/search'
        
        # ---- QDRANT API (Vector Database) ----
        self.qdrant_api_key = os.getenv('QDRANT_API_KEY', '')
        self.qdrant_url = os.getenv('QDRANT_URL', '')
        self.qdrant_collection = os.getenv('QDRANT_COLLECTION', 'terminator_knowledge')
        
        # ---- Weather API (free) ----
        self.weather_enabled = True
        
        # ---- Status tracking ----
        self.api_status = {
            'tavily': bool(self.tavily_api_key),
            'qdrant': bool(self.qdrant_api_key and self.qdrant_url),
            'weather': True
        }
        
        # Statistics tracking
        self.stats = {
            'api_usage': {
                'tavily': 0,
                'qdrant': 0,
                'weather': 0
            }
        }
        
    # ============================================
    # TAVILY API - Web Search
    # ============================================
    
    def search_tavily(self, query):
        """
        Search using Tavily API (1k free credits/month)
        """
        if not self.tavily_api_key:
            return None
        
        try:
            response = requests.post(
                self.tavily_api_url,
                headers={
                    'Authorization': f'Bearer {self.tavily_api_key}',
                    'Content-Type': 'application/json'
                },
                json={
                    'query': query,
                    'search_depth': 'basic',  # Use 'basic' to save credits
                    'include_answer': True,
                    'include_images': False,
                    'max_results': 5
                },
                timeout=15
            )
            
            if response.status_code == 200:
                data = response.json()
                results = data.get('results', [])
                
                if results:
                    formatted = []
                    
                    # Add the answer if available
                    if data.get('answer'):
                        formatted.append(f"💡 **Summary:** {data['answer']}\n")
                    
                    # Add search results
                    for r in results[:3]:
                        formatted.append(
                            f"📌 {r.get('title', 'No title')}\n"
                            f"📝 {r.get('content', 'No description')[:300]}...\n"
                            f"🔗 Source: {r.get('url', 'No link')}\n"
                        )
                    
                    self.stats['api_usage']['tavily'] += 1
                    return '\n'.join(formatted)
                else:
                    return "No results found on Tavily."
            else:
                return f"Tavily API error: {response.status_code}"
                
        except Exception as e:
            return f"Tavily search failed: {str(e)}"
    
    # ============================================
    # QDRANT API - Vector Database
    # ============================================
    
    def search_qdrant(self, query):
        """
        Search Qdrant vector database for similar stored information
        """
        if not self.qdrant_api_key or not self.qdrant_url:
            return None
        
        try:
            # Simple keyword search (for demo - in production use embeddings)
            response = requests.post(
                f"{self.qdrant_url}/collections/{self.qdrant_collection}/points/search",
                headers={
                    'api-key': self.qdrant_api_key,
                    'Content-Type': 'application/json'
                },
                json={
                    'limit': 3,
                    # In production, add vector search here
                    # 'vector': embedding,
                    'filter': {
                        'must': [
                            {
                                'key': 'text',
                                'match': {
                                    'text': query
                                }
                            }
                        ]
                    }
                },
                timeout=10
            )
            
            if response.status_code == 200:
                data = response.json()
                results = data.get('result', [])
                
                if results:
                    formatted = ["📚 **Stored Knowledge from Qdrant:**\n"]
                    for i, point in enumerate(results[:3], 1):
                        payload = point.get('payload', {})
                        text = payload.get('text', 'No content')
                        source = payload.get('source', 'Unknown')
                        formatted.append(
                            f"{i}. {text[:300]}...\n"
                            f"   📎 Source: {source}\n"
                        )
                    self.stats['api_usage']['qdrant'] += 1
                    return '\n'.join(formatted)
            
            return None
            
        except Exception as e:
            return f"Qdrant search failed: {str(e)}"
    
    def store_in_qdrant(self, text, metadata=None):
        """
        Store text in Qdrant for future retrieval
        """
        if not self.qdrant_api_key or not self.qdrant_url:
            return "Qdrant not configured"
        
        try:
            # In production, you'd generate an embedding
            response = requests.put(
                f"{self.qdrant_url}/collections/{self.qdrant_collection}/points",
                headers={
                    'api-key': self.qdrant_api_key,
                    'Content-Type': 'application/json'
                },
                json={
                    'points': [
                        {
                            'id': int(time.time() * 1000),
                            'payload': {
                                'text': text,
                                'source': metadata.get('source', 'user_input'),
                                'timestamp': datetime.now().isoformat(),
                                **metadata
                            }
                        }
                    ]
                },
                timeout=10
            )
            
            if response.status_code in [200, 201]:
                return "✅ Stored in Qdrant!"
            else:
                return f"Qdrant store failed: {response.status_code}"
                
        except Exception as e:
            return f"Qdrant store failed: {str(e)}"
    
    # ============================================
    # WEATHER API (Free, no key needed)
    # ============================================
    
    def get_weather(self, city):
        """
        Get weather using wttr.in (free, no API key)
        """
        if not self.weather_enabled:
            return None
        
        try:
            # Clean city name
            city_clean = city.strip().replace(' ', '+')
            response = requests.get(
                f'https://wttr.in/{city_clean}?format=%l:+%c+%t+%w+%h',
                timeout=10,
                headers={'User-Agent': 'TerminatorAI/1.0'}
            )
            
            if response.status_code == 200:
                weather_text = response.text.strip()
                if 'error' not in weather_text.lower() and weather_text:
                    self.stats['api_usage']['weather'] += 1
                    return f"🌤️ **Weather:** {weather_text}"
            
            return None
        except:
            return None
    
    # ============================================
    # MAIN SEARCH FUNCTION (Combines all APIs)
    # ============================================
    
    def search_web(self, query):
        """
        Search using multiple APIs in priority order:
        1. Tavily (best quality, limited credits)
        2. Qdrant (stored knowledge)
        3. Weather (if weather-related)
        4. Fallback (DuckDuckGo)
        """
        if not self.internet_enabled:
            return "Internet access is disabled. Enable it with '/internet on'"
        
        # ---- TRY 1: TAVILY API ----
        if self.api_status['tavily']:
            result = self.search_tavily(query)
            if result and "error" not in result.lower() and "No results" not in result:
                return result
        
        # ---- TRY 2: QDRANT ----
        if self.api_status['qdrant']:
            result = self.search_qdrant(query)
            if result and "failed" not in result.lower():
                return result
        
        # ---- TRY 3: WEATHER (if weather-related) ----
        if 'weather' in query.lower() or 'temperature' in query.lower():
            import re
            city_match = re.search(r'weather in ([a-zA-Z\s]+?)(?:[?]|$)', query.lower())
            if city_match:
                city = city_match.group(1).strip()
                weather = self.get_weather(city)
                if weather:
                    return weather + "\n\n💡 Weather data from wttr.in"
        
        # ---- TRY 4: FALLBACK SEARCH ----
        return self._fallback_search(query)
    
    def _fallback_search(self, query):
        """
        Fallback search using DuckDuckGo
        """
        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9',
                'DNT': '1'
            }
            
            response = requests.get(
                'https://html.duckduckgo.com/html/',
                params={'q': query},
                headers=headers,
                timeout=15
            )
            
            if response.status_code == 200:
                results = []
                title_pattern = r'<a[^>]*class="result__a"[^>]*href="([^"]*)"[^>]*>(.*?)</a>'
                titles = re.findall(title_pattern, response.text, re.DOTALL)
                
                for url, title in titles[:3]:
                    clean_title = re.sub(r'<[^>]+>', '', title).strip()
                    if clean_title and '...' not in clean_title:
                        results.append(f"📌 {clean_title}\n🔗 {url}")
                
                if results:
                    return '\n\n'.join(results[:3])
            
            return self._get_fallback_response(query)
            
        except Exception as e:
            return self._get_fallback_response(query)
    
    def _get_fallback_response(self, query):
        """Return helpful message when all search fails"""
        responses = [
            f"I couldn't search for '{query}'. The search services are temporarily unavailable.\n\n💡 **Try:**\n• Use 'scrape [URL]' for specific websites\n• Ask about math, plotting, or general questions\n• Try again later",
            
            f"Search is currently unavailable. Please try a different approach or ask me something else!",
            
            f"I'm having trouble connecting to search services. You can still ask me math questions, plot graphs, or chat with me!"
        ]
        return random.choice(responses)
    
    def get_grounded_response(self, question, search_results):
        """Format search results"""
        if not search_results or "couldn't search" in search_results.lower():
            return f"🌐 I couldn't find information on '{question}'. Please try a different search term!"
        
        return f"🔍 **Search Results for: '{question}'**\n\n{search_results}\n\n💡 You can ask me specific questions about these results!"
    
    def scrape_website(self, url):
        """
        Scrape a website for content
        """
        try:
            # Check for beautifulsoup
            try:
                from bs4 import BeautifulSoup
            except ImportError:
                return "BeautifulSoup not installed. Install with: pip install beautifulsoup4"
            
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
        """Simulate weather for different cities (fallback)"""
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
            return f"🌐 Internet access: {'Enabled' if self.internet_enabled else 'Disabled'}\n🔑 API Keys: Tavily: {'Set ✅' if self.tavily_api_key else 'Not set ❌'} | Qdrant: {'Set ✅' if self.qdrant_api_key else 'Not set ❌'}"
