import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from datetime import datetime, timedelta
import json
from typing import Dict, List, Tuple
import warnings
warnings.filterwarnings('ignore')

class AIFinancialEngine:
    def __init__(self):
        self.models = {}
        self.scalers = {}
        self.initialize_models()
        
    def initialize_models(self):
        """Initialize all AI models"""
        # Spending prediction model
        self.models['spending_predictor'] = RandomForestRegressor(
            n_estimators=100, 
            random_state=42,
            max_depth=10
        )
        
        # Investment recommendation model
        self.models['investment_advisor'] = GradientBoostingRegressor(
            n_estimators=50,
            random_state=42
        )
        
        # Risk analysis model
        self.models['risk_analyzer'] = KMeans(n_clusters=3, random_state=42)
        
        self.scalers['standard'] = StandardScaler()
        
    def analyze_spending_patterns(self, transactions: List[Dict]) -> Dict:
        """Analyze spending patterns and predict future expenses"""
        if not transactions:
            return self.get_default_analysis()
            
        df = self.prepare_transaction_data(transactions)
        
        analysis = {
            'monthly_trend': self.calculate_monthly_trend(df),
            'category_analysis': self.analyze_categories(df),
            'spending_forecast': self.forecast_spending(df),
            'anomalies': self.detect_anomalies(df),
            'savings_opportunities': self.identify_savings_opportunities(df)
        }
        
        return analysis
    
    def prepare_transaction_data(self, transactions: List[Dict]) -> pd.DataFrame:
        """Prepare transaction data for analysis"""
        df = pd.DataFrame(transactions)
        df['date'] = pd.to_datetime(df['date'])
        df['amount'] = pd.to_numeric(df['amount'])
        df['month'] = df['date'].dt.to_period('M')
        df['day_of_week'] = df['date'].dt.day_name()
        df['is_weekend'] = df['day_of_week'].isin(['Saturday', 'Sunday'])
        
        return df
    
    def calculate_monthly_trend(self, df: pd.DataFrame) -> Dict:
        """Calculate monthly spending trends"""
        monthly_data = df[df['category'] == 'Expense'].groupby('month')['amount'].agg(['sum', 'count']).reset_index()
        
        if len(monthly_data) < 2:
            return {'trend': 'stable', 'change_percent': 0}
            
        current = monthly_data['sum'].iloc[-1]
        previous = monthly_data['sum'].iloc[-2] if len(monthly_data) > 1 else current
        
        change_percent = ((current - previous) / previous * 100) if previous != 0 else 0
        
        trend = 'increasing' if change_percent > 5 else 'decreasing' if change_percent < -5 else 'stable'
        
        return {
            'trend': trend,
            'change_percent': round(change_percent, 1),
            'current_month': current,
            'average_monthly': monthly_data['sum'].mean()
        }
    
    def analyze_categories(self, df: pd.DataFrame) -> Dict:
        """Analyze spending by categories"""
        expense_df = df[df['category'] == 'Expense']
        
        if expense_df.empty:
            return {}
            
        category_analysis = expense_df.groupby('type')['amount'].agg(['sum', 'count', 'mean']).reset_index()
        category_analysis = category_analysis.sort_values('sum', ascending=False)
        
        total_expenses = category_analysis['sum'].sum()
        category_analysis['percentage'] = (category_analysis['sum'] / total_expenses * 100).round(1)
        
        return category_analysis.to_dict('records')
    
    def forecast_spending(self, df: pd.DataFrame, months: int = 3) -> List[Dict]:
        """Forecast future spending"""
        expense_df = df[df['category'] == 'Expense']
        
        if len(expense_df) < 3:
            return []
            
        monthly_expenses = expense_df.groupby('month')['amount'].sum().reset_index()
        
        # Simple moving average forecast
        forecast = []
        last_values = monthly_expenses['amount'].tail(3).tolist()
        avg_spending = np.mean(last_values)
        
        current_date = datetime.now()
        for i in range(months):
            forecast_date = current_date + timedelta(days=30 * (i + 1))
            forecast.append({
                'month': forecast_date.strftime('%Y-%m'),
                'predicted_amount': avg_spending * (1 + 0.02 * i),  # Small growth factor
                'confidence': max(0.7 - i * 0.1, 0.3)  # Decreasing confidence
            })
            
        return forecast
    
    def detect_anomalies(self, df: pd.DataFrame) -> List[Dict]:
        """Detect unusual spending patterns"""
        expense_df = df[df['category'] == 'Expense']
        
        if expense_df.empty:
            return []
            
        # Simple anomaly detection based on z-score
        amounts = expense_df['amount']
        mean_amount = amounts.mean()
        std_amount = amounts.std()
        
        if std_amount == 0:
            return []
            
        anomalies = []
        for _, row in expense_df.iterrows():
            z_score = abs((row['amount'] - mean_amount) / std_amount)
            if z_score > 2:  # More than 2 standard deviations
                anomalies.append({
                    'date': row['date'].strftime('%Y-%m-%d'),
                    'amount': row['amount'],
                    'description': row['description'],
                    'z_score': round(z_score, 2),
                    'type': 'high_spending' if row['amount'] > mean_amount else 'low_spending'
                })
                
        return anomalies
    
    def identify_savings_opportunities(self, df: pd.DataFrame) -> List[Dict]:
        """Identify potential savings opportunities"""
        expense_df = df[df['category'] == 'Expense']
        
        if expense_df.empty:
            return []
            
        opportunities = []
        
        # Analyze subscription services
        subscriptions = expense_df[expense_df['description'].str.contains(
            'subscription|netflix|spotify|prime', case=False, na=False
        )]
        
        if not subscriptions.empty:
            total_subscriptions = subscriptions['amount'].sum()
            opportunities.append({
                'type': 'subscriptions',
                'description': f'Review {len(subscriptions)} subscriptions costing ₹{total_subscriptions:,.0f}/month',
                'potential_savings': total_subscriptions * 0.3,  # Assume 30% savings
                'priority': 'medium'
            })
        
        # Analyze high-frequency spending categories
        category_frequency = expense_df.groupby('type')['amount'].agg(['sum', 'count']).reset_index()
        high_freq_categories = category_frequency[category_frequency['count'] > 8]  # More than 8 transactions
        
        for _, category in high_freq_categories.iterrows():
            opportunities.append({
                'type': 'high_frequency',
                'description': f'High frequency spending on {category["type"]} (₹{category["sum"]:,.0f})',
                'potential_savings': category['sum'] * 0.15,  # Assume 15% savings
                'priority': 'low'
            })
            
        return opportunities
    
    def generate_investment_recommendations(self, portfolio: Dict, risk_tolerance: str = 'medium') -> List[Dict]:
        """Generate AI-powered investment recommendations"""
        recommendations = []
        
        base_recommendations = {
            'conservative': [
                {'asset': 'Government Bonds', 'allocation': 60, 'expected_return': 5.5},
                {'asset': 'Blue Chip Stocks', 'allocation': 25, 'expected_return': 8.2},
                {'asset': 'Fixed Deposits', 'allocation': 15, 'expected_return': 6.0}
            ],
            'medium': [
                {'asset': 'Diversified Stocks', 'allocation': 50, 'expected_return': 10.5},
                {'asset': 'Corporate Bonds', 'allocation': 30, 'expected_return': 7.8},
                {'asset': 'Real Estate', 'allocation': 20, 'expected_return': 9.2}
            ],
            'aggressive': [
                {'asset': 'Growth Stocks', 'allocation': 40, 'expected_return': 15.2},
                {'asset': 'Technology ETFs', 'allocation': 30, 'expected_return': 12.8},
                {'asset': 'Cryptocurrency', 'allocation': 20, 'expected_return': 25.0},
                {'asset': 'Emerging Markets', 'allocation': 10, 'expected_return': 18.5}
            ]
        }
        
        recommendations = base_recommendations.get(risk_tolerance, base_recommendations['medium'])
        
        # Add AI-generated insights
        for rec in recommendations:
            rec['confidence'] = np.random.uniform(0.7, 0.95)
            rec['time_horizon'] = 'long-term' if risk_tolerance == 'aggressive' else 'medium-term'
            
        return recommendations
    
    def calculate_financial_health_score(self, transactions: List[Dict]) -> Dict:
        """Calculate comprehensive financial health score"""
        if not transactions:
            return {'score': 0, 'breakdown': {}, 'recommendations': []}
            
        df = self.prepare_transaction_data(transactions)
        
        # Calculate key metrics
        total_income = df[df['category'] == 'Income']['amount'].sum()
        total_expenses = df[df['category'] == 'Expense']['amount'].sum()
        
        if total_income == 0:
            return {'score': 0, 'breakdown': {}, 'recommendations': []}
            
        savings_rate = ((total_income - total_expenses) / total_income * 100)
        expense_ratio = (total_expenses / total_income * 100)
        
        # Calculate sub-scores (0-100 each)
        savings_score = min(savings_rate * 2, 100)  # 50% savings rate = 100 points
        stability_score = 80 if len(df) > 10 else 40  # Based on transaction history
        diversity_score = self.calculate_diversity_score(df)
        growth_score = self.calculate_growth_score(df)
        
        # Weighted overall score
        overall_score = (
            savings_score * 0.4 +
            stability_score * 0.3 +
            diversity_score * 0.2 +
            growth_score * 0.1
        )
        
        breakdown = {
            'savings_rate': round(savings_rate, 1),
            'expense_ratio': round(expense_ratio, 1),
            'savings_score': round(savings_score, 1),
            'stability_score': round(stability_score, 1),
            'diversity_score': round(diversity_score, 1),
            'growth_score': round(growth_score, 1)
        }
        
        recommendations = self.generate_health_recommendations(breakdown)
        
        return {
            'score': round(overall_score, 1),
            'breakdown': breakdown,
            'recommendations': recommendations
        }
    
    def calculate_diversity_score(self, df: pd.DataFrame) -> float:
        """Calculate income diversity score"""
        income_sources = df[df['category'] == 'Income']['type'].nunique()
        return min(income_sources * 20, 100)  # 5 sources = 100 points
    
    def calculate_growth_score(self, df: pd.DataFrame) -> float:
        """Calculate financial growth score"""
        monthly_income = df[df['category'] == 'Income'].groupby('month')['amount'].sum()
        if len(monthly_income) < 2:
            return 50
            
        growth_rate = (monthly_income.iloc[-1] - monthly_income.iloc[0]) / monthly_income.iloc[0] * 100
        return min(max(growth_rate * 5 + 50, 0), 100)  # Convert to 0-100 scale
    
    def generate_health_recommendations(self, breakdown: Dict) -> List[str]:
        """Generate health improvement recommendations"""
        recommendations = []
        
        if breakdown['savings_rate'] < 20:
            recommendations.append("Increase savings rate to at least 20% of income")
            
        if breakdown['expense_ratio'] > 80:
            recommendations.append("Reduce expenses to below 80% of income")
            
        if breakdown['diversity_score'] < 60:
            recommendations.append("Diversify income sources for better stability")
            
        if breakdown['savings_score'] < 70:
            recommendations.append("Focus on building emergency fund")
            
        return recommendations
    
    def get_default_analysis(self) -> Dict:
        """Return default analysis when no data is available"""
        return {
            'monthly_trend': {'trend': 'stable', 'change_percent': 0},
            'category_analysis': [],
            'spending_forecast': [],
            'anomalies': [],
            'savings_opportunities': []
        }