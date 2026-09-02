"""
Peak AI - Core Conversation Module
Handles all chat interactions and response routing
"""

import random
import json
import os
import re
from datetime import datetime
from math_ops import MathOperations
from graphics import GraphicsHandler
from utils import Utils

# Make turtle optional
try:
    from draw_turtle import TurtleDrawer
    TURTLE_AVAILABLE = True
except (ImportError, ModuleNotFoundError):
    TURTLE_AVAILABLE = False
    class TurtleDrawer:
        def __init__(self):
            self.turtle_available = False
            self.turtle_ready = False
        def draw(self, user_input):
            return "🎨 Turtle drawing is not available in this environment (requires GUI). Try using 'plot' or 'graph' commands instead!"

class PeakAI:
    """Main AI Assistant with conversation capabilities"""
    
    def __init__(self, name="Peak AI"):
        self.name = name
        self.version = "3.0"
        self.creator = "Peak Labs"
        self.conversation_history = []
        self.user_name = None
        self.user_mood = "neutral"
        self.memory = {}
        self.stats = {
            'math_problems_solved': 0,
            'jokes_told': 0,
            'graphs_drawn': 0,
            'conversations': 0,
            'web_searches': 0
        }
        
        # Initialize sub-modules
        self.math = MathOperations()
        self.graphics = GraphicsHandler()
        self.drawer = TurtleDrawer()
        self.utils = Utils()
        
    def greet(self):
        """Generate personalized greeting"""
        greetings = [
            f"⚡ Welcome to {self.name}! The most advanced AI assistant you'll ever meet!",
            f"🚀 {self.name} activated! Ready to revolutionize your coding experience!",
            f"💡 Hello! I'm {self.name}. I can do math, draw, analyze data, search the web, and chat!",
            f"🎯 Peak AI at your service! How can I help you reach new heights today?",
            f"🌟 {self.name} online! Let's create something amazing together!",
            f"🔥 Welcome! I'm {self.name}. I'm here to help you achieve peak performance!"
        ]
        return random.choice(greetings)
    
    def process_input(self, user_input):
        """Process user input with context awareness"""
        user_input = user_input.strip()
        
        # Save conversation history
        self.conversation_history.append(f"You: {user_input}")
        self.stats['conversations'] += 1
        
        # Analyze and respond
        response = self.analyze_and_respond(user_input)
        
        self.conversation_history.append(f"{self.name}: {response}")
        return response
    
    def analyze_and_respond(self, user_input):
        """Analyze input and route to appropriate handler"""
        lower_input = user_input.lower()
        
        # --- INTERNET COMMANDS - CHECK FIRST ---
        if lower_input.startswith('/internet'):
            return self.handle_internet_command(user_input)
        
        # --- System Commands ---
        if lower_input.startswith('/'):
            return self.handle_system_command(user_input)
        
        # --- Code Execution ---
        if lower_input.startswith('run '):
            return self.utils.execute_code(user_input[4:])
        
        # --- Internet Features ---
        
        # Web Search
        if lower_input.startswith('search ') or lower_input.startswith('google '):
            self.stats['web_searches'] += 1
            query = user_input[7:].strip() if lower_input.startswith('search ') else user_input[7:].strip()
            if not query:
                return "Please specify what you want to search for. Example: search python programming"
            results = self.utils.search_web(query)
            return self.utils.get_grounded_response(query, results)
        
        # Website Scraping
        if lower_input.startswith('scrape ') or lower_input.startswith('fetch '):
            parts = user_input.split(' ', 1)
            if len(parts) < 2:
                return "Please provide a URL to scrape. Example: scrape https://python.org"
            url = parts[1].strip()
            return self.utils.scrape_website(url)
        
        # --- WEATHER DETECTION (NEW) ---
        if "weather" in lower_input or "temperature" in lower_input:
            # Try to extract city
            city_match = re.search(r'weather in ([a-zA-Z\s]+?)(?:[?]|$)', lower_input)
            if city_match:
                city = city_match.group(1).strip()
                weather = self.utils.get_weather(city)
                if weather:
                    return weather
            # Fallback to search
            self.stats['web_searches'] += 1
            results = self.utils.search_web(user_input)
            return self.utils.get_grounded_response(user_input, results)
        
        # Check if user is asking about recent/current events (auto-search)
        if any(word in lower_input for word in ['current', 'recent', 'today', 'latest', 'news', 'update', 'what is']):
            if '?' in user_input or any(word in lower_input for word in ['what', 'who', 'when', 'where', 'why', 'how']):
                self.stats['web_searches'] += 1
                results = self.utils.search_web(user_input)
                return self.utils.get_grounded_response(user_input, results)
        
        # --- Conversation ---
        if "my name is" in lower_input or "call me" in lower_input:
            return self.handle_name(user_input)
        
        if "who am i" in lower_input:
            return self.handle_whoami()
        
        if any(word in lower_input for word in ["sad", "depressed", "down"]):
            self.user_mood = "sad"
            return "I'm sorry you're feeling down. Remember, tough times don't last! Can I tell you a joke or give you an inspiring quote? 💪"
        
        if any(word in lower_input for word in ["happy", "great", "wonderful"]):
            self.user_mood = "happy"
            return "That's fantastic! Your positive energy is contagious! Let's do something great together! 🚀"
        
        if any(word in lower_input for word in ["stressed", "anxious"]):
            self.user_mood = "stressed"
            return "Take a deep breath. You've got this! Let's break things down step by step. 🧘"
        
        if "how are you" in lower_input or "how's it going" in lower_input:
            moods = [
                "I'm operating at peak performance! How are you? ⚡",
                "Never better! Just processed 1M calculations! How about you? 🚀",
                "I'm fantastic! Ready to help you solve any problem! 💡"
            ]
            return random.choice(moods)
        
        if any(word in lower_input for word in ["what is love", "meaning of life"]):
            return self.handle_deep_questions(user_input)
        
        if any(word in lower_input for word in ["joke", "funny", "laugh"]):
            self.stats['jokes_told'] += 1
            return self.utils.tell_joke()
        
        if any(word in lower_input for word in ["quote", "inspiration", "motivation"]):
            return self.utils.get_quote()
        
        if "weather" in lower_input:
            return self.utils.simulate_weather()
        
        if any(word in lower_input for word in ["help", "what can you do"]):
            return self.show_help()
        
        if "status" in lower_input or "stats" in lower_input:
            return self.show_status()
        
        # --- Mathematics ---
        if any(op in lower_input for op in ['+', '-', '*', '/', '^', '%']):
            result = self.math.calculate_expression(user_input)
            self.stats['math_problems_solved'] += 1
            return result
        
        if "equation" in lower_input or "solve" in lower_input:
            return self.math.solve_equation(user_input)
        
        if "derivative" in lower_input:
            return self.math.calculate_derivative(user_input)
        
        if "integral" in lower_input:
            return self.math.calculate_integral(user_input)
        
        if "matrix" in lower_input:
            return self.math.handle_matrix(user_input)
        
        if any(word in lower_input for word in ["statistics", "stats", "analysis"]):
            return self.math.analyze_data(user_input)
        
        # --- Graphics ---
        if any(word in lower_input for word in ["plot", "graph", "chart", "visualize"]):
            self.stats['graphs_drawn'] += 1
            return self.graphics.create_plot(user_input)
        
        if "3d" in lower_input:
            return self.graphics.create_3d_plot(user_input)
        
        if any(word in lower_input for word in ["draw", "turtle", "shape"]):
            return self.drawer.draw(user_input)
        
        # --- Data Analysis ---
        if "data" in lower_input or "dataset" in lower_input:
            return self.math.analyze_dataset(user_input)
        
        # --- Default ---
        return self.default_response()
    
    def handle_name(self, user_input):
        """Handle name-related queries"""
        lower_input = user_input.lower()
        
        if "my name is" in lower_input:
            name_parts = lower_input.split("my name is")
            if len(name_parts) > 1:
                self.user_name = name_parts[1].strip().title()
                self.memory['user_name'] = self.user_name
                return f"✨ Wonderful to meet you, {self.user_name}! What brings you to Peak AI today?"
        
        if "call me" in lower_input:
            name_parts = lower_input.split("call me")
            if len(name_parts) > 1:
                self.user_name = name_parts[1].strip().title()
                self.memory['user_name'] = self.user_name
                return f"👋 Got it! I'll call you {self.user_name}. How can I help you?"
        
        return "I didn't catch that. Try saying 'my name is [your name]'"
    
    def handle_whoami(self):
        """Handle 'who am I' queries"""
        if self.user_name:
            return f"You are {self.user_name}! The amazing person using Peak AI! 💪"
        return "I don't know your name yet. Tell me 'my name is [your name]'"
    
    def handle_deep_questions(self, user_input):
        """Handle philosophical questions"""
        if "love" in user_input.lower():
            return "Love is a beautiful and complex concept! In my circuits, it's about helping others and making the world better. 💖"
        if "meaning" in user_input.lower():
            return "The meaning of life is what you make it! It's about learning, growing, and helping others. What does it mean to you? 🌟"
        return "That's a deep question! Let's explore it together. What do you think?"
    
    def handle_internet_command(self, command):
        """Handle internet-related commands"""
        cmd = command.lower().strip()
        
        if cmd == '/internet on':
            return self.utils.toggle_internet('on')
        elif cmd == '/internet off':
            return self.utils.toggle_internet('off')
        elif cmd == '/internet status':
            return self.utils.toggle_internet('status')
        elif cmd == '/internet':
            return self.utils.toggle_internet('status')
        else:
            return "Commands: /internet on, /internet off, /internet status"
    
    def handle_system_command(self, command):
        """Process system commands"""
        cmd = command.lower().strip()
        
        if cmd == '/status':
            return self.show_status()
        elif cmd == '/help':
            return self.show_help()
        elif cmd == '/clear':
            self.conversation_history = []
            return "🔄 Conversation history cleared!"
        elif cmd == '/stats':
            return self.show_stats()
        elif cmd.startswith('/save'):
            return self.save_conversation()
        elif cmd.startswith('/load'):
            return self.load_conversation()
        else:
            return f"Unknown command. Type /help for available commands."
    
    def show_stats(self):
        """Show usage statistics"""
        api_usage = self.utils.stats.get('api_usage', {})
        return f"""📊 Peak AI Statistics:
• Math problems solved: {self.stats['math_problems_solved']}
• Jokes told: {self.stats['jokes_told']}
• Graphs drawn: {self.stats['graphs_drawn']}
• Conversations: {self.stats['conversations']}
• Web searches: {self.stats['web_searches']}
• API usage: Tavily: {api_usage.get('tavily', 0)} | Qdrant: {api_usage.get('qdrant', 0)} | Weather: {api_usage.get('weather', 0)}
• User: {self.user_name or 'Not set'}"""
    
    def show_status(self):
        """Show detailed status"""
        internet_status = 'Enabled ✅' if self.utils.internet_enabled else 'Disabled ❌'
        tavily_status = 'Set ✅' if self.utils.tavily_api_key else 'Not set ❌'
        qdrant_status = 'Set ✅' if self.utils.qdrant_api_key else 'Not set ❌'
        
        return f"""
⚡ **Peak AI Status** ⚡
• Version: {self.version}
• Creator: {self.creator}
• Name: {self.name}
• Status: 🟢 Online & Ready
• User: {self.user_name or 'Not set'}
• Memory: {len(self.memory)} items
• Conversations: {len(self.conversation_history)} messages
• Internet: {internet_status}
• Tavily API: {tavily_status}
• Qdrant API: {qdrant_status}

📈 **Statistics:**
• Math Problems: {self.stats['math_problems_solved']}
• Jokes Told: {self.stats['jokes_told']}
• Graphs Drawn: {self.stats['graphs_drawn']}
• Web Searches: {self.stats['web_searches']}

**"Peak Performance Always!"** 🚀
"""
    
    def show_help(self):
        """Show help system with internet features"""
        return """
🤖 **Peak AI - Advanced Help System**

**🌐 Internet Features:**
• "search [query]" - Search the web
• "scrape [URL]" - Extract content from a website
• "what is the weather in [city]" - Get current weather
• "/internet on/off/status" - Control internet access

**🎯 Commands:**
• /status - Show AI status
• /stats - Show statistics
• /clear - Clear history
• /save - Save conversation
• /load - Load conversation

**💬 Conversation:**
• "my name is [name]" - Tell me your name
• "how are you?" - Ask how I'm doing
• "tell me a joke" - Hear a joke
• "give me a quote" - Get inspiration
• "what's the weather?" - Weather forecast

**🧮 Math:**
• "5 + 3", "10 * 4", "15 / 3"
• "sqrt(16)" - Square root
• "5!" - Factorial
• "is 17 prime?" - Prime check
• "analyze 5,10,15,20" - Data analysis

**📊 Graphics:**
• "plot sin" - Plot sine function
• "bar chart" - Create bar chart
• "pie chart" - Create pie chart
• "scatter" - Scatter plot

**🎨 Drawing:**
• "draw circle" - Draw with turtle
• "draw star" - Draw a star
• "draw spiral" - Draw a spiral
• "draw flower" - Draw a flower

Type naturally or use these commands! 🚀
"""
    
    def save_conversation(self):
        """Save conversation history"""
        try:
            data = {
                'history': self.conversation_history,
                'user_name': self.user_name,
                'memory': self.memory,
                'stats': self.stats
            }
            filename = f"peak_ai_conversation_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            with open(filename, 'w') as f:
                json.dump(data, f, indent=2)
            return f"✅ Conversation saved to {filename}"
        except Exception as e:
            return f"❌ Failed to save: {str(e)}"
    
    def load_conversation(self):
        """Load saved conversation"""
        try:
            files = [f for f in os.listdir() if f.startswith('peak_ai_conversation_')]
            if not files:
                return "❌ No saved conversations found."
            
            latest = sorted(files)[-1]
            with open(latest, 'r') as f:
                data = json.load(f)
            
            self.conversation_history = data.get('history', [])
            self.user_name = data.get('user_name')
            self.memory = data.get('memory', {})
            self.stats = data.get('stats', self.stats)
            
            return f"✅ Conversation loaded from {latest}"
        except Exception as e:
            return f"❌ Failed to load: {str(e)}"
    
    def default_response(self):
        """Default response when unsure"""
        responses = [
            "I'm not sure I understand. Could you rephrase that? 🤔",
            "Interesting! Can you tell me more?",
            "I'm still learning. Could you explain differently?",
            "I don't quite get it. Try asking about math, graphics, or try a web search with 'search [query]'!",
            "Hmm, that's new! Try 'search [your question]' to search the web.",
            "Could you be more specific? I want to help!"
        ]
        return random.choice(responses)
    
    def chat(self):
        """Main chat loop"""
        print("=" * 80)
        print(f"⚡ {self.name} - The Ultimate AI Assistant")
        print("=" * 80)
        print(f"\n{self.greet()}")
        print("\n💡 Type 'help' to see what I can do.")
        print("💡 Type 'bye' to exit.")
        print("💡 Type '/status' for stats.")
        print("💡 Type 'search [query]' to search the web!")
        print("💡 Type 'weather in [city]' for weather!")
        print("💡 Type '/internet status' to check internet access")
        print("\n" + "=" * 80)
        
        while True:
            user_input = input("\n👤 You: ").strip()
            
            if not user_input:
                continue
            
            if user_input.lower() in ['bye', 'goodbye', 'exit', 'quit']:
                farewells = [
                    "Goodbye! Come back anytime! 🌟",
                    "See you later! Have a wonderful day! 🚀",
                    "Bye! Keep learning and exploring! 📚",
                    "Take care! Nice chatting with you! 😊",
                    "Peak AI signing off! Remember, you're awesome! 🎯"
                ]
                print(f"\n🤖 {self.name}: {random.choice(farewells)}")
                break
            
            response = self.process_input(user_input)
            print(f"\n🤖 {self.name}: {response}")
