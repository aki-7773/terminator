"""
Peak AI - Turtle Drawing Module
Handles all turtle graphics (web-safe version)
"""

import re

class TurtleDrawer:
    """Handles all turtle drawings - web-safe version"""
    
    def __init__(self):
        self.turtle_ready = False
        self.turtle_available = False
        
        # Try to import turtle only if available
        try:
            import turtle
            self.turtle = turtle
            self.turtle_available = True
            self.turtle_ready = True
        except ImportError:
            # Turtle not available (e.g., on Render)
            self.turtle_available = False
            self.turtle_ready = False
    
    def draw(self, user_input):
        """Draw various shapes with turtle (if available)"""
        if not self.turtle_available:
            return "🎨 Turtle drawing is not available in this environment (requires GUI). Try using 'plot' or 'graph' commands instead!"
        
        try:
            t = self.turtle.Turtle()
            t.speed(3)
            t.pensize(2)
            lower_input = user_input.lower()
            
            if "circle" in lower_input:
                return self.draw_circle(t, user_input)
            elif "square" in lower_input:
                return self.draw_square(t, user_input)
            elif "triangle" in lower_input:
                return self.draw_triangle(t, user_input)
            elif "star" in lower_input:
                return self.draw_star(t)
            elif "spiral" in lower_input:
                return self.draw_spiral(t)
            elif "house" in lower_input:
                return self.draw_house(t)
            elif "flower" in lower_input:
                return self.draw_flower(t)
            elif "mandala" in lower_input:
                return self.draw_mandala(t)
            elif "hexagon" in lower_input:
                return self.draw_hexagon(t, user_input)
            else:
                return self.draw_pattern(t)
                
        except Exception as e:
            return f"Sorry, couldn't draw that: {str(e)}"
    
    def draw_circle(self, t, user_input):
        """Draw a circle"""
        numbers = re.findall(r'\d+', user_input)
        radius = int(numbers[0]) if numbers else 100
        t.fillcolor("blue")
        t.begin_fill()
        t.circle(radius)
        t.end_fill()
        self.turtle.done()
        return f"✅ Circle with radius {radius}!"
    
    def draw_square(self, t, user_input):
        """Draw a square"""
        numbers = re.findall(r'\d+', user_input)
        side = int(numbers[0]) if numbers else 100
        t.fillcolor("red")
        t.begin_fill()
        for _ in range(4):
            t.forward(side)
            t.right(90)
        t.end_fill()
        self.turtle.done()
        return f"✅ Square with side {side}!"
    
    def draw_triangle(self, t, user_input):
        """Draw a triangle"""
        numbers = re.findall(r'\d+', user_input)
        side = int(numbers[0]) if numbers else 100
        t.fillcolor("green")
        t.begin_fill()
        for _ in range(3):
            t.forward(side)
            t.right(120)
        t.end_fill()
        self.turtle.done()
        return f"✅ Triangle with side {side}!"
    
    def draw_star(self, t):
        """Draw a star"""
        t.fillcolor("gold")
        t.begin_fill()
        for _ in range(5):
            t.forward(100)
            t.right(144)
        t.end_fill()
        self.turtle.done()
        return "✅ Star drawn! ✨"
    
    def draw_spiral(self, t):
        """Draw a spiral"""
        for i in range(50):
            t.forward(i * 2)
            t.right(91)
        self.turtle.done()
        return "✅ Spiral drawn!"
    
    def draw_house(self, t):
        """Draw a house"""
        # House body
        t.fillcolor("yellow")
        t.begin_fill()
        for _ in range(4):
            t.forward(100)
            t.right(90)
        t.end_fill()
        
        # Roof
        t.goto(0, 100)
        t.fillcolor("red")
        t.begin_fill()
        t.goto(50, 150)
        t.goto(100, 100)
        t.end_fill()
        
        self.turtle.done()
        return "✅ House drawn! 🏠"
    
    def draw_flower(self, t):
        """Draw a flower"""
        colors = ["red", "blue", "green", "yellow", "purple", "orange"]
        for i in range(36):
            t.color(colors[i % 6])
            t.forward(100)
            t.right(170)
        self.turtle.done()
        return "✅ Flower drawn! 🌸"
    
    def draw_mandala(self, t):
        """Draw a mandala pattern"""
        colors = ["red", "blue", "green", "yellow", "purple", "orange"]
        for i in range(36):
            t.color(colors[i % 6])
            t.forward(100)
            t.right(170)
            t.forward(50)
            t.right(190)
        self.turtle.done()
        return "✅ Mandala drawn! 🎨"
    
    def draw_hexagon(self, t, user_input):
        """Draw a hexagon"""
        numbers = re.findall(r'\d+', user_input)
        side = int(numbers[0]) if numbers else 80
        t.fillcolor("purple")
        t.begin_fill()
        for _ in range(6):
            t.forward(side)
            t.right(60)
        t.end_fill()
        self.turtle.done()
        return f"✅ Hexagon with side {side}!"
    
    def draw_pattern(self, t):
        """Draw an abstract pattern"""
        colors = ["red", "blue", "green", "yellow", "purple", "orange"]
        for i in range(36):
            t.color(colors[i % 6])
            t.forward(100)
            t.right(170)
        self.turtle.done()
        return "✅ Abstract pattern drawn!"
