import tkinter as tk
from tkinter import ttk, messagebox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import json
import os
from datetime import datetime, timedelta
import random
from collections import defaultdict

class UltimateExpenseTracker:
    def __init__(self, root):
        self.root = root
        self.root.title("💰 Ultimate Expense Tracker")
        self.root.geometry("1200x800")
        
        # Define multiple themes
        self.themes = {
            "Dark Professional": {
                'primary': '#3b82f6',
                'secondary': '#1e293b',
                'accent': '#f59e0b',
                'success': '#10b981',
                'danger': '#ef4444',
                'dark': '#0f172a',
                'light': '#f8fafc',
                'card': '#1e293b',
                'text_light': '#f8fafc',
                'text_dark': '#0f172a'
            },
            "Light Modern": {
                'primary': '#2563eb',
                'secondary': '#e2e8f0',
                'accent': '#d97706',
                'success': '#059669',
                'danger': '#dc2626',
                'dark': '#ffffff',
                'light': '#1e293b',
                'card': '#f1f5f9',
                'text_light': '#1e293b',
                'text_dark': '#ffffff'
            },
            "Pink Cute": {
                'primary': '#ec4899',
                'secondary': '#fbcfe8',
                'accent': '#f59e0b',
                'success': '#10b981',
                'danger': '#ef4444',
                'dark': '#fdf2f8',
                'light': '#831843',
                'card': '#fce7f3',
                'text_light': '#831843',
                'text_dark': '#fdf2f8'
            },
            "Ocean Blue": {
                'primary': '#06b6d4',
                'secondary': '#cffafe',
                'accent': '#8b5cf6',
                'success': '#10b981',
                'danger': '#ef4444',
                'dark': '#ecfeff',
                'light': '#164e63',
                'card': '#cffafe',
                'text_light': '#164e63',
                'text_dark': '#ecfeff'
            },
            "Forest Green": {
                'primary': '#16a34a',
                'secondary': '#dcfce7',
                'accent': '#ca8a04',
                'success': '#16a34a',
                'danger': '#dc2626',
                'dark': '#f0fdf4',
                'light': '#166534',
                'card': '#dcfce7',
                'text_light': '#166534',
                'text_dark': '#f0fdf4'
            }
        }
        
        # Default theme
        self.current_theme = "Dark Professional"
        self.colors = self.themes[self.current_theme]
        
        # Enhanced categories with icons
        self.categories = {
            "🍔 Food": {"color": self.colors['danger'], "icon": "🍔"},
            "🚗 Transportation": {"color": self.colors['primary'], "icon": "🚗"},
            "🎬 Entertainment": {"color": "#8b5cf6", "icon": "🎬"},
            "🏠 Bills": {"color": self.colors['success'], "icon": "🏠"},
            "🛒 Shopping": {"color": self.colors['accent'], "icon": "🛒"},
            "🏥 Health": {"color": "#ec4899", "icon": "🏥"},
            "✈️ Travel": {"color": "#06b6d4", "icon": "✈️"},
            "💻 Tech": {"color": "#84cc16", "icon": "💻"},
            "🎓 Education": {"color": "#f97316", "icon": "🎓"},
            "🏋️ Fitness": {"color": "#22c55e", "icon": "🏋️"},
            "🎁 Gifts": {"color": "#eab308", "icon": "🎁"},
            "💼 Business": {"color": "#64748b", "icon": "💼"}
        }
        
        self.expenses = []
        self.budget_limits = {}
        self.metric_widgets = {}
        
        # Load data
        self.load_data()
        self.create_gui()
        self.update_dashboard()
        
    def create_gui(self):
        # Main container
        self.main_container = tk.Frame(self.root, bg=self.colors['dark'])
        self.main_container.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Header
        self.create_header(self.main_container)
        
        # Content area
        content_frame = tk.Frame(self.main_container, bg=self.colors['dark'])
        content_frame.pack(fill=tk.BOTH, expand=True, pady=20)
        
        # Left panel
        left_panel = tk.Frame(content_frame, bg=self.colors['dark'])
        left_panel.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # Right panel
        right_panel = tk.Frame(content_frame, bg=self.colors['dark'], width=400)
        right_panel.pack(side=tk.RIGHT, fill=tk.BOTH, padx=(20, 0))
        
        # Create sections
        self.create_metrics_section(left_panel)
        self.create_quick_add_section(left_panel)
        self.create_expenses_section(left_panel)
        self.create_charts_section(right_panel)
        self.create_analytics_section(right_panel)
        
    def create_header(self, parent):
        header_frame = tk.Frame(parent, bg=self.colors['secondary'], height=80)
        header_frame.pack(fill=tk.X, pady=(0, 20))
        header_frame.pack_propagate(False)
        
        # App title
        title_frame = tk.Frame(header_frame, bg=self.colors['secondary'])
        title_frame.pack(side=tk.LEFT, padx=30, pady=20)
        
        tk.Label(title_frame, text="💰", font=('Arial', 24), 
                bg=self.colors['secondary'], fg=self.colors['accent']).pack(side=tk.LEFT)
        tk.Label(title_frame, text="Ultimate Expense Tracker", font=('Arial', 20, 'bold'), 
                bg=self.colors['secondary'], fg=self.colors['text_light']).pack(side=tk.LEFT, padx=10)
        
        # Theme selector
        theme_frame = tk.Frame(header_frame, bg=self.colors['secondary'])
        theme_frame.pack(side=tk.RIGHT, padx=30, pady=20)
        
        tk.Label(theme_frame, text="Theme:", font=('Arial', 10), 
                bg=self.colors['secondary'], fg=self.colors['text_light']).pack(side=tk.LEFT)
        
        self.theme_var = tk.StringVar(value=self.current_theme)
        theme_combo = ttk.Combobox(theme_frame, textvariable=self.theme_var, 
                                  values=list(self.themes.keys()), state="readonly",
                                  font=('Arial', 10), width=15)
        theme_combo.pack(side=tk.LEFT, padx=10)
        theme_combo.bind('<<ComboboxSelected>>', self.change_theme)
        
        # Current date
        date_frame = tk.Frame(header_frame, bg=self.colors['secondary'])
        date_frame.pack(side=tk.RIGHT, padx=30, pady=20)
        
        self.date_label = tk.Label(date_frame, text=datetime.now().strftime("%A, %B %d, %Y"), 
                                  font=('Arial', 12), bg=self.colors['secondary'], fg=self.colors['text_light'])
        self.date_label.pack()
        
    def change_theme(self, event=None):
        self.current_theme = self.theme_var.get()
        self.colors = self.themes[self.current_theme]
        
        # Update categories colors
        self.categories["🍔 Food"]["color"] = self.colors['danger']
        self.categories["🚗 Transportation"]["color"] = self.colors['primary']
        self.categories["🎬 Entertainment"]["color"] = "#8b5cf6"
        self.categories["🏠 Bills"]["color"] = self.colors['success']
        self.categories["🛒 Shopping"]["color"] = self.colors['accent']
        self.categories["🏥 Health"]["color"] = "#ec4899"
        
        # Recreate the entire GUI with new theme
        self.main_container.destroy()
        self.create_gui()
        self.update_dashboard()
        
    def create_metrics_section(self, parent):
        metrics_frame = tk.Frame(parent, bg=self.colors['dark'])
        metrics_frame.pack(fill=tk.X, pady=(0, 20))
        
        # Create metric cards
        metric_configs = [
            ("Total Spent", "total_spent", "$0.00", "This Month", self.colors['primary']),
            ("Daily Average", "daily_avg", "$0.00", "Per Day", self.colors['success']),
            ("Budget Left", "budget_left", "$0.00", "Remaining", self.colors['accent']),
            ("Top Category", "top_category", "Food", "Spending", self.colors['danger'])
        ]
        
        for i, (title, key, value, subtitle, color) in enumerate(metric_configs):
            card_frame = tk.Frame(metrics_frame, bg=self.colors['card'], relief='raised', bd=2,
                                highlightbackground=color, highlightthickness=2)
            card_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, 
                          padx=(0, 15) if i < 3 else (0, 0))
            card_frame.configure(height=120)
            
            # Content
            content_frame = tk.Frame(card_frame, bg=self.colors['card'])
            content_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=15)
            
            # Title
            tk.Label(content_frame, text=title, font=('Arial', 12, 'bold'),
                    bg=self.colors['card'], fg=self.colors['text_light']).pack(anchor=tk.W)
            
            # Value
            value_label = tk.Label(content_frame, text=value, font=('Arial', 24, 'bold'),
                                  bg=self.colors['card'], fg=color)
            value_label.pack(anchor=tk.W, pady=(5, 0))
            
            # Subtitle
            subtitle_label = tk.Label(content_frame, text=subtitle, font=('Arial', 10),
                                     bg=self.colors['card'], fg=self.colors['text_light'])
            subtitle_label.pack(anchor=tk.W)
            
            # Store widgets for updating
            self.metric_widgets[key] = {
                'value': value_label,
                'subtitle': subtitle_label
            }
            
    def create_quick_add_section(self, parent):
        quick_frame = tk.LabelFrame(parent, text="⚡ Quick Add Expense", 
                                   font=('Arial', 12, 'bold'), bg=self.colors['dark'],
                                   fg=self.colors['text_light'], padx=20, pady=15)
        quick_frame.pack(fill=tk.X, pady=(0, 20))
        
        # Form grid
        form_frame = tk.Frame(quick_frame, bg=self.colors['dark'])
        form_frame.pack(fill=tk.X)
        
        # Category
        tk.Label(form_frame, text="Category", font=('Arial', 10), 
                bg=self.colors['dark'], fg=self.colors['text_light']).grid(row=0, column=0, sticky=tk.W, pady=5)
        self.category_var = tk.StringVar()
        category_combo = ttk.Combobox(form_frame, textvariable=self.category_var, 
                                     values=list(self.categories.keys()), state="readonly",
                                     font=('Arial', 10), width=20)
        category_combo.grid(row=0, column=1, padx=10, pady=5, sticky=tk.W)
        category_combo.set("🍔 Food")
        
        # Amount
        tk.Label(form_frame, text="Amount", font=('Arial', 10), 
                bg=self.colors['dark'], fg=self.colors['text_light']).grid(row=0, column=2, sticky=tk.W, pady=5, padx=(20,0))
        self.amount_var = tk.StringVar()
        amount_entry = tk.Entry(form_frame, textvariable=self.amount_var, font=('Arial', 12),
                               bg='white', fg='black', relief='solid', bd=1, width=15)
        amount_entry.grid(row=0, column=3, padx=10, pady=5, sticky=tk.W)
        
        # Description
        tk.Label(form_frame, text="Description", font=('Arial', 10), 
                bg=self.colors['dark'], fg=self.colors['text_light']).grid(row=1, column=0, sticky=tk.W, pady=5)
        self.desc_var = tk.StringVar()
        desc_entry = tk.Entry(form_frame, textvariable=self.desc_var, font=('Arial', 10),
                             bg='white', fg='black', relief='solid', bd=1, width=30)
        desc_entry.grid(row=1, column=1, columnspan=3, padx=10, pady=5, sticky=tk.W+tk.E)
        
        # Buttons
        button_frame = tk.Frame(quick_frame, bg=self.colors['dark'])
        button_frame.pack(fill=tk.X, pady=(10, 0))
        
        add_btn = tk.Button(button_frame, text="💾 Add Expense", font=('Arial', 11, 'bold'),
                           bg=self.colors['primary'], fg='white', relief='raised', bd=2,
                           command=self.add_expense, padx=20, pady=8)
        add_btn.pack(side=tk.LEFT)
        
        clear_btn = tk.Button(button_frame, text="🗑️ Clear", font=('Arial', 11),
                             bg=self.colors['secondary'], fg='white', relief='raised', bd=2,
                             command=self.clear_form, padx=20, pady=8)
        clear_btn.pack(side=tk.LEFT, padx=10)
        
        # Quick amount buttons
        quick_amounts = [10, 20, 50, 100]
        for amount in quick_amounts:
            btn = tk.Button(button_frame, text=f"${amount}", font=('Arial', 9),
                           bg=self.colors['card'], fg=self.colors['text_light'], relief='solid', bd=1,
                           command=lambda a=amount: self.amount_var.set(str(a)))
            btn.pack(side=tk.LEFT, padx=5)
        
    def create_expenses_section(self, parent):
        expenses_frame = tk.LabelFrame(parent, text="📋 Recent Expenses", 
                                      font=('Arial', 12, 'bold'), bg=self.colors['dark'],
                                      fg=self.colors['text_light'], padx=20, pady=15)
        expenses_frame.pack(fill=tk.BOTH, expand=True)
        
        # Toolbar
        toolbar = tk.Frame(expenses_frame, bg=self.colors['dark'])
        toolbar.pack(fill=tk.X, pady=(0, 10))
        
        # Search
        tk.Label(toolbar, text="Search:", font=('Arial', 10), 
                bg=self.colors['dark'], fg=self.colors['text_light']).pack(side=tk.LEFT)
        self.search_var = tk.StringVar()
        search_entry = tk.Entry(toolbar, textvariable=self.search_var, font=('Arial', 10),
                               bg='white', fg='black', relief='solid', bd=1, width=20)
        search_entry.pack(side=tk.LEFT, padx=5)
        search_entry.bind('<KeyRelease>', self.filter_expenses)
        
        # Filter by category
        tk.Label(toolbar, text="Category:", font=('Arial', 10), 
                bg=self.colors['dark'], fg=self.colors['text_light']).pack(side=tk.LEFT, padx=(20,0))
        self.filter_var = tk.StringVar()
        filter_combo = ttk.Combobox(toolbar, textvariable=self.filter_var, 
                                   values=["All"] + list(self.categories.keys()), state="readonly",
                                   font=('Arial', 10), width=15)
        filter_combo.pack(side=tk.LEFT, padx=5)
        filter_combo.set("All")
        filter_combo.bind('<<ComboboxSelected>>', self.filter_expenses)
        
        # Treeview
        tree_frame = tk.Frame(expenses_frame, bg=self.colors['dark'])
        tree_frame.pack(fill=tk.BOTH, expand=True)
        
        columns = ("Date", "Description", "Category", "Amount")
        self.expense_tree = ttk.Treeview(tree_frame, columns=columns, show="headings", height=12)
        
        # Configure columns
        self.expense_tree.heading("Date", text="📅 Date")
        self.expense_tree.heading("Description", text="📝 Description")
        self.expense_tree.heading("Category", text="🏷️ Category")
        self.expense_tree.heading("Amount", text="💰 Amount")
        
        self.expense_tree.column("Date", width=100)
        self.expense_tree.column("Description", width=200)
        self.expense_tree.column("Category", width=120)
        self.expense_tree.column("Amount", width=100)
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(tree_frame, orient=tk.VERTICAL, command=self.expense_tree.yview)
        self.expense_tree.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.expense_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
    def create_charts_section(self, parent):
        charts_frame = tk.LabelFrame(parent, text="📊 Analytics", 
                                    font=('Arial', 12, 'bold'), bg=self.colors['dark'],
                                    fg=self.colors['text_light'], padx=15, pady=15)
        charts_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 15))
        
        # Time filter
        filter_frame = tk.Frame(charts_frame, bg=self.colors['dark'])
        filter_frame.pack(fill=tk.X, pady=(0, 10))
        
        tk.Label(filter_frame, text="Period:", font=('Arial', 10), 
                bg=self.colors['dark'], fg=self.colors['text_light']).pack(side=tk.LEFT)
        
        self.time_filter = tk.StringVar(value="This Month")
        time_options = ["This Week", "This Month", "Last Month", "This Year", "All Time"]
        
        for option in time_options:
            rb = tk.Radiobutton(filter_frame, text=option, variable=self.time_filter, 
                               value=option, bg=self.colors['dark'], fg=self.colors['text_light'],
                               selectcolor=self.colors['primary'], command=self.update_dashboard)
            rb.pack(side=tk.LEFT, padx=5)
        
        # Chart container
        self.chart_container = tk.Frame(charts_frame, bg=self.colors['card'], height=250)
        self.chart_container.pack(fill=tk.BOTH, expand=True)
        self.chart_container.pack_propagate(False)
        
    def create_analytics_section(self, parent):
        analytics_frame = tk.LabelFrame(parent, text="🎯 Insights", 
                                       font=('Arial', 12, 'bold'), bg=self.colors['dark'],
                                       fg=self.colors['text_light'], padx=15, pady=15)
        analytics_frame.pack(fill=tk.BOTH, expand=True)
        
        self.insights_text = tk.Text(analytics_frame, height=8, font=('Arial', 10),
                                    bg=self.colors['card'], fg=self.colors['text_light'],
                                    relief='solid', bd=1, wrap=tk.WORD)
        self.insights_text.pack(fill=tk.BOTH, expand=True)
        self.insights_text.config(state=tk.DISABLED)
        
    def add_expense(self):
        category = self.category_var.get()
        amount_str = self.amount_var.get()
        description = self.desc_var.get()
        
        if not category or category not in self.categories:
            messagebox.showerror("Error", "Please select a valid category")
            return
            
        try:
            amount = float(amount_str)
            if amount <= 0:
                raise ValueError
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid positive amount")
            return
        
        expense = {
            "id": len(self.expenses) + 1,
            "category": category,
            "amount": amount,
            "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "description": description or f"{category} expense"
        }
        
        self.expenses.append(expense)
        self.clear_form()
        self.save_data()
        self.update_dashboard()
        
        messagebox.showinfo("Success", f"✅ Added ${amount:.2f} for {category}")
    
    def clear_form(self):
        self.amount_var.set("")
        self.desc_var.set("")
        self.category_var.set("🍔 Food")
    
    def filter_expenses(self, event=None):
        search_term = self.search_var.get().lower()
        category_filter = self.filter_var.get()
        
        for item in self.expense_tree.get_children():
            self.expense_tree.delete(item)
        
        filtered_expenses = self.expenses.copy()
        
        if search_term:
            filtered_expenses = [e for e in filtered_expenses 
                               if search_term in e['description'].lower()]
        
        if category_filter != "All":
            filtered_expenses = [e for e in filtered_expenses 
                               if e['category'] == category_filter]
        
        # Show recent first
        filtered_expenses.sort(key=lambda x: x['date'], reverse=True)
        
        for expense in filtered_expenses[:20]:  # Limit to 20 entries
            date_obj = datetime.strptime(expense['date'], "%Y-%m-%d %H:%M:%S")
            self.expense_tree.insert("", "end", values=(
                date_obj.strftime("%m/%d/%Y"),
                expense['description'],
                expense['category'],
                f"${expense['amount']:.2f}"
            ))
    
    def update_dashboard(self):
        self.update_metrics()
        self.update_expenses_list()
        self.update_insights()
        self.update_chart()
    
    def update_metrics(self):
        if not self.expenses:
            # Set default values
            self.metric_widgets['total_spent']['value'].config(text="$0.00")
            self.metric_widgets['daily_avg']['value'].config(text="$0.00")
            self.metric_widgets['budget_left']['value'].config(text="$0.00")
            self.metric_widgets['top_category']['value'].config(text="None")
            return
        
        # Calculate based on time filter
        filtered_expenses = self.get_filtered_expenses()
        
        if filtered_expenses:
            total_spent = sum(e['amount'] for e in filtered_expenses)
            
            # Calculate daily average
            unique_days = len(set(datetime.strptime(e['date'], "%Y-%m-%d %H:%M:%S").day 
                                for e in filtered_expenses))
            daily_avg = total_spent / unique_days if unique_days > 0 else 0
            
            # Find top category
            category_totals = defaultdict(float)
            for expense in filtered_expenses:
                category_totals[expense['category']] += expense['amount']
            
            top_category = max(category_totals.items(), key=lambda x: x[1])[0] if category_totals else "None"
            
            # Update metrics
            self.metric_widgets['total_spent']['value'].config(text=f"${total_spent:.2f}")
            self.metric_widgets['daily_avg']['value'].config(text=f"${daily_avg:.2f}")
            self.metric_widgets['top_category']['value'].config(text=top_category.split()[-1])
            
            # Simple budget calculation (example: $2000 monthly budget)
            budget = 2000
            budget_left = max(0, budget - total_spent)
            self.metric_widgets['budget_left']['value'].config(text=f"${budget_left:.2f}")
    
    def update_expenses_list(self):
        # Clear existing items
        for item in self.expense_tree.get_children():
            self.expense_tree.delete(item)
        
        # Add expenses (most recent first)
        recent_expenses = sorted(self.expenses, 
                                key=lambda x: datetime.strptime(x['date'], "%Y-%m-%d %H:%M:%S"), 
                                reverse=True)[:15]
        
        for expense in recent_expenses:
            date_obj = datetime.strptime(expense['date'], "%Y-%m-%d %H:%M:%S")
            self.expense_tree.insert("", "end", values=(
                date_obj.strftime("%m/%d/%Y"),
                expense['description'],
                expense['category'],
                f"${expense['amount']:.2f}"
            ))
    
    def update_chart(self):
        # Clear previous chart
        for widget in self.chart_container.winfo_children():
            widget.destroy()
        
        if not self.expenses:
            # Show empty state
            empty_label = tk.Label(self.chart_container, text="📈 Expense Chart\n\nAdd some expenses to see analytics", 
                                  font=('Arial', 12), bg=self.colors['card'], fg=self.colors['text_light'])
            empty_label.pack(expand=True)
            return
        
        # Calculate category totals for filtered expenses
        filtered_expenses = self.get_filtered_expenses()
        
        if not filtered_expenses:
            empty_label = tk.Label(self.chart_container, text="📈 Expense Chart\n\nNo expenses for selected period", 
                                  font=('Arial', 12), bg=self.colors['card'], fg=self.colors['text_light'])
            empty_label.pack(expand=True)
            return
        
        category_totals = defaultdict(float)
        for expense in filtered_expenses:
            category_totals[expense['category']] += expense['amount']
        
        # Create pie chart
        fig, ax = plt.subplots(figsize=(5, 4))
        fig.patch.set_facecolor(self.colors['card'])
        
        categories = list(category_totals.keys())
        amounts = list(category_totals.values())
        colors = [self.categories[cat]['color'] for cat in categories]
        
        wedges, texts, autotexts = ax.pie(amounts, labels=categories, autopct='%1.1f%%',
                                         colors=colors, startangle=90)
        
        # Style the chart
        for text in texts:
            text.set_color(self.colors['text_light'])
        for autotext in autotexts:
            autotext.set_color(self.colors['text_light'])
            autotext.set_fontweight('bold')
        
        ax.set_title('Spending by Category', color=self.colors['text_light'], pad=20)
        
        # Embed in tkinter
        canvas = FigureCanvasTkAgg(fig, self.chart_container)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
    
    def update_insights(self):
        self.insights_text.config(state=tk.NORMAL)
        self.insights_text.delete(1.0, tk.END)
        
        if not self.expenses:
            insights = "💡 Add your first expense to see insights here!"
        else:
            filtered_expenses = self.get_filtered_expenses()
            
            if filtered_expenses:
                total = sum(e['amount'] for e in filtered_expenses)
                avg = total / len(filtered_expenses)
                
                category_totals = defaultdict(float)
                for expense in filtered_expenses:
                    category_totals[expense['category']] += expense['amount']
                
                top_category = max(category_totals.items(), key=lambda x: x[1])
                
                insights = f"""💰 Total Spent: ${total:.2f}
📈 Average Expense: ${avg:.2f}
🏆 Top Category: {top_category[0]} (${top_category[1]:.2f})
🎯 {len(filtered_expenses)} transactions

💡 Tips:
• You're doing great with {top_category[0].split()[0]} spending!
• Consider setting budgets for larger categories"""
            else:
                insights = "💡 No expenses for selected period. Try changing the time filter!"
        
        self.insights_text.insert(1.0, insights)
        self.insights_text.config(state=tk.DISABLED)
    
    def get_filtered_expenses(self):
        time_filter = self.time_filter.get()
        today = datetime.now()
        
        if time_filter == "This Week":
            start_date = today - timedelta(days=today.weekday())
            filtered = [e for e in self.expenses 
                       if datetime.strptime(e['date'], "%Y-%m-%d %H:%M:%S") >= start_date]
        elif time_filter == "This Month":
            filtered = [e for e in self.expenses 
                       if datetime.strptime(e['date'], "%Y-%m-%d %H:%M:%S").month == today.month
                       and datetime.strptime(e['date'], "%Y-%m-%d %H:%M:%S").year == today.year]
        elif time_filter == "Last Month":
            last_month = today.month - 1 if today.month > 1 else 12
            year = today.year if today.month > 1 else today.year - 1
            filtered = [e for e in self.expenses 
                       if datetime.strptime(e['date'], "%Y-%m-%d %H:%M:%S").month == last_month
                       and datetime.strptime(e['date'], "%Y-%m-%d %H:%M:%S").year == year]
        elif time_filter == "This Year":
            filtered = [e for e in self.expenses 
                       if datetime.strptime(e['date'], "%Y-%m-%d %H:%M:%S").year == today.year]
        else:  # All Time
            filtered = self.expenses
        
        return filtered
    
    def load_data(self):
        try:
            if os.path.exists('premium_expenses.json'):
                with open('premium_expenses.json', 'r') as f:
                    data = json.load(f)
                    if isinstance(data, dict) and 'expenses' in data:
                        self.expenses = data['expenses']
                        if 'theme' in data:
                            self.current_theme = data['theme']
                            self.colors = self.themes[self.current_theme]
                    else:
                        self.expenses = data
            else:
                self.create_sample_data()
        except:
            self.create_sample_data()
    
    def create_sample_data(self):
        # Create realistic sample data
        sample_descriptions = {
            "🍔 Food": ["Lunch at Cafe", "Grocery shopping", "Coffee break", "Dinner with friends"],
            "🚗 Transportation": ["Gas refill", "Uber ride", "Bus ticket", "Car maintenance"],
            "🎬 Entertainment": ["Movie tickets", "Netflix subscription", "Concert", "Bowling night"],
            "🏠 Bills": ["Electricity bill", "Internet bill", "Water bill", "Phone bill"],
            "🛒 Shopping": ["Clothes shopping", "Electronics", "Home decor", "Books"],
            "🏥 Health": ["Doctor visit", "Medicine", "Gym membership", "Vitamins"]
        }
        
        self.expenses = []
        current_date = datetime.now()
        
        for i in range(20):
            category = random.choice(list(self.categories.keys()))
            amount = round(random.uniform(5, 150), 2)
            days_ago = random.randint(0, 30)
            expense_date = current_date - timedelta(days=days_ago)
            
            expense = {
                "id": i + 1,
                "category": category,
                "amount": amount,
                "date": expense_date.strftime("%Y-%m-%d %H:%M:%S"),
                "description": random.choice(sample_descriptions.get(category, ["General expense"]))
            }
            self.expenses.append(expense)
        
        self.save_data()
    
    def save_data(self):
        data = {
            'expenses': self.expenses,
            'theme': self.current_theme
        }
        with open('premium_expenses.json', 'w') as f:
            json.dump(data, f, indent=2)

if __name__ == "__main__":
    root = tk.Tk()
    app = UltimateExpenseTracker(root)
    root.mainloop()