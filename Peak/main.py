"""
Peak AI - Main Entry Point
The Ultimate AI Assistant
"""

from chat import PeakAI

def main():
    """Start the Peak AI chatbot"""
    print("=" * 80)
    print("🚀 Starting Peak AI...")
    print("=" * 80)
    
    # Create and start the chatbot
    bot = PeakAI("Peak AI")
    bot.chat()

if __name__ == "__main__":
    main()