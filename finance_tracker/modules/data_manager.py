import json
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from typing import Dict, List, Optional
import os
from dataclasses import dataclass, asdict
import hashlib

@dataclass
class Transaction:
    id: str
    date: str
    amount: float
    category: str
    type: str
    description: str
    tags: List[str]
    status: str = "completed"
    created_at: str = None
    updated_at: str = None
    
    def __post_init__(self):
        if self.created_at is None:
            self.created_at = datetime.now().isoformat()
        if self.updated_at is None:
            self.updated_at = self.created_at

class QuantumDataManager:
    def __init__(self, data_file: str = "quantum_finance_data.json"):
        self.data_file = data_file
        self.cache_file = "quantum_cache.json"
        self.transactions: List[Transaction] = []
        self.portfolio: Dict = {}
        self.user_profile: Dict = {}
        self.cache: Dict = {}
        
        self.load_data()
        
    def generate_id(self, data: str) -> str:
        """Generate unique ID for transactions"""
        return hashlib.md5(data.encode()).hexdigest()[:12]
    
    def load_data(self) -> None:
        """Load all data from storage"""
        self.load_primary_data()
        self.load_cache()
        
    def load_primary_data(self) -> None:
        """Load primary transaction data"""
        if os.path.exists(self.data_file):
            try:
                with open(self.data_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    
                # Load transactions
                self.transactions = [
                    Transaction(**txn) for txn in data.get('transactions', [])
                ]
                
                # Load portfolio
                self.portfolio = data.get('portfolio', {})
                
                # Load user profile
                self.user_profile = data.get('user_profile', {
                    'risk_tolerance': 'medium',
                    'financial_goals': [],
                    'income_sources': [],
                    'investment_experience': 'beginner'
                })
                
            except Exception as e:
                print(f"Error loading data: {e}")
                self.initialize_sample_data()
        else:
            self.initialize_sample_data()
    
    def initialize_sample_data(self) -> None:
        """Initialize with sample data for demonstration"""
        sample_transactions = [
            {
                "id": self.generate_id("salary_jan"),
                "date": "2024-01-15",
                "amount": 75000,
                "category": "Income",
                "type": "Salary",
                "description": "Monthly Salary",
                "tags": ["salary", "primary-income"],
                "status": "completed"
            },
            {
                "id": self.generate_id("grocery_jan"),
                "date": "2024-01-16",
                "amount": 8500,
                "category": "Expense",
                "type": "Food",
                "description": "Grocery Shopping",
                "tags": ["essential", "food"],
                "status": "completed"
            },
            {
                "id": self.generate_id("freelance_jan"),
                "date": "2024-01-18",
                "amount": 25000,
                "category": "Income",
                "type": "Freelance",
                "description": "Web Development Project",
                "tags": ["freelance", "side-income"],
                "status": "completed"
            }
        ]
        
        self.transactions = [Transaction(**txn) for txn in sample_transactions]
        
        self.portfolio = {
            'total_value': 1284732,
            'allocations': {
                'stocks': 35,
                'bonds': 25,
                'real_estate': 20,
                'crypto': 10,
                'cash': 5,
                'commodities': 5
            },
            'performance': {
                'ytd_return': 12.8,
                'monthly_return': 2.4,
                'volatility': 8.2
            }
        }
        
        self.user_profile = {
            'name': 'Quantum Investor',
            'risk_tolerance': 'medium',
            'financial_goals': [
                {'goal': 'Retirement', 'target': 5000000, 'timeline': 15},
                {'goal': 'Home Purchase', 'target': 2500000, 'timeline': 5}
            ],
            'income_sources': ['Salary', 'Freelance', 'Investments'],
            'investment_experience': 'intermediate'
        }
        
        self.save_data()
    
    def load_cache(self) -> None:
        """Load cached data for performance"""
        if os.path.exists(self.cache_file):
            try:
                with open(self.cache_file, 'r') as f:
                    self.cache = json.load(f)
            except:
                self.cache = {}
    
    def save_cache(self) -> None:
        """Save cache data"""
        try:
            with open(self.cache_file, 'w') as f:
                json.dump(self.cache, f, indent=2)
        except Exception as e:
            print(f"Error saving cache: {e}")
    
    def save_data(self) -> None:
        """Save all data to storage"""
        try:
            data = {
                'transactions': [asdict(txn) for txn in self.transactions],
                'portfolio': self.portfolio,
                'user_profile': self.user_profile,
                'last_updated': datetime.now().isoformat(),
                'version': '2.0.0'
            }
            
            with open(self.data_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
                
            self.update_cache()
            
        except Exception as e:
            print(f"Error saving data: {e}")
    
    def update_cache(self) -> None:
        """Update cache with frequently accessed data"""
        self.cache['summary'] = self.get_financial_summary()
        self.cache['recent_transactions'] = self.get_recent_transactions(10)
        self.cache['last_updated'] = datetime.now().isoformat()
        
        self.save_cache()
    
    def add_transaction(self, transaction_data: Dict) -> str:
        """Add a new transaction"""
        if 'id' not in transaction_data:
            transaction_data['id'] = self.generate_id(
                f"{transaction_data['date']}_{transaction_data['amount']}_{transaction_data['description']}"
            )
            
        transaction = Transaction(**transaction_data)
        self.transactions.append(transaction)
        self.save_data()
        
        return transaction.id
    
    def update_transaction(self, transaction_id: str, updates: Dict) -> bool:
        """Update an existing transaction"""
        for i, txn in enumerate(self.transactions):
            if txn.id == transaction_id:
                updated_data = {**asdict(txn), **updates}
                updated_data['updated_at'] = datetime.now().isoformat()
                self.transactions[i] = Transaction(**updated_data)
                self.save_data()
                return True
        return False
    
    def delete_transaction(self, transaction_id: str) -> bool:
        """Delete a transaction"""
        initial_length = len(self.transactions)
        self.transactions = [txn for txn in self.transactions if txn.id != transaction_id]
        
        if len(self.transactions) < initial_length:
            self.save_data()
            return True
        return False
    
    def get_transactions(self, filters: Optional[Dict] = None) -> List[Transaction]:
        """Get transactions with optional filtering"""
        transactions = self.transactions.copy()
        
        if filters:
            if 'category' in filters and filters['category'] != 'All':
                transactions = [t for t in transactions if t.category == filters['category']]
                
            if 'type' in filters and filters['type'] != 'All':
                transactions = [t for t in transactions if t.type == filters['type']]
                
            if 'date_range' in filters:
                start_date = datetime.strptime(filters['date_range']['start'], '%Y-%m-%d')
                end_date = datetime.strptime(filters['date_range']['end'], '%Y-%m-%d')
                transactions = [
                    t for t in transactions 
                    if start_date <= datetime.strptime(t.date, '%Y-%m-%d') <= end_date
                ]
        
        return sorted(transactions, key=lambda x: x.date, reverse=True)
    
    def get_recent_transactions(self, limit: int = 5) -> List[Dict]:
        """Get recent transactions for dashboard"""
        recent = sorted(self.transactions, key=lambda x: x.date, reverse=True)[:limit]
        return [asdict(txn) for txn in recent]
    
    def get_financial_summary(self) -> Dict:
        """Get comprehensive financial summary"""
        if not self.transactions:
            return self.get_empty_summary()
            
        df = pd.DataFrame([asdict(txn) for txn in self.transactions])
        df['date'] = pd.to_datetime(df['date'])
        df['amount'] = pd.to_numeric(df['amount'])
        
        # Calculate key metrics
        total_income = df[df['category'] == 'Income']['amount'].sum()
        total_expenses = df[df['category'] == 'Expense']['amount'].sum()
        net_worth = total_income - total_expenses + self.portfolio.get('total_value', 0)
        
        # Monthly calculations
        current_month = datetime.now().strftime('%Y-%m')
        monthly_income = df[
            (df['category'] == 'Income') & 
            (df['date'].dt.strftime('%Y-%m') == current_month)
        ]['amount'].sum()
        
        monthly_expenses = df[
            (df['category'] == 'Expense') & 
            (df['date'].dt.strftime('%Y-%m') == current_month)
        ]['amount'].sum()
        
        savings_rate = ((monthly_income - monthly_expenses) / monthly_income * 100) if monthly_income > 0 else 0
        
        # Category breakdown
        expense_breakdown = df[df['category'] == 'Expense'].groupby('type')['amount'].sum().to_dict()
        income_breakdown = df[df['category'] == 'Income'].groupby('type')['amount'].sum().to_dict()
        
        return {
            'total_income': total_income,
            'total_expenses': total_expenses,
            'net_worth': net_worth,
            'current_month_income': monthly_income,
            'current_month_expenses': monthly_expenses,
            'savings_rate': savings_rate,
            'expense_breakdown': expense_breakdown,
            'income_breakdown': income_breakdown,
            'transaction_count': len(df),
            'portfolio_value': self.portfolio.get('total_value', 0),
            'last_updated': datetime.now().isoformat()
        }
    
    def get_empty_summary(self) -> Dict:
        """Return empty summary template"""
        return {
            'total_income': 0,
            'total_expenses': 0,
            'net_worth': 0,
            'current_month_income': 0,
            'current_month_expenses': 0,
            'savings_rate': 0,
            'expense_breakdown': {},
            'income_breakdown': {},
            'transaction_count': 0,
            'portfolio_value': 0,
            'last_updated': datetime.now().isoformat()
        }
    
    def update_portfolio(self, portfolio_data: Dict) -> None:
        """Update portfolio information"""
        self.portfolio = {**self.portfolio, **portfolio_data}
        self.save_data()
    
    def update_user_profile(self, profile_data: Dict) -> None:
        """Update user profile"""
        self.user_profile = {**self.user_profile, **profile_data}
        self.save_data()
    
    def get_performance_metrics(self) -> Dict:
        """Get performance metrics for monitoring"""
        summary = self.get_financial_summary()
        
        return {
            'data_size': len(self.transactions),
            'last_backup': datetime.now().isoformat(),
            'memory_usage': len(json.dumps([asdict(t) for t in self.transactions])),
            'cache_hits': self.cache.get('hits', 0),
            'response_time': '0.05s',  # Simulated
            'uptime': '99.9%'  # Simulated
        }
    
    def export_data(self, format_type: str = 'json') -> str:
        """Export data in specified format"""
        data = {
            'transactions': [asdict(txn) for txn in self.transactions],
            'portfolio': self.portfolio,
            'user_profile': self.user_profile,
            'export_date': datetime.now().isoformat()
        }
        
        if format_type == 'json':
            return json.dumps(data, indent=2)
        elif format_type == 'csv':
            # Convert transactions to CSV
            df = pd.DataFrame(data['transactions'])
            return df.to_csv(index=False)
        else:
            raise ValueError(f"Unsupported format: {format_type}")
    
    def import_data(self, file_path: str, format_type: str = 'json') -> bool:
        """Import data from file"""
        try:
            if format_type == 'json':
                with open(file_path, 'r', encoding='utf-8') as f:
                    imported_data = json.load(f)
                    
                # Validate and import
                if 'transactions' in imported_data:
                    self.transactions = [
                        Transaction(**txn) for txn in imported_data['transactions']
                    ]
                    
                if 'portfolio' in imported_data:
                    self.portfolio = imported_data['portfolio']
                    
                if 'user_profile' in imported_data:
                    self.user_profile = imported_data['user_profile']
                    
                self.save_data()
                return True
                
        except Exception as e:
            print(f"Error importing data: {e}")
            return False
    
    def cleanup_old_data(self, older_than_days: int = 365) -> int:
        """Clean up data older than specified days"""
        cutoff_date = datetime.now() - timedelta(days=older_than_days)
        initial_count = len(self.transactions)
        
        self.transactions = [
            txn for txn in self.transactions 
            if datetime.strptime(txn.date, '%Y-%m-%d') >= cutoff_date
        ]
        
        removed_count = initial_count - len(self.transactions)
        if removed_count > 0:
            self.save_data()
            
        return removed_count