"""
Peak AI - Graphics Module (fixed)
Handles all plotting and visualization without recursion
"""

import re
import numpy as np
import matplotlib
matplotlib.use('Agg')  # Ensure headless backend
import matplotlib.pyplot as plt

class GraphicsHandler:
    def __init__(self):
        self.plot_ready = True
    
    def create_plot(self, user_input):
        """Main entry point – calls specific plot functions."""
        try:
            lower = user_input.lower()
            
            if "bar" in lower:
                return self._bar_chart(user_input)
            elif "pie" in lower:
                return self._pie_chart(user_input)
            elif "scatter" in lower:
                return self._scatter_plot(user_input)
            elif "histogram" in lower:
                return self._histogram(user_input)
            else:
                # Default: line plot (handles sin, cos, etc.)
                return self._line_plot(user_input)
        except Exception as e:
            return f"Couldn't create plot: {str(e)}"
    
    def _bar_chart(self, user_input):
        numbers = re.findall(r'(\d+\.?\d*)', user_input)
        if numbers:
            vals = [float(n) for n in numbers]
            labels = [f'Item {i+1}' for i in range(len(vals))]
            plt.bar(labels, vals, color='skyblue', edgecolor='black')
            plt.title('📊 Bar Chart')
            plt.grid(True, alpha=0.3)
        else:
            labels = ['A', 'B', 'C', 'D', 'E']
            vals = [25, 40, 35, 50, 45]
            plt.bar(labels, vals, color=['red','blue','green','orange','purple'])
            plt.title('📊 Sample Bar Chart')
        plt.xlabel('Categories')
        plt.ylabel('Values')
        plt.show()
        return "✅ Bar chart created"
    
    def _pie_chart(self, user_input):
        numbers = re.findall(r'(\d+\.?\d*)', user_input)
        if numbers:
            vals = [float(n) for n in numbers]
            labels = [f'Part {i+1}' for i in range(len(vals))]
        else:
            vals = [30, 25, 25, 20]
            labels = ['Apples', 'Bananas', 'Oranges', 'Grapes']
        plt.pie(vals, labels=labels, autopct='%1.1f%%', startangle=90)
        plt.title('📊 Pie Chart')
        plt.axis('equal')
        plt.show()
        return "✅ Pie chart created"
    
    def _scatter_plot(self, user_input):
        numbers = re.findall(r'(\d+\.?\d*)', user_input)
        if len(numbers) >= 4:
            x = [float(n) for n in numbers[0:len(numbers)//2]]
            y = [float(n) for n in numbers[len(numbers)//2:]]
            plt.scatter(x, y, color='red', s=100, alpha=0.6)
            plt.title('Scatter Plot')
            plt.xlabel('X')
            plt.ylabel('Y')
        else:
            x = np.random.rand(50)
            y = np.random.rand(50)
            plt.scatter(x, y, c=x, s=100, alpha=0.6)
            plt.title('Random Scatter Plot')
            plt.colorbar()
        plt.grid(True, alpha=0.3)
        plt.show()
        return "✅ Scatter plot created"
    
    def _histogram(self, user_input):
        numbers = re.findall(r'(\d+\.?\d*)', user_input)
        if numbers:
            data = [float(n) for n in numbers]
        else:
            data = np.random.normal(0, 1, 1000)
        plt.hist(data, bins=10, color='green', alpha=0.7)
        plt.title('Histogram')
        plt.xlabel('Values')
        plt.ylabel('Frequency')
        plt.grid(True, alpha=0.3)
        plt.show()
        return "✅ Histogram created"
    
    def _line_plot(self, user_input):
        lower = user_input.lower()
        x = np.linspace(0, 10, 100)
        
        # Determine function
        if "sin" in lower:
            y = np.sin(x)
            label = "sin(x)"
        elif "cos" in lower:
            y = np.cos(x)
            label = "cos(x)"
        elif "tan" in lower:
            y = np.tan(x)
            label = "tan(x)"
            plt.ylim(-10, 10)  # avoid extreme values
        elif "exp" in lower or "exponential" in lower:
            y = np.exp(x/2)
            label = "exp(x/2)"
        elif "log" in lower:
            x = np.linspace(0.1, 10, 100)
            y = np.log(x)
            label = "ln(x)"
        elif "parabola" in lower or "quadratic" in lower:
            y = x**2
            label = "x²"
        elif "cubic" in lower:
            y = x**3
            label = "x³"
        else:
            # Default: show sin and cos together
            plt.plot(x, np.sin(x), label='sin(x)', linewidth=2)
            plt.plot(x, np.cos(x), label='cos(x)', linewidth=2)
            plt.title('Sine and Cosine')
            plt.xlabel('x')
            plt.ylabel('y')
            plt.legend()
            plt.grid(True, alpha=0.3)
            plt.show()
            return "✅ Sine and cosine plot"
        
        plt.plot(x, y, label=label, linewidth=2)
        plt.title(f'Plot of {label}')
        plt.xlabel('x')
        plt.ylabel('y')
        plt.legend()
        plt.grid(True, alpha=0.3)
        plt.show()
        return f"✅ Plot of {label} created"
