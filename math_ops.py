"""
Peak AI - Mathematics Module
Handles all mathematical operations
"""

import re
import math
import numpy as np
from collections import Counter

class MathOperations:
    """Handles all mathematical operations"""
    
    def __init__(self):
        self.context = {}
    
    def calculate_expression(self, expression):
        """Calculate mathematical expressions safely"""
        try:
            # Clean the expression
            cleaned = re.sub(r'[^0-9+\-*/().^% ]', '', expression)
            cleaned = cleaned.replace('^', '**')
            
            if cleaned:
                result = eval(cleaned)
                if isinstance(result, float) and result.is_integer():
                    result = int(result)
                return f"The result is: {result}"
            return "I couldn't parse that expression."
        except ZeroDivisionError:
            return "Division by zero is not allowed!"
        except:
            return "I couldn't calculate that. Please check your input."
    
    def solve_equation(self, text):
        """Solve simple linear equations"""
        if '=' in text:
            parts = text.split('=')
            if len(parts) == 2:
                left = parts[0].strip()
                right = parts[1].strip()
                try:
                    if 'x' in left:
                        # Simple equation solver
                        left_val = eval(left.replace('x', '0'))
                        right_val = eval(right)
                        # Extract coefficient
                        coeff_parts = left.split('x')
                        if coeff_parts[0].strip():
                            coeff = eval(coeff_parts[0].strip() or '1')
                        else:
                            coeff = 1
                        result = (right_val - left_val) / coeff
                        return f"x = {result:.2f}"
                except:
                    pass
        return "Try: 2x + 3 = 7"
    
    def calculate_derivative(self, text):
        """Calculate simple derivatives"""
        if 'x^2' in text or 'x²' in text:
            return "The derivative of x² is 2x"
        if 'sin' in text:
            return "The derivative of sin(x) is cos(x)"
        if 'cos' in text:
            return "The derivative of cos(x) is -sin(x)"
        if 'tan' in text:
            return "The derivative of tan(x) is sec²(x)"
        if 'e^' in text or 'exp' in text:
            return "The derivative of e^x is e^x"
        return "Try: derivative of x^2"
    
    def calculate_integral(self, text):
        """Calculate simple integrals"""
        if 'x^2' in text or 'x²' in text:
            return "The integral of x² is (1/3)x³ + C"
        if 'sin' in text:
            return "The integral of sin(x) is -cos(x) + C"
        if 'cos' in text:
            return "The integral of cos(x) is sin(x) + C"
        if '1/x' in text:
            return "The integral of 1/x is ln|x| + C"
        return "Try: integrate x^2"
    
    def handle_matrix(self, text):
        """Handle matrix operations"""
        numbers = re.findall(r'\d+', text)
        if len(numbers) >= 4:
            matrix = []
            for i in range(0, len(numbers), 2):
                if i+1 < len(numbers):
                    matrix.append([int(numbers[i]), int(numbers[i+1])])
            
            if len(matrix) == 2 and len(matrix[0]) == 2:
                det = matrix[0][0]*matrix[1][1] - matrix[0][1]*matrix[1][0]
                return f"Matrix: {matrix}\nDeterminant: {det}"
            return f"Matrix: {matrix}"
        return "Try: matrix [[1,2],[3,4]]"
    
    def analyze_data(self, text):
        """Analyze data sets"""
        numbers = re.findall(r'(\d+\.?\d*)', text)
        if len(numbers) >= 2:
            data = [float(n) for n in numbers]
            mean = sum(data) / len(data)
            median = sorted(data)[len(data)//2]
            variance = sum((x - mean)**2 for x in data) / len(data)
            std_dev = math.sqrt(variance)
            
            return f"""📊 Data Analysis Results:
• Data points: {len(data)}
• Mean: {mean:.2f}
• Median: {median:.2f}
• Standard Deviation: {std_dev:.2f}
• Min: {min(data):.2f}
• Max: {max(data):.2f}
• Sum: {sum(data):.2f}"""
        return "Provide data: analyze 5,10,15,20,25"
    
    def analyze_dataset(self, text):
        """Detailed dataset analysis"""
        numbers = re.findall(r'(\d+\.?\d*)', text)
        if len(numbers) >= 3:
            data = [float(n) for n in numbers]
            mean = sum(data) / len(data)
            median = sorted(data)[len(data)//2]
            variance = sum((x - mean)**2 for x in data) / len(data)
            std_dev = math.sqrt(variance)
            
            return f"""📊 Dataset Analysis - {len(data)} points

📈 Statistics:
• Mean: {mean:.2f}
• Median: {median:.2f}
• Standard Deviation: {std_dev:.2f}
• Range: {min(data):.2f} - {max(data):.2f}
• Total: {sum(data):.2f}

💡 Insight:
• {'High' if std_dev > mean*0.5 else 'Moderate' if std_dev > mean*0.2 else 'Low'} variance
• {'Data is evenly distributed' if len(set(data)) > len(data)*0.7 else 'Some repeated values'}"""
        
        return "Provide dataset: analyze 2,4,6,8,10,12,14,16"