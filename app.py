"""
Peak AI - Graphics Module (with image output)
"""

import re
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import io
import base64

class GraphicsHandler:
    def __init__(self):
        self.plot_ready = True

    def create_plot(self, user_input):
        """Main entry – returns dict with 'response' and 'image'."""
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
                return self._line_plot(user_input)
        except Exception as e:
            return {"response": f"Couldn't create plot: {str(e)}", "image": None}

    def _plot_to_base64(self, fig):
        buf = io.BytesIO()
        fig.savefig(buf, format='png', bbox_inches='tight')
        buf.seek(0)
        img_base64 = base64.b64encode(buf.read()).decode('utf-8')
        plt.close(fig)
        return f"data:image/png;base64,{img_base64}"

    def _bar_chart(self, user_input):
        numbers = re.findall(r'(\d+\.?\d*)', user_input)
        fig, ax = plt.subplots()
        if numbers:
            vals = [float(n) for n in numbers]
            labels = [f'Item {i+1}' for i in range(len(vals))]
        else:
            vals = [25, 40, 35, 50, 45]
            labels = ['A', 'B', 'C', 'D', 'E']
        ax.bar(labels, vals, color='skyblue', edgecolor='black')
        ax.set_title('📊 Bar Chart')
        ax.set_xlabel('Categories')
        ax.set_ylabel('Values')
        ax.grid(True, alpha=0.3)
        img = self._plot_to_base64(fig)
        return {"response": "✅ Bar chart created", "image": img}

    def _pie_chart(self, user_input):
        numbers = re.findall(r'(\d+\.?\d*)', user_input)
        if numbers:
            vals = [float(n) for n in numbers]
            labels = [f'Part {i+1}' for i in range(len(vals))]
        else:
            vals = [30, 25, 25, 20]
            labels = ['Apples', 'Bananas', 'Oranges', 'Grapes']
        fig, ax = plt.subplots()
        ax.pie(vals, labels=labels, autopct='%1.1f%%', startangle=90)
        ax.set_title('📊 Pie Chart')
        ax.axis('equal')
        img = self._plot_to_base64(fig)
        return {"response": "✅ Pie chart created", "image": img}

    def _scatter_plot(self, user_input):
        numbers = re.findall(r'(\d+\.?\d*)', user_input)
        fig, ax = plt.subplots()
        if len(numbers) >= 4:
            x = [float(n) for n in numbers[0:len(numbers)//2]]
            y = [float(n) for n in numbers[len(numbers)//2:]]
            ax.scatter(x, y, color='red', s=100, alpha=0.6)
            ax.set_title('Scatter Plot')
            ax.set_xlabel('X')
            ax.set_ylabel('Y')
        else:
            x = np.random.rand(50)
            y = np.random.rand(50)
            ax.scatter(x, y, c=x, s=100, alpha=0.6)
            ax.set_title('Random Scatter Plot')
            plt.colorbar(ax.scatter(x, y, c=x, s=100, alpha=0.6), ax=ax)
        ax.grid(True, alpha=0.3)
        img = self._plot_to_base64(fig)
        return {"response": "✅ Scatter plot created", "image": img}

    def _histogram(self, user_input):
        numbers = re.findall(r'(\d+\.?\d*)', user_input)
        fig, ax = plt.subplots()
        if numbers:
            data = [float(n) for n in numbers]
        else:
            data = np.random.normal(0, 1, 1000)
        ax.hist(data, bins=10, color='green', alpha=0.7)
        ax.set_title('Histogram')
        ax.set_xlabel('Values')
        ax.set_ylabel('Frequency')
        ax.grid(True, alpha=0.3)
        img = self._plot_to_base64(fig)
        return {"response": "✅ Histogram created", "image": img}

    def _line_plot(self, user_input):
        lower = user_input.lower()
        x = np.linspace(0, 10, 100)
        fig, ax = plt.subplots()

        if "sin" in lower:
            y = np.sin(x)
            label = "sin(x)"
        elif "cos" in lower:
            y = np.cos(x)
            label = "cos(x)"
        elif "tan" in lower:
            y = np.tan(x)
            label = "tan(x)"
            ax.set_ylim(-10, 10)
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
            # default: sin and cos together
            ax.plot(x, np.sin(x), label='sin(x)', linewidth=2)
            ax.plot(x, np.cos(x), label='cos(x)', linewidth=2)
            ax.set_title('Sine and Cosine')
            ax.set_xlabel('x')
            ax.set_ylabel('y')
            ax.legend()
            ax.grid(True, alpha=0.3)
            img = self._plot_to_base64(fig)
            return {"response": "✅ Sine and cosine plot", "image": img}

        ax.plot(x, y, label=label, linewidth=2)
        ax.set_title(f'Plot of {label}')
        ax.set_xlabel('x')
        ax.set_ylabel('y')
        ax.legend()
        ax.grid(True, alpha=0.3)
        img = self._plot_to_base64(fig)
        return {"response": f"✅ Plot of {label} created", "image": img}
