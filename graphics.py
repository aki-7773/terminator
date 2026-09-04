"""
Peak AI - Graphics Module
Handles all plotting and visualization
"""

import re
import numpy as np
import matplotlib
matplotlib.use('Agg')  # Ensure headless backend
import matplotlib.pyplot as plt

class GraphicsHandler:
    """Handles all graphics and visualization"""
    
    def __init__(self):
        self.plot_ready = True
    
    def create_plot(self, user_input):
        """Create various types of plots"""
        try:
            numbers = re.findall(r'(\d+\.?\d*)', user_input)
            lower_input = user_input.lower()
            
            # Bar Chart
            if "bar" in lower_input:
                return self.create_bar_chart(numbers)
            
            # Pie Chart
            elif "pie" in lower_input:
                return self.create_pie_chart(numbers)
            
            # Scatter Plot
            elif "scatter" in lower_input:
                return self.create_scatter_plot(numbers)
            
            # Histogram
            elif "histogram" in lower_input:
                return self.create_histogram(numbers)
            
            # Default: Line Plot (handles sin, cos, etc.)
            else:
                return self.create_line_plot(numbers, lower_input)
                
        except Exception as e:
            return f"Couldn't create plot: {str(e)}"
    
    def create_bar_chart(self, numbers):
        """Create bar chart"""
        if numbers:
            nums = [float(n) for n in numbers]
            labels = [f'Item {i+1}' for i in range(len(nums))]
            plt.bar(labels, nums, color='skyblue', edgecolor='black')
            plt.title('📊 Bar Chart')
            plt.xlabel('Categories')
            plt.ylabel('Values')
            plt.grid(True, alpha=0.3)
            plt.show()
            return f"✅ Bar chart created with {len(nums)} values!"
        else:
            labels = ['A', 'B', 'C', 'D', 'E']
            values = [25, 40, 35, 50, 45]
            plt.bar(labels, values, color=['red', 'blue', 'green', 'orange', 'purple'])
            plt.title('📊 Sample Bar Chart')
            plt.xlabel('Categories')
            plt.ylabel('Values')
            plt.grid(True, alpha=0.3)
            plt.show()
            return "✅ Sample bar chart created!"
    
    def create_pie_chart(self, numbers):
        """Create pie chart"""
        if numbers:
            nums = [float(n) for n in numbers]
            labels = [f'Part {i+1}' for i in range(len(nums))]
            plt.pie(nums, labels=labels, autopct='%1.1f%%', startangle=90)
            plt.title('📊 Pie Chart')
            plt.axis('equal')
            plt.show()
            return f"✅ Pie chart with {len(nums)} sections!"
        else:
            labels = ['Apples', 'Bananas', 'Oranges', 'Grapes']
            sizes = [30, 25, 25, 20]
            plt.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90)
            plt.title('Fruit Distribution')
            plt.axis('equal')
            plt.show()
            return "✅ Sample pie chart created!"
    
    def create_scatter_plot(self, numbers):
        """Create scatter plot"""
        if len(numbers) >= 4:
            x = numbers[0:len(numbers)//2]
            y = numbers[len(numbers)//2:]
            plt.scatter(x, y, color='red', s=100, alpha=0.6)
            plt.title('Scatter Plot')
            plt.xlabel('X Values')
            plt.ylabel('Y Values')
            plt.grid(True, alpha=0.3)
            plt.show()
            return "✅ Scatter plot created!"
        else:
            x = np.random.rand(50)
            y = np.random.rand(50)
            plt.scatter(x, y, c=x, s=100, alpha=0.6)
            plt.title('Random Scatter Plot')
            plt.colorbar()
            plt.show()
            return "✅ Random scatter plot created!"
    
    def create_histogram(self, numbers):
        """Create histogram"""
        if numbers:
            nums = [float(n) for n in numbers]
            plt.hist(nums, bins=10, color='green', alpha=0.7)
            plt.title('Histogram')
            plt.xlabel('Values')
            plt.ylabel('Frequency')
            plt.grid(True, alpha=0.3)
            plt.show()
            return f"✅ Histogram with {len(nums)} values!"
        else:
            data = np.random.normal(0, 1, 1000)
            plt.hist(data, bins=20, color='blue', alpha=0.7)
            plt.title('Random Normal Distribution')
            plt.xlabel('Value')
            plt.ylabel('Frequency')
            plt.grid(True, alpha=0.3)
            plt.show()
            return "✅ Sample histogram created!"
    
    def create_line_plot(self, numbers, lower_input):
        """Create line plot, handles sin/cos/exp etc."""
        x = np.linspace(0, 10, 100)
        
        if "sin" in lower_input:
            y = np.sin(x)
            label = 'sin(x)'
        elif "cos" in lower_input:
            y = np.cos(x)
            label = 'cos(x)'
        elif "tan" in lower_input:
            y = np.tan(x)
            label = 'tan(x)'
            plt.ylim(-10, 10)  # avoid extreme values
        elif "exp" in lower_input or "exponential" in lower_input:
            y = np.exp(x/2)
            label = 'exp(x/2)'
        elif "log" in lower_input:
            x = np.linspace(0.1, 10, 100)
            y = np.log(x)
            label = 'ln(x)'
        elif "parabola" in lower_input or "quadratic" in lower_input:
            y = x**2
            label = 'x²'
        elif "cubic" in lower_input:
            y = x**3
            label = 'x³'
        else:
            # Default: show both sin and cos if no function specified
            plt.plot(x, np.sin(x), label='sin(x)', linewidth=2)
            plt.plot(x, np.cos(x), label='cos(x)', linewidth=2)
            plt.title('Sine and Cosine Functions')
            plt.xlabel('x')
            plt.ylabel('y')
            plt.legend()
            plt.grid(True, alpha=0.3)
            plt.show()
            return "✅ Sine and cosine plot created!"
        
        plt.plot(x, y, label=label, linewidth=2)
        plt.title(f'Plot of {label}')
        plt.xlabel('x')
        plt.ylabel('y')
        plt.legend()
        plt.grid(True, alpha=0.3)
        plt.show()
        return f"✅ Plot of {label} created!"
