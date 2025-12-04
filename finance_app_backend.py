"""
Personal Finance & Product Management App - Backend
Features: Product Management, Price Tracking, Expenses, Income, Cart, Analytics
"""

import json
import sqlite3
from datetime import datetime, timedelta
from typing import List, Dict, Any, Optional, Tuple
import statistics
from pathlib import Path

# ============================================================================
# DATABASE SETUP & INITIALIZATION
# ============================================================================

class DatabaseManager:
    """Handles all database operations using SQLite"""

    def __init__(self, db_name: str = "finance_app.db"):
        self.db_path = Path(db_name)
        self.conn = None
        self.init_database()

    def init_database(self):
        """Initialize database tables"""
        self.conn = sqlite3.connect(str(self.db_path))
        self.conn.row_factory = sqlite3.Row
        cursor = self.conn.cursor()

        # Products table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS products (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL UNIQUE,
                price REAL NOT NULL,
                quantity INTEGER DEFAULT 0,
                category TEXT,
                description TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)

        # Expenses table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS expenses (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                category TEXT NOT NULL,
                amount REAL NOT NULL,
                description TEXT,
                date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                payment_method TEXT
            )
        """)

        # Income table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS income (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                source TEXT NOT NULL,
                amount REAL NOT NULL,
                description TEXT,
                date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                income_type TEXT
            )
        """)

        # Cart table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS cart (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                product_id INTEGER NOT NULL,
                quantity INTEGER NOT NULL,
                price_at_purchase REAL NOT NULL,
                added_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (product_id) REFERENCES products(id)
            )
        """)

        # Transaction History (completed purchases)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS transactions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                total_amount REAL NOT NULL,
                transaction_type TEXT,
                items_count INTEGER,
                date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)

        self.conn.commit()

    def close(self):
        """Close database connection"""
        if self.conn:
            self.conn.close()

    def execute_query(self, query: str, params: tuple = ()) -> List[Dict]:
        """Execute SELECT query"""
        cursor = self.conn.cursor()
        cursor.execute(query, params)
        return [dict(row) for row in cursor.fetchall()]

    def execute_update(self, query: str, params: tuple = ()) -> int:
        """Execute INSERT/UPDATE/DELETE query"""
        cursor = self.conn.cursor()
        cursor.execute(query, params)
        self.conn.commit()
        return cursor.lastrowid


# ============================================================================
# PRODUCT MANAGEMENT
# ============================================================================

class ProductManager:
    """Manages product operations"""

    def __init__(self, db: DatabaseManager):
        self.db = db

    def add_product(self, name: str, price: float, quantity: int = 0, 
                   category: str = "General", description: str = "") -> Dict:
        """Add new product"""
        try:
            query = """
                INSERT INTO products (name, price, quantity, category, description)
                VALUES (?, ?, ?, ?, ?)
            """
            product_id = self.db.execute_update(query, (name, price, quantity, category, description))
            return {"success": True, "product_id": product_id, "message": f"Product '{name}' added"}
        except sqlite3.IntegrityError:
            return {"success": False, "message": f"Product '{name}' already exists"}

    def update_product(self, product_id: int, **kwargs) -> Dict:
        """Update product details"""
        allowed_fields = ["name", "price", "quantity", "category", "description"]
        updates = {k: v for k, v in kwargs.items() if k in allowed_fields}

        if not updates:
            return {"success": False, "message": "No valid fields to update"}

        updates["updated_at"] = datetime.now().isoformat()
        set_clause = ", ".join([f"{k} = ?" for k in updates.keys()])
        values = list(updates.values()) + [product_id]

        query = f"UPDATE products SET {set_clause} WHERE id = ?"
        self.db.execute_update(query, tuple(values))

        return {"success": True, "message": f"Product ID {product_id} updated"}

    def get_product(self, product_id: int) -> Optional[Dict]:
        """Get product by ID"""
        query = "SELECT * FROM products WHERE id = ?"
        results = self.db.execute_query(query, (product_id,))
        return results[0] if results else None

    def get_all_products(self, category: str = None) -> List[Dict]:
        """Get all products, optionally filtered by category"""
        if category:
            query = "SELECT * FROM products WHERE category = ? ORDER BY name"
            return self.db.execute_query(query, (category,))
        else:
            query = "SELECT * FROM products ORDER BY category, name"
            return self.db.execute_query(query)

    def search_products(self, search_term: str) -> List[Dict]:
        """Search products by name"""
        query = "SELECT * FROM products WHERE name LIKE ? ORDER BY name"
        return self.db.execute_query(query, (f"%{search_term}%",))

    def delete_product(self, product_id: int) -> Dict:
        """Delete product"""
        query = "DELETE FROM products WHERE id = ?"
        self.db.execute_update(query, (product_id,))
        return {"success": True, "message": f"Product ID {product_id} deleted"}


# ============================================================================
# CART MANAGEMENT
# ============================================================================

class CartManager:
    """Manages shopping cart operations"""

    def __init__(self, db: DatabaseManager, product_manager: ProductManager):
        self.db = db
        self.pm = product_manager

    def add_to_cart(self, product_id: int, quantity: int) -> Dict:
        """Add product to cart"""
        product = self.pm.get_product(product_id)
        if not product:
            return {"success": False, "message": "Product not found"}

        if product["quantity"] < quantity:
            return {"success": False, "message": f"Insufficient stock. Available: {product['quantity']}"}

        query = """
            INSERT INTO cart (product_id, quantity, price_at_purchase)
            VALUES (?, ?, ?)
        """
        cart_id = self.db.execute_update(query, (product_id, quantity, product["price"]))
        return {"success": True, "cart_id": cart_id, "message": "Product added to cart"}

    def update_cart_item(self, cart_id: int, quantity: int) -> Dict:
        """Update quantity in cart"""
        query = "UPDATE cart SET quantity = ? WHERE id = ?"
        self.db.execute_update(query, (quantity, cart_id))
        return {"success": True, "message": "Cart item updated"}

    def remove_from_cart(self, cart_id: int) -> Dict:
        """Remove item from cart"""
        query = "DELETE FROM cart WHERE id = ?"
        self.db.execute_update(query, (cart_id,))
        return {"success": True, "message": "Item removed from cart"}

    def get_cart(self) -> List[Dict]:
        """Get all items in cart with product details"""
        query = """
            SELECT c.id, c.product_id, c.quantity, c.price_at_purchase,
                   p.name, p.category,
                   (c.quantity * c.price_at_purchase) as total_price
            FROM cart c
            JOIN products p ON c.product_id = p.id
            ORDER BY c.added_at DESC
        """
        return self.db.execute_query(query)

    def get_cart_summary(self) -> Dict:
        """Get cart summary with totals"""
        cart = self.get_cart()
        total_items = sum(item["quantity"] for item in cart)
        total_price = sum(item["total_price"] for item in cart)

        return {
            "items": cart,
            "item_count": len(cart),
            "total_quantity": total_items,
            "total_price": round(total_price, 2)
        }

    def checkout(self, payment_method: str = "cash") -> Dict:
        """Complete purchase and clear cart"""
        summary = self.get_cart_summary()

        if not summary["items"]:
            return {"success": False, "message": "Cart is empty"}

        # Update product quantities
        for item in summary["items"]:
            new_qty = item["quantity"]
            product = self.pm.get_product(item["product_id"])
            self.pm.update_product(item["product_id"], 
                                  quantity=product["quantity"] - new_qty)

        # Record transaction
        query = """
            INSERT INTO transactions (total_amount, transaction_type, items_count)
            VALUES (?, ?, ?)
        """
        transaction_id = self.db.execute_update(
            query, (summary["total_price"], "purchase", summary["item_count"])
        )

        # Clear cart
        query = "DELETE FROM cart"
        self.db.execute_update(query)

        return {
            "success": True,
            "transaction_id": transaction_id,
            "total_amount": summary["total_price"],
            "message": "Checkout successful"
        }

    def clear_cart(self) -> Dict:
        """Clear all items from cart"""
        query = "DELETE FROM cart"
        self.db.execute_update(query)
        return {"success": True, "message": "Cart cleared"}


# ============================================================================
# EXPENSE MANAGEMENT
# ============================================================================

class ExpenseManager:
    """Manages expense tracking"""

    def __init__(self, db: DatabaseManager):
        self.db = db

    def add_expense(self, category: str, amount: float, description: str = "", 
                   payment_method: str = "cash") -> Dict:
        """Record an expense"""
        query = """
            INSERT INTO expenses (category, amount, description, payment_method)
            VALUES (?, ?, ?, ?)
        """
        expense_id = self.db.execute_update(query, (category, amount, description, payment_method))
        return {"success": True, "expense_id": expense_id, "message": f"Expense of ₹{amount} recorded"}

    def get_expenses(self, days: int = 30) -> List[Dict]:
        """Get expenses from last N days"""
        cutoff_date = (datetime.now() - timedelta(days=days)).isoformat()
        query = """
            SELECT * FROM expenses
            WHERE date >= ?
            ORDER BY date DESC
        """
        return self.db.execute_query(query, (cutoff_date,))

    def get_expenses_by_category(self, days: int = 30) -> Dict:
        """Group expenses by category"""
        expenses = self.get_expenses(days)
        category_totals = {}

        for expense in expenses:
            cat = expense["category"]
            category_totals[cat] = category_totals.get(cat, 0) + expense["amount"]

        return category_totals

    def get_total_expenses(self, days: int = 30) -> float:
        """Get total expenses for period"""
        expenses = self.get_expenses(days)
        return round(sum(exp["amount"] for exp in expenses), 2)

    def delete_expense(self, expense_id: int) -> Dict:
        """Delete an expense"""
        query = "DELETE FROM expenses WHERE id = ?"
        self.db.execute_update(query, (expense_id,))
        return {"success": True, "message": "Expense deleted"}


# ============================================================================
# INCOME MANAGEMENT
# ============================================================================

class IncomeManager:
    """Manages income tracking"""

    def __init__(self, db: DatabaseManager):
        self.db = db

    def add_income(self, source: str, amount: float, description: str = "", 
                  income_type: str = "regular") -> Dict:
        """Record income"""
        query = """
            INSERT INTO income (source, amount, description, income_type)
            VALUES (?, ?, ?, ?)
        """
        income_id = self.db.execute_update(query, (source, amount, description, income_type))
        return {"success": True, "income_id": income_id, "message": f"Income of ₹{amount} recorded"}

    def get_income(self, days: int = 30) -> List[Dict]:
        """Get income from last N days"""
        cutoff_date = (datetime.now() - timedelta(days=days)).isoformat()
        query = """
            SELECT * FROM income
            WHERE date >= ?
            ORDER BY date DESC
        """
        return self.db.execute_query(query, (cutoff_date,))

    def get_income_by_source(self, days: int = 30) -> Dict:
        """Group income by source"""
        income_list = self.get_income(days)
        source_totals = {}

        for inc in income_list:
            src = inc["source"]
            source_totals[src] = source_totals.get(src, 0) + inc["amount"]

        return source_totals

    def get_total_income(self, days: int = 30) -> float:
        """Get total income for period"""
        income_list = self.get_income(days)
        return round(sum(inc["amount"] for inc in income_list), 2)

    def delete_income(self, income_id: int) -> Dict:
        """Delete income record"""
        query = "DELETE FROM income WHERE id = ?"
        self.db.execute_update(query, (income_id,))
        return {"success": True, "message": "Income record deleted"}


# ============================================================================
# ANALYTICS & REPORTING
# ============================================================================

class Analytics:
    """Generates reports and analytics"""

    def __init__(self, db: DatabaseManager, expense_mgr: ExpenseManager, 
                 income_mgr: IncomeManager, product_mgr: ProductManager):
        self.db = db
        self.em = expense_mgr
        self.im = income_mgr
        self.pm = product_mgr

    def get_financial_summary(self, days: int = 30) -> Dict:
        """Get comprehensive financial summary"""
        total_income = self.im.get_total_income(days)
        total_expenses = self.em.get_total_expenses(days)
        balance = round(total_income - total_expenses, 2)

        return {
            "period_days": days,
            "total_income": total_income,
            "total_expenses": total_expenses,
            "balance": balance,
            "savings_rate": round((balance / total_income * 100) if total_income > 0 else 0, 2)
        }

    def get_expense_breakdown(self, days: int = 30) -> Dict:
        """Get expense breakdown by category"""
        return self.em.get_expenses_by_category(days)

    def get_income_breakdown(self, days: int = 30) -> Dict:
        """Get income breakdown by source"""
        return self.im.get_income_by_source(days)

    def get_daily_summary(self, date: str = None) -> Dict:
        """Get summary for a specific day"""
        if not date:
            date = datetime.now().strftime("%Y-%m-%d")

        query = "SELECT SUM(amount) as total FROM expenses WHERE DATE(date) = ?"
        expenses = self.db.execute_query(query, (date,))
        total_expenses = expenses[0]["total"] or 0

        query = "SELECT SUM(amount) as total FROM income WHERE DATE(date) = ?"
        income = self.db.execute_query(query, (date,))
        total_income = income[0]["total"] or 0

        return {
            "date": date,
            "income": total_income,
            "expenses": total_expenses,
            "net": round(total_income - total_expenses, 2)
        }

    def get_top_expenses(self, limit: int = 5, days: int = 30) -> List[Dict]:
        """Get top N expenses"""
        query = """
            SELECT category, amount, description, date
            FROM expenses
            WHERE date >= ?
            ORDER BY amount DESC
            LIMIT ?
        """
        cutoff_date = (datetime.now() - timedelta(days=days)).isoformat()
        return self.db.execute_query(query, (cutoff_date, limit))

    def get_top_income_sources(self, limit: int = 5, days: int = 30) -> List[Dict]:
        """Get top N income sources"""
        query = """
            SELECT source, amount, description, date
            FROM income
            WHERE date >= ?
            ORDER BY amount DESC
            LIMIT ?
        """
        cutoff_date = (datetime.now() - timedelta(days=days)).isoformat()
        return self.db.execute_query(query, (cutoff_date, limit))

    def get_product_analytics(self) -> Dict:
        """Get product inventory analytics"""
        products = self.pm.get_all_products()
        total_products = len(products)
        total_inventory_value = sum(p["price"] * p["quantity"] for p in products)
        low_stock = [p for p in products if p["quantity"] < 5]

        return {
            "total_products": total_products,
            "total_inventory_value": round(total_inventory_value, 2),
            "low_stock_items": low_stock,
            "categories": list(set(p["category"] for p in products))
        }

    def get_monthly_trend(self, months: int = 6) -> List[Dict]:
        """Get monthly income vs expenses trend"""
        trends = []

        for i in range(months, 0, -1):
            month_start = datetime.now() - timedelta(days=30*i)
            month_end = month_start + timedelta(days=30)

            query = "SELECT SUM(amount) as total FROM income WHERE date BETWEEN ? AND ?"
            income = self.db.execute_query(query, (month_start.isoformat(), month_end.isoformat()))
            total_income = income[0]["total"] or 0

            query = "SELECT SUM(amount) as total FROM expenses WHERE date BETWEEN ? AND ?"
            expenses = self.db.execute_query(query, (month_start.isoformat(), month_end.isoformat()))
            total_expenses = expenses[0]["total"] or 0

            trends.append({
                "month": month_start.strftime("%B %Y"),
                "income": total_income,
                "expenses": total_expenses,
                "balance": round(total_income - total_expenses, 2)
            })

        return trends


# ============================================================================
# EXPORT & REPORTING
# ============================================================================

class ReportExporter:
    """Export data for visualization and reporting"""

    def __init__(self, analytics: Analytics):
        self.analytics = analytics

    def export_to_json(self, filename: str = "financial_report.json") -> Dict:
        """Export financial data to JSON"""
        report = {
            "generated_at": datetime.now().isoformat(),
            "financial_summary": self.analytics.get_financial_summary(),
            "expense_breakdown": self.analytics.get_expense_breakdown(),
            "income_breakdown": self.analytics.get_income_breakdown(),
            "top_expenses": self.analytics.get_top_expenses(),
            "top_income": self.analytics.get_top_income_sources(),
            "product_analytics": self.analytics.get_product_analytics(),
            "monthly_trend": self.analytics.get_monthly_trend()
        }

        with open(filename, "w") as f:
            json.dump(report, f, indent=4)

        return {"success": True, "message": f"Report exported to {filename}"}

    def export_csv_expenses(self, filename: str = "expenses.csv") -> Dict:
        """Export expenses to CSV"""
        import csv

        expenses = self.analytics.em.get_expenses(days=365)

        if not expenses:
            return {"success": False, "message": "No expenses to export"}

        with open(filename, "w", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=["id", "category", "amount", "description", "date", "payment_method"])
            writer.writeheader()
            writer.writerows(expenses)

        return {"success": True, "message": f"Expenses exported to {filename}"}

    def get_visualization_data(self) -> Dict:
        """Get data formatted for visualization libraries"""
        expense_breakdown = self.analytics.get_expense_breakdown()
        income_breakdown = self.analytics.get_income_breakdown()
        monthly_trend = self.analytics.get_monthly_trend()

        return {
            "pie_chart_expenses": {
                "labels": list(expense_breakdown.keys()),
                "values": list(expense_breakdown.values())
            },
            "pie_chart_income": {
                "labels": list(income_breakdown.keys()),
                "values": list(income_breakdown.values())
            },
            "line_chart_trend": {
                "months": [t["month"] for t in monthly_trend],
                "income": [t["income"] for t in monthly_trend],
                "expenses": [t["expenses"] for t in monthly_trend],
                "balance": [t["balance"] for t in monthly_trend]
            }
        }


# ============================================================================
# MAIN APPLICATION CLASS
# ============================================================================

class FinanceApp:
    """Main application that integrates all managers"""

    def __init__(self, db_name: str = "finance_app.db"):
        self.db = DatabaseManager(db_name)
        self.products = ProductManager(self.db)
        self.cart = CartManager(self.db, self.products)
        self.expenses = ExpenseManager(self.db)
        self.income = IncomeManager(self.db)
        self.analytics = Analytics(self.db, self.expenses, self.income, self.products)
        self.exporter = ReportExporter(self.analytics)

    def close(self):
        """Close app and database"""
        self.db.close()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()


# ============================================================================
# EXAMPLE USAGE & DEMONSTRATION
# ============================================================================

if __name__ == "__main__":
    print("=" * 70)
    print("Personal Finance & Product Management App - Backend Demo")
    print("=" * 70)

    # Initialize app
    app = FinanceApp("demo_finance.db")

    print("\n✓ Database initialized successfully")

    # Add sample products
    print("\n--- Adding Products ---")
    products_data = [
        ("Laptop", 45000, 2, "Electronics", "HP Pavilion"),
        ("Phone", 25000, 5, "Electronics", "OnePlus Nord"),
        ("Headphones", 3000, 10, "Electronics", "Noise-cancelling"),
        ("Books", 500, 20, "Education", "Python Programming"),
        ("Coffee", 200, 50, "Food", "Premium blend"),
    ]

    for name, price, qty, cat, desc in products_data:
        result = app.products.add_product(name, price, qty, cat, desc)
        print(f"  {result['message']}")

    # Add sample income
    print("\n--- Recording Income ---")
    app.income.add_income("Salary", 50000, "Monthly salary", "regular")
    app.income.add_income("Freelance", 15000, "Project work", "irregular")
    print("  ✓ Income records added")

    # Add sample expenses
    print("\n--- Recording Expenses ---")
    expenses_data = [
        ("Groceries", 5000, "Weekly shopping"),
        ("Utilities", 2000, "Electricity bill"),
        ("Transport", 1500, "Fuel and travel"),
        ("Entertainment", 3000, "Movies and dining"),
        ("Health", 1200, "Medicine"),
    ]

    for category, amount, desc in expenses_data:
        app.expenses.add_expense(category, amount, desc)
        print(f"  ✓ {category}: ₹{amount}")

    # Add to cart and checkout
    print("\n--- Shopping Cart Demo ---")
    app.cart.add_to_cart(1, 1)  # Add Laptop
    app.cart.add_to_cart(2, 2)  # Add 2 Phones

    summary = app.cart.get_cart_summary()
    print(f"  Items in cart: {summary['item_count']}")
    print(f"  Total quantity: {summary['total_quantity']}")
    print(f"  Total price: ₹{summary['total_price']}")

    result = app.cart.checkout()
    print(f"  {result['message']}")

    # Analytics
    print("\n--- Financial Summary (Last 30 Days) ---")
    summary = app.analytics.get_financial_summary(30)
    print(f"  Total Income: ₹{summary['total_income']}")
    print(f"  Total Expenses: ₹{summary['total_expenses']}")
    print(f"  Balance: ₹{summary['balance']}")
    print(f"  Savings Rate: {summary['savings_rate']}%")

    print("\n--- Expense Breakdown ---")
    expenses_by_cat = app.analytics.get_expense_breakdown()
    for category, amount in expenses_by_cat.items():
        print(f"  {category}: ₹{amount}")

    print("\n--- Income Breakdown ---")
    income_by_src = app.analytics.get_income_breakdown()
    for source, amount in income_by_src.items():
        print(f"  {source}: ₹{amount}")

    print("\n--- Product Analytics ---")
    prod_analytics = app.analytics.get_product_analytics()
    print(f"  Total Products: {prod_analytics['total_products']}")
    print(f"  Inventory Value: ₹{prod_analytics['total_inventory_value']}")
    print(f"  Low Stock Items: {len(prod_analytics['low_stock_items'])}")

    print("\n--- Monthly Trend ---")
    for trend in app.analytics.get_monthly_trend(3):
        print(f"  {trend['month']}: Income ₹{trend['income']}, Expenses ₹{trend['expenses']}, Balance ₹{trend['balance']}")

    # Export data
    print("\n--- Exporting Data ---")
    app.exporter.export_to_json("financial_report.json")
    app.exporter.export_csv_expenses("expenses.csv")
    print("  ✓ Reports exported (financial_report.json, expenses.csv)")

    # Get visualization data
    print("\n--- Visualization Data Structure ---")
    viz_data = app.exporter.get_visualization_data()
    print(f"  Expense Categories: {len(viz_data['pie_chart_expenses']['labels'])}")
    print(f"  Income Sources: {len(viz_data['pie_chart_income']['labels'])}")
    print(f"  Monthly Trend Points: {len(viz_data['line_chart_trend']['months'])}")

    print("\n--- All Products ---")
    for product in app.products.get_all_products():
        print(f"  {product['name']}: ₹{product['price']} (Stock: {product['quantity']})")

    app.close()

    print("\n" + "=" * 70)
    print("✓ Demo completed successfully!")
    print("=" * 70)
