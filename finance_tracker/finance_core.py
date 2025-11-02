import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import json
import os
from typing import Dict, List, Optional
from dataclasses import dataclass
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import StandardScaler
import warnings
warnings.filterwarnings('ignore')

@dataclass
class Transaction:
    date: str
    amount: float
    category: str
    subcategory: str
    description: str
    id: Optional[str] = None
    
    def __post_init__(self):
        if self.id is None:
            self.id = f"{self.date}_{self.amount}_{hash(self.description)}"

class FinanceManager:
    def __init__(self, data_file="quantum_finance_data.json"):
        self.data_file = data_file
        self.transactions: List[Transaction] = []
        self.load_data()
        
    def add_transaction(self, transaction: Transaction):
        """Add a new transaction with validation"""
        self.transactions.append(transaction)
        self.save_data()
        
    def get_transactions_df(self) -> pd.DataFrame:
        """Convert transactions to DataFrame with enhanced features"""
        if not self.transactions:
            return pd.DataFrame()
            
        data = []
        for t in self.transactions:
            data.append({
                'Date': t.date,
                'Amount': t.amount,
                'Category': t.category,
                'Subcategory': t.subcategory,
                'Description': t.description,
                'ID': t.id
            })
            
        df = pd.DataFrame(data)
        df['Date'] = pd.to_datetime(df['Date'])
        df['Month'] = df['Date'].dt.to_period('M')
        df['Year'] = df['Date'].dt.year
        df['Day'] = df['Date'].dt.day_name()
        
        return df
        
    def get_financial_summary(self) -> Dict:
        """Get comprehensive financial summary"""
        df = self.get_transactions_df()
        if df.empty:
            return self._get_empty_summary()
            
        current_month = pd.Timestamp.now().to_period('M')
        
        # Basic calculations
        total_income = df[df['Category'] == 'Income']['Amount'].sum()
        total_expenses = df[df['Category'] == 'Expense']['Amount'].sum()
        net_balance = total_income - total_expenses
        
        # Monthly calculations
        monthly_data = df.groupby('Month').agg({
            'Amount': lambda x: x[df['Category'] == 'Income'].sum(),
            'Category': lambda x: x[df['Category'] == 'Expense'].sum()
        }).rename(columns={'Amount': 'Income', 'Category': 'Expense'})
        
        current_month_data = monthly_data.loc[current_month] if current_month in monthly_data.index else pd.Series({'Income': 0, 'Expense': 0})
        
        # Advanced metrics
        savings_rate = (net_balance / total_income * 100) if total_income > 0 else 0
        expense_ratio = (total_expenses / total_income * 100) if total_income > 0 else 0
        
        # Category breakdown
        expense_breakdown = df[df['Category'] == 'Expense'].groupby('Subcategory')['Amount'].sum().to_dict()
        income_breakdown = df[df['Category'] == 'Income'].groupby('Subcategory')['Amount'].sum().to_dict()
        
        return {
            'total_income': total_income,
            'total_expenses': total_expenses,
            'net_balance': net_balance,
            'current_month_income': current_month_data['Income'],
            'current_month_expense': current_month_data['Expense'],
            'savings_rate': savings_rate,
            'expense_ratio': expense_ratio,
            'expense_breakdown': expense_breakdown,
            'income_breakdown': income_breakdown,
            'transaction_count': len(df),
            'avg_monthly_income': monthly_data['Income'].mean(),
            'avg_monthly_expense': monthly_data['Expense'].mean()
        }
        
    def get_spending_trends(self) -> Dict:
        """Analyze spending trends and patterns"""
        df = self.get_transactions_df()
        if df.empty:
            return {}
            
        # Monthly trends
        monthly_trends = df.groupby('Month').agg({
            'Amount': [('Income', lambda x: x[df['Category'] == 'Income'].sum()),
                      ('Expense', lambda x: x[df['Category'] == 'Expense'].sum())]
        }).droplevel(0, axis=1)
        
        monthly_trends['Savings'] = monthly_trends['Income'] - monthly_trends['Expense']
        
        # Daily spending patterns
        daily_patterns = df[df['Category'] == 'Expense'].groupby('Day')['Amount'].mean()
        
        # Category trends
        category_trends = df[df['Category'] == 'Expense'].groupby(['Month', 'Subcategory'])['Amount'].sum().unstack(fill_value=0)
        
        return {
            'monthly_trends': monthly_trends,
            'daily_patterns': daily_patterns,
            'category_trends': category_trends
        }
        
    def save_data(self):
        """Save data to JSON file"""
        data = {
            'transactions': [
                {
                    'date': t.date,
                    'amount': t.amount,
                    'category': t.category,
                    'subcategory': t.subcategory,
                    'description': t.description,
                    'id': t.id
                }
                for t in self.transactions
            ]
        }
        
        with open(self.data_file, 'w') as f:
            json.dump(data, f, indent=2)
            
    def load_data(self):
        """Load data from JSON file"""
        if os.path.exists(self.data_file):
            try:
                with open(self.data_file, 'r') as f:
                    data = json.load(f)
                    
                self.transactions = [
                    Transaction(
                        date=t['date'],
                        amount=t['amount'],
                        category=t['category'],
                        subcategory=t['subcategory'],
                        description=t['description'],
                        id=t.get('id')
                    )
                    for t in data.get('transactions', [])
                ]
            except Exception as e:
                print(f"Error loading data: {e}")
                self.transactions = []
                
    def _get_empty_summary(self) -> Dict:
        """Return empty summary template"""
        return {
            'total_income': 0,
            'total_expenses': 0,
            'net_balance': 0,
            'current_month_income': 0,
            'current_month_expense': 0,
            'savings_rate': 0,
            'expense_ratio': 0,
            'expense_breakdown': {},
            'income_breakdown': {},
            'transaction_count': 0,
            'avg_monthly_income': 0,
            'avg_monthly_expense': 0
        }

