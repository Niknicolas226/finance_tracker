import tkinter as tk
from tkinter import ttk
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import numpy as np
from datetime import datetime

class ModernGauge(tk.Canvas):
    def __init__(self, parent, width=200, height=150, **kwargs):
        super().__init__(parent, width=width, height=height, **kwargs)
        self.width = width
        self.height = height
        self.value = 0
        self.max_value = 100
        self.unit = "%"
        
    def set_value(self, value, max_value=100, unit="%"):
        self.value = value
        self.max_value = max_value
        self.unit = unit
        self.draw_gauge()
        
    def draw_gauge(self):
        self.delete("all")
        
        # Calculate proportions
        center_x = self.width // 2
        center_y = self.height - 20
        radius = min(self.width, self.height) // 2 - 10
        
        # Draw gauge arc
        start_angle = 180
        end_angle = 0
        extent = end_angle - start_angle
        
        # Background arc
        self.create_arc(
            center_x - radius, center_y - radius,
            center_x + radius, center_y + radius,
            start=start_angle, extent=extent,
            style="arc", outline="#e0e0e0", width=8
        )
        
        # Value arc
        value_angle = start_angle + (self.value / self.max_value) * extent
        self.create_arc(
            center_x - radius, center_y - radius,
            center_x + radius, center_y + radius,
            start=start_angle, extent=value_angle - start_angle,
            style="arc", outline="#4CAF50", width=8
        )
        
        # Value text
        self.create_text(
            center_x, center_y - 10,
            text=f"{self.value:.1f}{self.unit}",
            font=("Arial", 14, "bold"),
            fill="#333"
        )
        
        # Label
        self.create_text(
            center_x, center_y + 20,
            text="Progress",
            font=("Arial", 10),
            fill="#666"
        )

class AnimatedChart:
    def __init__(self, parent, chart_type="line"):
        self.parent = parent
        self.chart_type = chart_type
        self.fig = Figure(figsize=(6, 4), dpi=100)
        self.ax = self.fig.add_subplot(111)
        self.canvas = FigureCanvasTkAgg(self.fig, parent)
        
    def update_chart(self, data, labels=None, title="", animate=True):
        self.ax.clear()
        
        if self.chart_type == "line":
            self.ax.plot(data, marker='o', linewidth=2, markersize=4)
        elif self.chart_type == "bar":
            x_pos = np.arange(len(data))
            self.ax.bar(x_pos, data, alpha=0.7)
            if labels:
                self.ax.set_xticks(x_pos)
                self.ax.set_xticklabels(labels, rotation=45)
        elif self.chart_type == "pie":
            self.ax.pie(data, labels=labels, autopct='%1.1f%%', startangle=90)
            
        self.ax.set_title(title, fontsize=12, fontweight='bold')
        self.ax.grid(True, alpha=0.3)
        
        if animate:
            self.fig.canvas.draw()
            
    def get_widget(self):
        return self.canvas.get_tk_widget()

class NotificationManager:
    def __init__(self, parent):
        self.parent = parent
        self.notifications = []
        
    def show_notification(self, title, message, notification_type="info", duration=5000):
        """Show a modern notification toast"""
        toast = ttk.Toplevel(self.parent)
        toast.title("Notification")
        toast.geometry("300x80")
        toast.resizable(False, False)
        
        # Position toast in top-right corner
        toast.geometry(f"+{self.parent.winfo_x() + self.parent.winfo_width() - 320}+{self.parent.winfo_y() + 50}")
        
        # Style based on type
        styles = {
            "info": "info",
            "success": "success", 
            "warning": "warning",
            "danger": "danger"
        }
        
        style = styles.get(notification_type, "info")
        
        frame = ttk.Frame(toast, bootstyle=style)
        frame.pack(fill="both", expand=True, padx=2, pady=2)
        
        ttk.Label(frame, text=title, font=("Arial", 10, "bold"), bootstyle=f"inverse-{style}").pack(anchor="w", padx=10, pady=(5, 0))
        ttk.Label(frame, text=message, font=("Arial", 9), bootstyle=f"inverse-{style}").pack(anchor="w", padx=10, pady=(0, 5))
        
        # Auto-close after duration
        toast.after(duration, toast.destroy)

class FinancialHealthMeter(tk.Frame):
    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)
        self.create_widgets()
        
    def create_widgets(self):
        ttk.Label(self, text="Financial Health Score", font=("Arial", 12, "bold")).pack(pady=5)
        
        self.canvas = tk.Canvas(self, width=200, height=120, bg="white")
        self.canvas.pack(pady=10)
        
        self.score_label = ttk.Label(self, text="--/100", font=("Arial", 14, "bold"))
        self.score_label.pack()
        
        ttk.Label(self, text="Based on savings, spending habits, and financial goals").pack(pady=5)
        
    def update_score(self, score):
        self.score_label.config(text=f"{score}/100")
        self.draw_meter(score)
        
    def draw_meter(self, score):
        self.canvas.delete("all")
        
        # Draw meter background
        self.canvas.create_arc(10, 10, 190, 190, start=180, extent=180, 
                              outline="#e0e0e0", width=20, style="arc")
        
        # Draw score arc
        angle = 180 * (score / 100)
        color = self.get_score_color(score)
        self.canvas.create_arc(10, 10, 190, 190, start=180, extent=angle,
                              outline=color, width=20, style="arc")
        
        # Draw markers
        for i in range(0, 101, 25):
            angle = 180 + (180 * (i / 100))
            x1 = 100 + 80 * np.cos(np.radians(angle))
            y1 = 100 - 80 * np.sin(np.radians(angle))
            x2 = 100 + 70 * np.cos(np.radians(angle))
            y2 = 100 - 70 * np.sin(np.radians(angle))
            self.canvas.create_line(x1, y1, x2, y2, width=2, fill="#666")
            
    def get_score_color(self, score):
        if score >= 80:
            return "#4CAF50"  # Green
        elif score >= 60:
            return "#FFC107"  # Yellow
        elif score >= 40:
            return "#FF9800"  # Orange
        else:
            return "#F44336"  # Red