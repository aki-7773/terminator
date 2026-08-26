"""
Peak AI - Graphics Module
Handles all plotting and visualization
"""

import re
import numpy as np
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
            
            # Default: Line Plot
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
            # Sample data
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
            # Random scatter
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
        """Create line plot"""
        if len(numbers) >= 2:
            nums = [float(n) for n in numbers]
            x = list(range(len(nums)))
            plt.plot(x, nums, marker='o', linestyle='-', linewidth=2, markersize=8)
            plt.title('📈 Line Plot')
            plt.xlabel('Index')
            plt.ylabel('Values')
            plt.grid(True, alpha=0.3)
            plt.show()
            return f"✅ Line plot with {len(nums)} points!"
        else:
            # Function plotting
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
                # Limit y-axis for tan
                plt.ylim(-10, 10)
            elif "exp" in lower_input or "exponential" in lower_input:
                y = np.exp(x/2)
                label = 'exp(x/2)'
            elif "log" in lower_input:
                x = np.linspace(0.1, 10, 100)
                y = np.log(x)
                label = 'ln(x)'
            else:
                # Default: sin and cos
                y = np.sin(x)
                y2 = np.cos(x)
                plt.plot(x, y, label='sin(x)', linewidth=2)
                plt.plot(x, y2, label='cos(x)', linewidth=2)
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
    
    def create_3d_plot(self, user_input):
        """Create 3D surface plot"""
        try:
            from mpl_toolkits.mplot3d import Axes3D
            
            fig = plt.figure(figsize=(10, 8))
            ax = fig.add_subplot(111, projection='3d')
            
            # Create 3D data
            x = np.linspace(-5, 5, 30)
            y = np.linspace(-5, 5, 30)
            X, Y = np.meshgrid(x, y)
            Z = np.sin(np.sqrt(X**2 + Y**2))
            
            ax.plot_surface(X, Y, Z, cmap='viridis', alpha=0.8)
            ax.set_title('3D Surface Plot')
            ax.set_xlabel('X')
            ax.set_ylabel('Y')
            ax.set_zlabel('Z')
            
            plt.show()
            return "✅ 3D surface plot created!"
        except ImportError:
            return "3D plots need mpl_toolkits. Install with: pip install matplotlib"
        except Exception as e:
            return f"Error creating 3D plot: {str(e)}"