class AIPredictor:
    def __init__(self):
        self.model = LinearRegression()
        self.scaler = StandardScaler()
        
    def predict_future_balance(self, finance_manager: FinanceManager, months: int = 6) -> Dict:
        """Predict future balance using linear regression"""
        df = finance_manager.get_transactions_df()
        if df.empty or len(df) < 3:
            return {}
            
        # Prepare data for prediction
        monthly_data = df.groupby('Month').agg({
            'Amount': [('Income', lambda x: x[df['Category'] == 'Income'].sum()),
                      ('Expense', lambda x: x[df['Category'] == 'Expense'].sum())]
        }).droplevel(0, axis=1)
        
        monthly_data['Balance'] = monthly_data['Income'] - monthly_data['Expense']
        monthly_data = monthly_data.reset_index()
        monthly_data['MonthIndex'] = range(len(monthly_data))
        
        if len(monthly_data) < 2:
            return {}
            
        # Train model
        X = monthly_data[['MonthIndex']].values
        y = monthly_data['Balance'].values
        
        self.model.fit(X, y)
        
        # Predict future
        future_months = range(len(monthly_data), len(monthly_data) + months)
        future_predictions = self.model.predict(np.array(future_months).reshape(-1, 1))
        
        # Calculate confidence intervals (simplified)
        confidence = 0.8
        std_dev = np.std(y - self.model.predict(X))
        margin_error = std_dev * 1.96  # 95% confidence
        
        predictions = []
        for i, pred in enumerate(future_predictions):
            month_idx = len(monthly_data) + i
            predictions.append({
                'month': month_idx,
                'predicted_balance': max(0, pred),
                'confidence_low': max(0, pred - margin_error),
                'confidence_high': max(0, pred + margin_error)
            })
            
        return {
            'predictions': predictions,
            'r_squared': self.model.score(X, y),
            'current_trend': 'increasing' if future_predictions[-1] > future_predictions[0] else 'decreasing'
        }
        
    def get_spending_recommendations(self, finance_manager: FinanceManager) -> List[Dict]:
        """Generate AI-powered spending recommendations"""
        summary = finance_manager.get_financial_summary()
        trends = finance_manager.get_spending_trends()
        
        recommendations = []
        
        # Check savings rate
        if summary['savings_rate'] < 20:
            recommendations.append({
                'type': 'warning',
                'title': 'Low Savings Rate',
                'message': f'Your savings rate is {summary["savings_rate"]:.1f}%. Aim for at least 20%.',
                'action': 'Review discretionary spending'
            })
            
        # Check expense ratio
        if summary['expense_ratio'] > 80:
            recommendations.append({
                'type': 'danger',
                'title': 'High Expense Ratio',
                'message': f'You\'re spending {summary["expense_ratio"]:.1f}% of your income.',
                'action': 'Create a strict budget'
            })
            
        # Analyze category spending
        if 'category_trends' in trends and not trends['category_trends'].empty:
            latest_month = trends['category_trends'].iloc[-1]
            high_spending_categories = latest_month[latest_month > latest_month.mean() * 1.5]
            
            for category, amount in high_spending_categories.items():
                recommendations.append({
                    'type': 'info',
                    'title': f'High {category} Spending',
                    'message': f'You spent ₹{amount:,.2f} on {category} this month.',
                    'action': f'Review {category} expenses'
                })
                
        return recommendations

# Sample data generator for demonstration
class SampleDataGenerator:
    @staticmethod
    def generate_sample_data(finance_manager: FinanceManager, months=6):
        """Generate sample financial data for demonstration"""
        base_date = datetime.now() - timedelta(days=30*months)
        
        income_categories = ["Salary", "Freelance", "Investment"]
        expense_categories = ["Food", "Transport", "Entertainment", "Bills", "Shopping"]
        
        transactions = []
        
        # Generate income
        for i in range(months):
            month_date = base_date + timedelta(days=30*i)
            
            # Salary (consistent)
            transactions.append(Transaction(
                date=month_date.strftime("%Y-%m-01"),
                amount=50000 + np.random.normal(0, 1000),
                category="Income",
                subcategory="Salary",
                description="Monthly Salary"
            ))
            
            # Random freelance income
            if np.random.random() > 0.7:
                transactions.append(Transaction(
                    date=(month_date + timedelta(days=15)).strftime("%Y-%m-%d"),
                    amount=10000 + np.random.exponential(5000),
                    category="Income",
                    subcategory="Freelance",
                    description="Freelance Project"
                ))
                
        # Generate expenses
        for i in range(months * 20):  # ~20 transactions per month
            month_date = base_date + timedelta(days=30*(i//20))
            day_offset = np.random.randint(1, 30)
            trans_date = month_date + timedelta(days=day_offset)
            
            category = np.random.choice(expense_categories)
            amount = SampleDataGenerator._get_typical_amount(category)
            
            transactions.append(Transaction(
                date=trans_date.strftime("%Y-%m-%d"),
                amount=amount,
                category="Expense",
                subcategory=category,
                description=f"{category} expense"
            ))
            
        # Add to finance manager
        for transaction in transactions:
            finance_manager.add_transaction(transaction)
            
    @staticmethod
    def _get_typical_amount(category):
        """Get typical amount for a category"""
        ranges = {
            "Food": (200, 1500),
            "Transport": (100, 800),
            "Entertainment": (500, 3000),
            "Bills": (1000, 5000),
            "Shopping": (1000, 8000)
        }
        low, high = ranges.get(category, (100, 1000))
        return np.random.uniform(low, high)