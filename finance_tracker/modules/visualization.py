import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from typing import Dict, List, Optional
import tkinter as tk

class QuantumVisualizationEngine:
    def __init__(self):
        self.colors = {
            'primary': '#00D4FF',
            'secondary': '#FF6B6B', 
            'success': '#00FF88',
            'warning': '#FFD166',
            'danger': '#FF4444',
            'info': '#00A8FF',
            'dark': '#0a0a0a',
            'light': '#1a1a1a'
        }
        self.setup_matplotlib()
    
    def setup_matplotlib(self):
        """Configure matplotlib for dark theme"""
        plt.style.use('dark_background')
        plt.rcParams['figure.facecolor'] = self.colors['dark']
        plt.rcParams['axes.facecolor'] = self.colors['light']
        plt.rcParams['savefig.facecolor'] = self.colors['dark']
        plt.rcParams['grid.color'] = '#2a2a2a'
        plt.rcParams['text.color'] = 'white'
        plt.rcParams['axes.labelcolor'] = 'white'
        plt.rcParams['xtick.color'] = 'white'
        plt.rcParams['ytick.color'] = 'white'
    
    def create_wealth_growth_chart(self, parent, transactions: List[Dict], 
                                 portfolio_value: float = 0) -> FigureCanvasTkAgg:
        """Create animated wealth growth chart"""
        fig = Figure(figsize=(10, 5), dpi=100)
        ax = fig.add_subplot(111)
        
        # Process transaction data
        df = self.prepare_wealth_data(transactions, portfolio_value)
        
        if df.empty:
            ax.text(0.5, 0.5, 'No data available', ha='center', va='center', 
                   transform=ax.transAxes, fontsize=14)
            ax.set_facecolor(self.colors['light'])
            canvas = FigureCanvasTkAgg(fig, parent)
            return canvas
        
        # Create wealth growth line
        ax.plot(df['date'], df['cumulative_wealth'], 
               color=self.colors['success'], linewidth=3, 
               marker='o', markersize=4, markerfacecolor=self.colors['primary'])
        
        # Fill under line
        ax.fill_between(df['date'], df['cumulative_wealth'], 
                       alpha=0.3, color=self.colors['success'])
        
        # Styling
        ax.set_ylabel('Wealth (₹)', color='white', fontsize=12, fontweight='bold')
        ax.set_xlabel('Date', color='white', fontsize=12, fontweight='bold')
        ax.set_title('Wealth Growth Over Time', color='white', fontsize=14, fontweight='bold')
        
        # Format y-axis as currency
        ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'₹{x/1000:.0f}K'))
        
        # Rotate x-axis labels
        plt.setp(ax.get_xticklabels(), rotation=45)
        
        # Grid and borders
        ax.grid(True, alpha=0.3, color='white')
        for spine in ax.spines.values():
            spine.set_color('white')
            spine.set_linewidth(1)
        
        ax.tick_params(colors='white')
        
        fig.tight_layout()
        canvas = FigureCanvasTkAgg(fig, parent)
        canvas.draw()
        
        return canvas
    
    def prepare_wealth_data(self, transactions: List[Dict], portfolio_value: float) -> pd.DataFrame:
        """Prepare wealth data for charting"""
        if not transactions:
            return pd.DataFrame()
            
        df = pd.DataFrame(transactions)
        df['date'] = pd.to_datetime(df['date'])
        df['amount'] = pd.to_numeric(df['amount'])
        
        # Calculate daily net flow
        daily_flow = df.groupby('date').apply(
            lambda x: x[x['category'] == 'Income']['amount'].sum() - 
                     x[x['category'] == 'Expense']['amount'].sum()
        ).reset_index(name='net_flow')
        
        # Create date range
        start_date = daily_flow['date'].min()
        end_date = daily_flow['date'].max()
        date_range = pd.date_range(start=start_date, end=end_date, freq='D')
        
        # Reindex to include all dates
        daily_flow = daily_flow.set_index('date').reindex(date_range, fill_value=0).reset_index()
        daily_flow.columns = ['date', 'net_flow']
        
        # Calculate cumulative wealth
        initial_wealth = 1000000  # Starting wealth
        daily_flow['cumulative_wealth'] = initial_wealth + daily_flow['net_flow'].cumsum()
        
        # Add portfolio value to latest date
        if portfolio_value > 0 and not daily_flow.empty:
            latest_wealth = daily_flow['cumulative_wealth'].iloc[-1]
            adjustment = portfolio_value - latest_wealth
            daily_flow['cumulative_wealth'] += adjustment
            
        return daily_flow
    
    def create_income_expense_chart(self, parent, transactions: List[Dict]) -> FigureCanvasTkAgg:
        """Create income vs expense comparison chart"""
        fig = Figure(figsize=(10, 5), dpi=100)
        ax = fig.add_subplot(111)
        
        df = self.prepare_monthly_data(transactions)
        
        if df.empty:
            ax.text(0.5, 0.5, 'No data available', ha='center', va='center', 
                   transform=ax.transAxes, fontsize=14)
            ax.set_facecolor(self.colors['light'])
            canvas = FigureCanvasTkAgg(fig, parent)
            return canvas
        
        # Create bar chart
        x = np.arange(len(df))
        width = 0.35
        
        bars1 = ax.bar(x - width/2, df['income'], width, label='Income', 
                      color=self.colors['success'], alpha=0.8)
        bars2 = ax.bar(x + width/2, df['expenses'], width, label='Expenses', 
                      color=self.colors['danger'], alpha=0.8)
        
        # Add value labels on bars
        self.add_bar_labels(ax, bars1)
        self.add_bar_labels(ax, bars2)
        
        # Styling
        ax.set_ylabel('Amount (₹)', color='white', fontsize=12, fontweight='bold')
        ax.set_xlabel('Month', color='white', fontsize=12, fontweight='bold')
        ax.set_title('Monthly Income vs Expenses', color='white', fontsize=14, fontweight='bold')
        ax.set_xticks(x)
        ax.set_xticklabels(df['month'], rotation=45)
        ax.legend(facecolor=self.colors['light'], edgecolor='none', 
                 labelcolor='white', fontsize=10)
        
        # Format y-axis
        ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'₹{x/1000:.0f}K'))
        
        # Grid
        ax.grid(True, alpha=0.3, color='white', axis='y')
        for spine in ax.spines.values():
            spine.set_color('white')
        
        fig.tight_layout()
        canvas = FigureCanvasTkAgg(fig, parent)
        canvas.draw()
        
        return canvas
    
    def prepare_monthly_data(self, transactions: List[Dict]) -> pd.DataFrame:
        """Prepare monthly data for charting"""
        if not transactions:
            return pd.DataFrame()
            
        df = pd.DataFrame