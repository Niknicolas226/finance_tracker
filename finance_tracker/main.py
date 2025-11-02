import tkinter as tk
from tkinter import ttk, messagebox
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from ttkbootstrap.style import Bootstyle
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.animation as animation
from matplotlib.figure import Figure
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import json
import os
import threading
import time
from collections import deque
import requests
import warnings
warnings.filterwarnings('ignore')

# Configure matplotlib for better performance
plt.style.use('dark_background')
plt.rcParams['figure.facecolor'] = '#1a1a1a'
plt.rcParams['axes.facecolor'] = '#2d2d2d'

class AdvancedFinanceTracker:
    def __init__(self):
        self.setup_theme()
        self.setup_data()
        self.create_main_window()
        self.start_real_time_updates()
        
    def setup_theme(self):
        """Setup modern theme with custom colors"""
        self.root = ttk.Window(
            title="🚀 QUANTUM FINANCE PRO",
            themename="superhero",
            size=(1600, 1000),
            iconphoto="💰",
            resizable=(True, True)
        )
        
        # Custom dark theme enhancements
        self.style = ttk.Style()
        self.style.configure('success.TButton', font=('Segoe UI', 10, 'bold'))
        self.style.configure('info.TButton', font=('Segoe UI', 10, 'bold'))
        self.style.configure('warning.TButton', font=('Segoe UI', 10, 'bold'))
        self.style.configure('danger.TButton', font=('Segoe UI', 10, 'bold'))
        
    def setup_data(self):
        """Initialize advanced data structures"""
        self.transactions = []
        self.data_file = "quantum_finance_data.json"
        self.performance_data = deque(maxlen=100)
        self.real_time_metrics = {
            'current_balance': 0,
            'transactions_today': 0,
            'spending_velocity': 0,
            'savings_trend': 0
        }
        
        self.load_data()
        self.setup_sample_data()
        
    def setup_sample_data(self):
        """Create realistic sample data if none exists"""
        if not self.transactions:
            sample_transactions = [
                {"date": "2024-01-15", "amount": 75000, "category": "Income", "type": "Salary", "description": "Monthly Salary"},
                {"date": "2024-01-16", "amount": 8500, "category": "Expense", "type": "Food", "description": "Grocery Shopping"},
                {"date": "2024-01-18", "amount": 25000, "category": "Income", "type": "Freelance", "description": "Web Development Project"},
                {"date": "2024-01-20", "amount": 3200, "category": "Expense", "type": "Bills", "description": "Electricity Bill"},
                {"date": "2024-01-22", "amount": 12300, "category": "Expense", "type": "Shopping", "description": "Electronics Purchase"},
                {"date": "2024-01-25", "amount": 5500, "category": "Income", "type": "Investment", "description": "Stock Dividends"},
                {"date": "2024-01-28", "amount": 1800, "category": "Expense", "type": "Entertainment", "description": "Movie & Dinner"},
                {"date": "2024-02-01", "amount": 78000, "category": "Income", "type": "Salary", "description": "Monthly Salary"},
                {"date": "2024-02-05", "amount": 9200, "category": "Expense", "type": "Food", "description": "Restaurant & Groceries"},
                {"date": "2024-02-10", "amount": 18000, "category": "Income", "type": "Freelance", "description": "Mobile App Development"},
            ]
            self.transactions = sample_transactions
            self.save_data()
        
    def create_main_window(self):
        """Create the main application window with modern layout"""
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        
        # Create main container with gradient effect
        self.main_container = ttk.Frame(self.root, bootstyle="dark")
        self.main_container.grid(row=0, column=0, sticky="nsew", padx=2, pady=2)
        self.main_container.columnconfigure(1, weight=1)
        self.main_container.rowconfigure(1, weight=1)
        
        self.create_modern_header()
        self.create_advanced_sidebar()
        self.create_main_content_area()
        
    def create_modern_header(self):
        """Create a modern header with real-time metrics"""
        header = ttk.Frame(self.main_container, bootstyle="primary", height=80)
        header.grid(row=0, column=0, columnspan=2, sticky="ew", pady=(0, 5))
        header.grid_propagate(False)
        
        # Left section - App title and logo
        title_frame = ttk.Frame(header, bootstyle="primary")
        title_frame.pack(side=tk.LEFT, padx=20, pady=15)
        
        # Animated logo
        self.logo_label = ttk.Label(
            title_frame, 
            text="🚀", 
            font=("Segoe UI", 24),
            bootstyle="inverse-primary"
        )
        self.logo_label.pack(side=tk.LEFT)
        
        ttk.Label(
            title_frame, 
            text="QUANTUM FINANCE PRO", 
            font=("Segoe UI", 20, "bold"),
            bootstyle="inverse-primary"
        ).pack(side=tk.LEFT, padx=10)
        
        # Center section - Real-time metrics
        metrics_frame = ttk.Frame(header, bootstyle="primary")
        metrics_frame.pack(side=tk.LEFT, padx=50, pady=10)
        
        self.real_time_widgets = {}
        metrics = [
            ("Live Balance", "₹---", "success"),
            ("Today's Flow", "₹---", "info"),
            ("Spending Rate", "---/hr", "warning"),
            ("Savings Trend", "▲ ---%", "success")
        ]
        
        for text, value, style in metrics:
            frame = ttk.Frame(metrics_frame, bootstyle="primary")
            frame.pack(side=tk.LEFT, padx=15)
            
            ttk.Label(
                frame, 
                text=text, 
                font=("Segoe UI", 9),
                bootstyle="inverse-primary"
            ).pack()
            
            label = ttk.Label(
                frame, 
                text=value, 
                font=("Segoe UI", 11, "bold"),
                bootstyle="inverse-primary"
            )
            label.pack()
            self.real_time_widgets[text] = label
        
        # Right section - Time and user
        right_frame = ttk.Frame(header, bootstyle="primary")
        right_frame.pack(side=tk.RIGHT, padx=20, pady=10)
        
        self.time_label = ttk.Label(
            right_frame,
            text="Loading...",
            font=("Segoe UI", 11, "bold"),
            bootstyle="inverse-primary"
        )
        self.time_label.pack()
        
        ttk.Label(
            right_frame,
            text="👤 Premium User",
            font=("Segoe UI", 10),
            bootstyle="inverse-primary"
        ).pack()
        
        self.animate_logo()
        self.update_clock()
        
    def create_advanced_sidebar(self):
        """Create an advanced sidebar with collapsible sections"""
        self.sidebar = ttk.Frame(self.main_container, bootstyle="secondary", width=280)
        self.sidebar.grid(row=1, column=0, sticky="nsew", padx=(0, 5))
        self.sidebar.grid_propagate(False)
        
        # User profile card
        profile_card = ttk.Frame(self.sidebar, bootstyle="dark", relief="solid", borderwidth=1)
        profile_card.pack(fill="x", padx=10, pady=15)
        
        # Profile header with avatar
        profile_header = ttk.Frame(profile_card, bootstyle="dark")
        profile_header.pack(fill="x", padx=15, pady=10)
        
        ttk.Label(
            profile_header,
            text="👑",
            font=("Segoe UI", 24),
            bootstyle="dark"
        ).pack(side=tk.LEFT)
        
        ttk.Label(
            profile_header,
            text="FINANCE MASTER",
            font=("Segoe UI", 12, "bold"),
            bootstyle="light"
        ).pack(side=tk.LEFT, padx=10)
        
        # Financial health score
        health_frame = ttk.Frame(profile_card, bootstyle="dark")
        health_frame.pack(fill="x", padx=15, pady=(0, 10))
        
        self.health_score = ttk.Progressbar(
            health_frame,
            bootstyle="success-striped",
            value=75,
            maximum=100
        )
        self.health_score.pack(fill="x")
        
        ttk.Label(
            health_frame,
            text="Financial Health: 75%",
            font=("Segoe UI", 9),
            bootstyle="light"
        ).pack()
        
        # Quick stats with icons
        stats_card = ttk.Labelframe(self.sidebar, text="📊 LIVE METRICS", bootstyle="info", padding=15)
        stats_card.pack(fill="x", padx=10, pady=10)
        
        self.quick_stats = {}
        stat_items = [
            ("💰 Total Balance", "₹---", "success"),
            ("📈 Monthly Income", "₹---", "info"), 
            ("📉 Monthly Expense", "₹---", "danger"),
            ("🎯 Savings Rate", "---%", "warning"),
            ("⚡ Net Cash Flow", "₹---", "primary")
        ]
        
        for text, value, style in stat_items:
            stat_frame = ttk.Frame(stats_card)
            stat_frame.pack(fill="x", pady=3)
            
            ttk.Label(stat_frame, text=text, font=("Segoe UI", 9), width=15).pack(side=tk.LEFT)
            label = ttk.Label(stat_frame, text=value, font=("Segoe UI", 9, "bold"), bootstyle=style)
            label.pack(side=tk.RIGHT)
            self.quick_stats[text] = label
            
        # Navigation with modern icons
        nav_card = ttk.Labelframe(self.sidebar, text="🎯 NAVIGATION", bootstyle="primary", padding=12)
        nav_card.pack(fill="x", padx=10, pady=10)
        
        nav_items = [
            ("📊 Dashboard", "dashboard", self.show_dashboard),
            ("💸 Transactions", "transactions", self.show_transactions),
            ("📈 Analytics", "analytics", self.show_analytics),
            ("🤖 AI Insights", "ai", self.show_ai_insights),
            ("🎯 Budget", "budget", self.show_budget),
            ("📋 Reports", "reports", self.show_reports),
            ("⚙️ Settings", "settings", self.show_settings)
        ]
        
        for text, icon, command in nav_items:
            btn = ttk.Button(
                nav_card,
                text=text,
                command=command,
                bootstyle="outline-primary",
                width=20
            )
            btn.pack(pady=4, fill="x")
            
    def create_main_content_area(self):
        """Create the main content area with modern notebook"""
        self.main_content = ttk.Frame(self.main_container, bootstyle="dark")
        self.main_content.grid(row=1, column=1, sticky="nsew")
        self.main_content.columnconfigure(0, weight=1)
        self.main_content.rowconfigure(0, weight=1)
        
        # Create modern notebook with custom style
        self.notebook = ttk.Notebook(self.main_content, bootstyle="dark")
        self.notebook.pack(fill="both", expand=True)
        
        # Create all tabs
        self.create_dashboard_tab()
        self.create_transactions_tab()
        self.create_analytics_tab()
        self.create_ai_tab()
        self.create_budget_tab()
        self.create_reports_tab()
        self.create_settings_tab()
        
        self.notebook.select(0)
        self.update_all_displays()
        
    def create_dashboard_tab(self):
        """Create advanced dashboard with multiple widgets"""
        dashboard_tab = ttk.Frame(self.notebook, bootstyle="dark")
        self.notebook.add(dashboard_tab, text="📊 DASHBOARD")
        
        # Top metrics row with animated cards
        metrics_frame = ttk.Frame(dashboard_tab, bootstyle="dark")
        metrics_frame.pack(fill="x", padx=15, pady=15)
        
        metrics = [
            ("Total Wealth", "₹---", "success", "💰", "trending_up"),
            ("Monthly Income", "₹---", "info", "📈", "show_chart"),
            ("Monthly Expense", "₹---", "danger", "📉", "warning"),
            ("Investment Growth", "+12.5%", "warning", "💹", "auto_graph")
        ]
        
        for i, (title, value, style, icon, anim) in enumerate(metrics):
            card = self.create_animated_metric_card(metrics_frame, title, value, style, icon, anim)
            card.grid(row=0, column=i, padx=8, sticky="nsew")
            metrics_frame.columnconfigure(i, weight=1)
            
        # Main content area with charts
        content_frame = ttk.Frame(dashboard_tab, bootstyle="dark")
        content_frame.pack(fill="both", expand=True, padx=15, pady=(0, 15))
        content_frame.columnconfigure(0, weight=3)
        content_frame.columnconfigure(1, weight=2)
        content_frame.rowconfigure(0, weight=1)
        
        # Left - Main charts
        left_frame = ttk.Frame(content_frame, bootstyle="dark")
        left_frame.grid(row=0, column=0, sticky="nsew", padx=(0, 10))
        left_frame.columnconfigure(0, weight=1)
        left_frame.rowconfigure(0, weight=1)
        left_frame.rowconfigure(1, weight=1)
        
        # Income vs Expense chart
        chart1_frame = ttk.Labelframe(left_frame, text="💰 INCOME VS EXPENSE TREND", bootstyle="info", padding=10)
        chart1_frame.grid(row=0, column=0, sticky="nsew", pady=(0, 10))
        self.create_animated_income_expense_chart(chart1_frame)
        
        # Cash flow chart
        chart2_frame = ttk.Labelframe(left_frame, text="💸 CASH FLOW ANALYSIS", bootstyle="success", padding=10)
        chart2_frame.grid(row=1, column=0, sticky="nsew")
        self.create_cash_flow_chart(chart2_frame)
        
        # Right - Side widgets
        right_frame = ttk.Frame(content_frame, bootstyle="dark")
        right_frame.grid(row=0, column=1, sticky="nsew")
        right_frame.rowconfigure(0, weight=1)
        right_frame.rowconfigure(1, weight=1)
        
        # Expense distribution
        pie_frame = ttk.Labelframe(right_frame, text="📊 EXPENSE DISTRIBUTION", bootstyle="warning", padding=10)
        pie_frame.grid(row=0, column=0, sticky="nsew", pady=(0, 10))
        self.create_animated_pie_chart(pie_frame)
        
        # Recent transactions
        recent_frame = ttk.Labelframe(right_frame, text="🕒 RECENT TRANSACTIONS", bootstyle="primary", padding=10)
        recent_frame.grid(row=1, column=0, sticky="nsew")
        recent_frame.columnconfigure(0, weight=1)
        recent_frame.rowconfigure(0, weight=1)
        
        self.create_recent_transactions_widget(recent_frame)
        
    def create_animated_metric_card(self, parent, title, value, style, icon, animation_type):
        """Create animated metric cards"""
        card = ttk.Frame(parent, bootstyle="light", relief="solid", borderwidth=1, padding=15)
        
        # Header with icon
        header = ttk.Frame(card, bootstyle="light")
        header.pack(fill="x")
        
        ttk.Label(
            header,
            text=icon,
            font=("Segoe UI", 20),
            bootstyle=style
        ).pack(side=tk.LEFT)
        
        ttk.Label(
            header,
            text=title,
            font=("Segoe UI", 11, "bold"),
            bootstyle="dark"
        ).pack(side=tk.LEFT, padx=10)
        
        # Value with animation potential
        value_label = ttk.Label(
            card,
            text=value,
            font=("Segoe UI", 16, "bold"),
            bootstyle=style
        )
        value_label.pack(pady=10)
        
        # Store reference for updates
        if not hasattr(self, 'metric_cards'):
            self.metric_cards = {}
        self.metric_cards[title] = value_label
        
        return card
        
    def create_animated_income_expense_chart(self, parent):
        """Create animated income vs expense chart"""
        fig = Figure(figsize=(8, 4), dpi=100, facecolor='#2d2d2d')
        ax = fig.add_subplot(111)
        ax.set_facecolor('#2d2d2d')
        
        # Sample data with animation
        months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun']
        income = [65000, 72000, 68000, 85000, 79000, 82000]
        expenses = [48000, 52000, 61000, 59000, 67000, 62000]
        
        bars1 = ax.bar(np.arange(len(months)) - 0.2, income, 0.4, label='Income', color='#00ff88', alpha=0.8)
        bars2 = ax.bar(np.arange(len(months)) + 0.2, expenses, 0.4, label='Expenses', color='#ff4444', alpha=0.8)
        
        ax.set_xticks(np.arange(len(months)))
        ax.set_xticklabels(months, color='white')
        ax.set_ylabel('Amount (₹)', color='white')
        ax.legend(facecolor='#2d2d2d', edgecolor='none', labelcolor='white')
        ax.grid(True, alpha=0.3, color='white')
        
        # Set spine colors
        for spine in ax.spines.values():
            spine.set_color('white')
            
        ax.tick_params(colors='white')
        
        canvas = FigureCanvasTkAgg(fig, parent)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True)
        
    def create_cash_flow_chart(self, parent):
        """Create animated cash flow chart"""
        fig = Figure(figsize=(8, 3), dpi=100, facecolor='#2d2d2d')
        ax = fig.add_subplot(111)
        ax.set_facecolor('#2d2d2d')
        
        # Sample cash flow data
        days = range(1, 31)
        cash_flow = np.cumsum(np.random.normal(1000, 500, 30))
        
        ax.plot(days, cash_flow, color='#00a8ff', linewidth=2, marker='o', markersize=3)
        ax.fill_between(days, cash_flow, alpha=0.3, color='#00a8ff')
        
        ax.set_xlabel('Days', color='white')
        ax.set_ylabel('Cash Flow (₹)', color='white')
        ax.grid(True, alpha=0.3, color='white')
        
        for spine in ax.spines.values():
            spine.set_color('white')
        ax.tick_params(colors='white')
        
        canvas = FigureCanvasTkAgg(fig, parent)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True)
        
    def create_animated_pie_chart(self, parent):
        """Create animated pie chart for expenses"""
        fig = Figure(figsize=(5, 4), dpi=100, facecolor='#2d2d2d')
        ax = fig.add_subplot(111)
        ax.set_facecolor('#2d2d2d')
        
        categories = ['Food', 'Transport', 'Entertainment', 'Bills', 'Shopping', 'Health']
        amounts = [18000, 12000, 15000, 11000, 8000, 6000]
        colors = ['#ff6b6b', '#4ecdc4', '#45b7d1', '#96ceb4', '#feca57', '#ff9ff3']
        
        wedges, texts, autotexts = ax.pie(amounts, labels=categories, colors=colors, autopct='%1.1f%%',
                                         startangle=90, textprops={'color': 'white'})
        
        for autotext in autotexts:
            autotext.set_color('white')
            autotext.set_fontweight('bold')
            
        ax.axis('equal')
        
        canvas = FigureCanvasTkAgg(fig, parent)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True)
        
    def create_recent_transactions_widget(self, parent):
        """Create recent transactions widget"""
        # Create treeview with modern style
        columns = ("Date", "Description", "Amount", "Category", "Status")
        tree = ttk.Treeview(parent, columns=columns, show="headings", height=8)
        
        # Configure columns
        col_config = {
            "Date": 100, "Description": 200, "Amount": 120, 
            "Category": 100, "Status": 80
        }
        
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=col_config[col])
            
        # Add scrollbar
        scrollbar = ttk.Scrollbar(parent, orient=tk.VERTICAL, command=tree.yview)
        tree.configure(yscrollcommand=scrollbar.set)
        
        tree.pack(side=tk.LEFT, fill="both", expand=True)
        scrollbar.pack(side=tk.RIGHT, fill="y")
        
        # Add sample transactions
        sample_data = [
            ("2024-01-15", "Monthly Salary", "₹75,000", "Income", "✅ Completed"),
            ("2024-01-16", "Grocery Shopping", "₹8,500", "Expense", "✅ Completed"),
            ("2024-01-18", "Freelance Project", "₹25,000", "Income", "✅ Completed"),
            ("2024-01-20", "Electricity Bill", "₹3,200", "Expense", "✅ Completed"),
            ("2024-01-22", "Online Shopping", "₹12,300", "Expense", "✅ Completed"),
        ]
        
        for data in sample_data:
            tree.insert("", tk.END, values=data)
            
    def create_transactions_tab(self):
        """Create advanced transactions management tab"""
        transactions_tab = ttk.Frame(self.notebook, bootstyle="dark")
        self.notebook.add(transactions_tab, text="💸 TRANSACTIONS")
        
        # Implementation would continue here...
        # [Previous transactions tab code with enhancements]
        
    def create_analytics_tab(self):
        """Create advanced analytics tab"""
        analytics_tab = ttk.Frame(self.notebook, bootstyle="dark")
        self.notebook.add(analytics_tab, text="📈 ANALYTICS")
        
        content = ttk.Frame(analytics_tab, bootstyle="dark")
        content.pack(fill="both", expand=True, padx=20, pady=20)
        
        ttk.Label(
            content,
            text="🤖 ADVANCED ANALYTICS DASHBOARD",
            font=("Segoe UI", 18, "bold"),
            bootstyle="light"
        ).pack(pady=10)
        
        # Advanced analytics content
        analytics_frame = ttk.Labelframe(content, text="📊 PREDICTIVE INSIGHTS", bootstyle="info", padding=20)
        analytics_frame.pack(fill="both", expand=True, pady=10)
        
        insights = [
            "🎯 Predicted savings increase of 15% next month",
            "📈 Spending patterns show 20% reduction in unnecessary expenses",
            "💰 Investment opportunities identified: ₹50,000 potential growth",
            "⚡ Cash flow optimization: Save ₹8,500 monthly",
            "📊 Credit score improvement: +25 points possible"
        ]
        
        for insight in insights:
            card = ttk.Frame(analytics_frame, bootstyle="light", relief="solid", borderwidth=1, padding=10)
            card.pack(fill="x", pady=5)
            ttk.Label(card, text=insight, font=("Segoe UI", 10), bootstyle="dark").pack(anchor="w")
            
    def create_ai_tab(self):
        """Create AI-powered insights tab"""
        ai_tab = ttk.Frame(self.notebook, bootstyle="dark")
        self.notebook.add(ai_tab, text="🤖 AI INSIGHTS")
        
        content = ttk.Frame(ai_tab, bootstyle="dark")
        content.pack(fill="both", expand=True, padx=20, pady=20)
        
        ttk.Label(
            content,
            text="🧠 AI-POWERED FINANCIAL INTELLIGENCE",
            font=("Segoe UI", 18, "bold"),
            bootstyle="light"
        ).pack(pady=10)
        
        # AI recommendations
        ai_frame = ttk.Labelframe(content, text="💡 SMART RECOMMENDATIONS", bootstyle="success", padding=20)
        ai_frame.pack(fill="both", expand=True, pady=10)
        
        recommendations = [
            "✅ Automate 20% savings from each income source",
            "💡 Refinance high-interest debt: Save ₹12,000 annually",
            "📊 Optimize tax strategy: Potential ₹45,000 savings",
            "🎯 Increase emergency fund to 6 months of expenses",
            "🚀 Consider index fund investments for long-term growth"
        ]
        
        for i, recommendation in enumerate(recommendations):
            card = ttk.Frame(ai_frame, bootstyle="light", relief="solid", borderwidth=1, padding=15)
            card.pack(fill="x", pady=8)
            
            ttk.Label(
                card, 
                text="🤖", 
                font=("Segoe UI", 16),
                bootstyle="info"
            ).pack(side=tk.LEFT, padx=(0, 10))
            
            ttk.Label(
                card, 
                text=recommendation, 
                font=("Segoe UI", 11),
                bootstyle="dark"
            ).pack(side=tk.LEFT, fill="x", expand=True)
            
    def create_budget_tab(self):
        """Create advanced budget planning tab"""
        budget_tab = ttk.Frame(self.notebook, bootstyle="dark")
        self.notebook.add(budget_tab, text="🎯 BUDGET")
        
        # Budget planning implementation
        # [Previous budget tab code with enhancements]
        
    def create_reports_tab(self):
        """Create comprehensive reports tab"""
        reports_tab = ttk.Frame(self.notebook, bootstyle="dark")
        self.notebook.add(reports_tab, text="📋 REPORTS")
        
        # Reports implementation
        # [Previous reports tab code with enhancements]
        
    def create_settings_tab(self):
        """Create settings tab"""
        settings_tab = ttk.Frame(self.notebook, bootstyle="dark")
        self.notebook.add(settings_tab, text="⚙️ SETTINGS")
        
        content = ttk.Frame(settings_tab, bootstyle="dark")
        content.pack(fill="both", expand=True, padx=20, pady=20)
        
        ttk.Label(
            content,
            text="⚙️ APPLICATION SETTINGS",
            font=("Segoe UI", 18, "bold"),
            bootstyle="light"
        ).pack(pady=10)
        
        # Settings options
        settings_frame = ttk.Labelframe(content, text="Preferences", bootstyle="primary", padding=20)
        settings_frame.pack(fill="both", expand=True, pady=10)
        
        # Theme selection
        theme_frame = ttk.Frame(settings_frame)
        theme_frame.pack(fill="x", pady=10)
        
        ttk.Label(theme_frame, text="Theme:", font=("Segoe UI", 11), width=15).pack(side=tk.LEFT)
        theme_var = tk.StringVar(value="darkly")
        theme_combo = ttk.Combobox(
            theme_frame, 
            textvariable=theme_var,
            values=["darkly", "superhero", "cyborg", "solar", "vapor"],
            state="readonly",
            width=20
        )
        theme_combo.pack(side=tk.LEFT)
        
    # Performance and utility methods
    def start_real_time_updates(self):
        """Start real-time data updates in separate thread"""
        def update_loop():
            while True:
                self.update_real_time_metrics()
                self.update_performance_data()
                time.sleep(2)  # Update every 2 seconds
                
        thread = threading.Thread(target=update_loop, daemon=True)
        thread.start()
        
    def update_real_time_metrics(self):
        """Update real-time metrics"""
        try:
            # Calculate real-time metrics
            total_income = sum(t["amount"] for t in self.transactions if t["category"] == "Income")
            total_expense = sum(t["amount"] for t in self.transactions if t["category"] == "Expense")
            balance = total_income - total_expense
            
            # Update widgets if they exist
            if hasattr(self, 'real_time_widgets'):
                self.real_time_widgets["Live Balance"].config(text=f"₹{balance:,.0f}")
                self.real_time_widgets["Today's Flow"].config(text=f"₹{total_income/30:,.0f}")
                
            if hasattr(self, 'quick_stats'):
                self.quick_stats["💰 Total Balance"].config(text=f"₹{balance:,.2f}")
                self.quick_stats["📈 Monthly Income"].config(text=f"₹{total_income:,.2f}")
                self.quick_stats["📉 Monthly Expense"].config(text=f"₹{total_expense:,.2f}")
                
        except Exception as e:
            print(f"Error updating metrics: {e}")
            
    def update_performance_data(self):
        """Update performance monitoring data"""
        current_time = time.time()
        self.performance_data.append({
            'timestamp': current_time,
            'memory_usage': 0,  # Would be actual memory monitoring
            'response_time': 0  # Would be actual performance monitoring
        })
        
    def animate_logo(self):
        """Animate the logo"""
        logos = ["🚀", "💎", "💰", "📈", "💹"]
        current_logo = self.logo_label.cget("text")
        next_index = (logos.index(current_logo) + 1) % len(logos) if current_logo in logos else 0
        self.logo_label.config(text=logos[next_index])
        self.root.after(2000, self.animate_logo)  # Change every 2 seconds
        
    def update_clock(self):
        """Update the real-time clock"""
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        if hasattr(self, 'time_label'):
            self.time_label.config(text=current_time)
        self.root.after(1000, self.update_clock)
        
    def update_all_displays(self):
        """Update all displays with current data"""
        self.update_real_time_metrics()
        
    def load_data(self):
        """Load data from JSON file"""
        if os.path.exists(self.data_file):
            try:
                with open(self.data_file, 'r') as f:
                    data = json.load(f)
                    self.transactions = data.get('transactions', [])
            except Exception as e:
                print(f"Error loading data: {e}")
                self.transactions = []
                
    def save_data(self):
        """Save data to JSON file"""
        try:
            data = {'transactions': self.transactions}
            with open(self.data_file, 'w') as f:
                json.dump(data, f, indent=2)
        except Exception as e:
            print(f"Error saving data: {e}")
            
    # Navigation methods
    def show_dashboard(self):
        self.notebook.select(0)
        
    def show_transactions(self):
        self.notebook.select(1)
        
    def show_analytics(self):
        self.notebook.select(2)
        
    def show_ai_insights(self):
        self.notebook.select(3)
        
    def show_budget(self):
        self.notebook.select(4)
        
    def show_reports(self):
        self.notebook.select(5)
        
    def show_settings(self):
        self.notebook.select(6)
        
    def run(self):
        """Start the application"""
        try:
            self.root.mainloop()
        except Exception as e:
            print(f"Application error: {e}")

if __name__ == "__main__":
    # Set high DPI awareness for better rendering on Windows
    try:
        from ctypes import windll
        windll.shcore.SetProcessDpiAwareness(1)
    except:
        pass
    
    app = AdvancedFinanceTracker()
    app.run()