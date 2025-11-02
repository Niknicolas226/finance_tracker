from datetime import datetime
import re

class DataValidator:
    @staticmethod
    def get_date(prompt="Enter date (DD-MM-YYYY or DD-MM-YY): ", allow_default=True):
        """Get a valid date from the user with multiple format support"""
        while True:
            date_str = input(prompt).strip()
            
            if allow_default and not date_str:
                return datetime.today().strftime("%d-%m-%Y")
            
            try:
                # Try multiple date formats
                for fmt in ["%d-%m-%Y", "%d-%m-%y", "%Y-%m-%d"]:
                    try:
                        valid_date = datetime.strptime(date_str, fmt)
                        return valid_date.strftime("%d-%m-%Y")
                    except ValueError:
                        continue
                print("❌ Invalid date format. Please use DD-MM-YYYY, DD-MM-YY, or YYYY-MM-DD")
            except Exception as e:
                print(f"❌ Date error: {e}")

    @staticmethod
    def get_amount(prompt="Enter amount: "):
        """Get a valid positive amount with currency formatting support"""
        while True:
            try:
                amount_str = input(prompt).strip()
                
                # Remove currency symbols and commas
                amount_str = re.sub(r'[₹$,]', '', amount_str)
                
                amount = float(amount_str)
                if amount <= 0:
                    print("❌ Amount must be positive.")
                    continue
                
                return round(amount, 2)
            except ValueError:
                print("❌ Please enter a valid number (e.g., 1500.50)")

    @staticmethod
    def get_category(prompt="Enter category (I for Income / E for Expense): "):
        """Get category with enhanced validation"""
        while True:
            category = input(prompt).strip().upper()
            
            if category in ["I", "INCOME"]:
                return "I"
            elif category in ["E", "EXPENSE"]:
                return "E"
            else:
                print("❌ Invalid category. Please enter 'I' for Income or 'E' for Expense")

    @staticmethod
    def get_description(prompt="Enter description: ", required=True):
        """Get description with validation"""
        while True:
            description = input(prompt).strip()
            
            if not description and required:
                print("❌ Description is required.")
                continue
            
            if len(description) > 100:
                print("❌ Description too long (max 100 characters).")
                continue
            
            return description

    @staticmethod
    def get_transaction_type():
        """Get transaction type for advanced categorization"""
        print("\n📊 Transaction Types:")
        types = {
            "1": ("Salary", "I"),
            "2": ("Investment", "I"), 
            "3": ("Freelance", "I"),
            "4": ("Food & Dining", "E"),
            "5": ("Shopping", "E"),
            "6": ("Bills & Utilities", "E"),
            "7": ("Transport", "E"),
            "8": ("Entertainment", "E"),
            "9": ("Other", "Both")
        }
        
        for key, (name, cat) in types.items():
            print(f"  {key}. {name} ({'Income' if cat == 'I' else 'Expense' if cat == 'E' else 'Both'})")
        
        while True:
            choice = input("\nSelect transaction type (1-9): ").strip()
            if choice in types:
                return types[choice]
            print("❌ Invalid choice. Please select 1-9.")

# Backward compatibility
def get_date(prompt="Enter date (DD-MM-YYYY): ", allow_default=True):
    return DataValidator.get_date(prompt, allow_default)

def get_amount(prompt="Enter amount: "):
    return DataValidator.get_amount(prompt)

def get_category(prompt="Enter category (I for Income / E for Expense): "):
    return DataValidator.get_category(prompt)

def get_description(prompt="Enter description: "):
    return DataValidator.get_description(prompt, required=True)

if __name__ == "__main__":
    # Test the validators
    print("🧪 Testing Data Validators...")
    
    date = get_date("Test date: ", allow_default=False)
    amount = get_amount("Test amount: ")
    category = get_category("Test category: ")
    description = get_description("Test description: ")
    
    print(f"\n✅ Results:")
    print(f"Date: {date}")
    print(f"Amount: {amount}")
    print(f"Category: {category}")
    print(f"Description: {description}")