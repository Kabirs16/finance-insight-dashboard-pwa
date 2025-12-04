import 'package:flutter/material.dart';
import 'package:fl_chart/fl_chart.dart';

void main() {
  runApp(const FinanceApp());
}

class FinanceApp extends StatelessWidget {
  const FinanceApp({Key? key}) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Finance Manager',
      theme: ThemeData(
        primarySwatch: Colors.deepPurple,
        useMaterial3: true,
      ),
      home: const FinanceDashboard(),
    );
  }
}

class FinanceDashboard extends StatefulWidget {
  const FinanceDashboard({Key? key}) : super(key: key);

  @override
  State<FinanceDashboard> createState() => _FinanceDashboardState();
}

class _FinanceDashboardState extends State<FinanceDashboard>
    with SingleTickerProviderStateMixin {
  late TabController _tabController;

  // Sample data
  double totalIncome = 65000;
  double totalExpenses = 12500;
  double balance = 52500;

  final List<Map<String, dynamic>> expenses = [
    {'category': 'Groceries', 'amount': 5000},
    {'category': 'Utilities', 'amount': 2000},
    {'category': 'Transport', 'amount': 1500},
    {'category': 'Entertainment', 'amount': 3000},
    {'category': 'Health', 'amount': 1000},
  ];

  final List<Map<String, dynamic>> income = [
    {'source': 'Salary', 'amount': 50000},
    {'source': 'Freelance', 'amount': 15000},
  ];

  final List<Map<String, dynamic>> products = [
    {
      'id': 1,
      'name': 'Laptop',
      'price': 45000,
      'quantity': 2,
      'category': 'Electronics'
    },
    {
      'id': 2,
      'name': 'Phone',
      'price': 25000,
      'quantity': 5,
      'category': 'Electronics'
    },
    {
      'id': 3,
      'name': 'Coffee',
      'price': 200,
      'quantity': 50,
      'category': 'Food'
    },
  ];

  @override
  void initState() {
    super.initState();
    _tabController = TabController(length: 4, vsync: this);
  }

  @override
  void dispose() {
    _tabController.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('💰 Finance Manager'),
        centerTitle: true,
        elevation: 0,
        bottom: TabBar(
          controller: _tabController,
          tabs: const [
            Tab(text: 'Dashboard'),
            Tab(text: 'Expenses'),
            Tab(text: 'Income'),
            Tab(text: 'Products'),
          ],
        ),
      ),
      body: TabBarView(
        controller: _tabController,
        children: [
          _buildDashboard(),
          _buildExpenses(),
          _buildIncome(),
          _buildProducts(),
        ],
      ),
    );
  }

  Widget _buildDashboard() {
    return SingleChildScrollView(
      padding: const EdgeInsets.all(16),
      child: Column(
        children: [
          // KPI Cards
          GridView.count(
            crossAxisCount: 2,
            crossAxisSpacing: 16,
            mainAxisSpacing: 16,
            shrinkWrap: true,
            physics: const NeverScrollableScrollPhysics(),
            children: [
              _buildKPICard(
                'Total Income',
                '₹${totalIncome.toStringAsFixed(0)}',
                Colors.green,
              ),
              _buildKPICard(
                'Total Expenses',
                '₹${totalExpenses.toStringAsFixed(0)}',
                Colors.red,
              ),
              _buildKPICard(
                'Balance',
                '₹${balance.toStringAsFixed(0)}',
                Colors.blue,
              ),
              _buildKPICard(
                'Savings Rate',
                '${((balance / totalIncome) * 100).toStringAsFixed(1)}%',
                Colors.orange,
              ),
            ],
          ),
          const SizedBox(height: 24),

          // Charts Section
          Card(
            elevation: 4,
            shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(12)),
            child: Padding(
              padding: const EdgeInsets.all(16),
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  const Text(
                    'Expense Breakdown',
                    style: TextStyle(fontSize: 18, fontWeight: FontWeight.bold),
                  ),
                  const SizedBox(height: 16),
                  SizedBox(
                    height: 250,
                    child: PieChart(
                      PieChartData(
                        sections: _buildExpenseSections(),
                        centerSpaceRadius: 40,
                        sectionsSpace: 0,
                      ),
                    ),
                  ),
                ],
              ),
            ),
          ),
          const SizedBox(height: 16),

          Card(
            elevation: 4,
            shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(12)),
            child: Padding(
              padding: const EdgeInsets.all(16),
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  const Text(
                    'Income vs Expenses',
                    style: TextStyle(fontSize: 18, fontWeight: FontWeight.bold),
                  ),
                  const SizedBox(height: 16),
                  SizedBox(
                    height: 250,
                    child: BarChart(
                      BarChartData(
                        barGroups: [
                          BarChartGroupData(
                            x: 0,
                            barRods: [
                              BarChartRodData(
                                toY: totalIncome / 1000,
                                color: Colors.green,
                              ),
                              BarChartRodData(
                                toY: totalExpenses / 1000,
                                color: Colors.red,
                              ),
                            ],
                          ),
                        ],
                      ),
                    ),
                  ),
                ],
              ),
            ),
          ),
        ],
      ),
    );
  }

  Widget _buildExpenses() {
    return ListView.builder(
      padding: const EdgeInsets.all(16),
      itemCount: expenses.length,
      itemBuilder: (context, index) {
        final expense = expenses[index];
        return Card(
          margin: const EdgeInsets.only(bottom: 12),
          child: ListTile(
            leading: CircleAvatar(
              backgroundColor: Colors.red.shade100,
              child: const Icon(Icons.trending_down, color: Colors.red),
            ),
            title: Text(expense['category']),
            subtitle: Text('₹${expense['amount']}'),
            trailing: IconButton(
              icon: const Icon(Icons.delete, color: Colors.red),
              onPressed: () {
                setState(() {
                  expenses.removeAt(index);
                });
              },
            ),
          ),
        );
      },
    );
  }

  Widget _buildIncome() {
    return ListView.builder(
      padding: const EdgeInsets.all(16),
      itemCount: income.length,
      itemBuilder: (context, index) {
        final inc = income[index];
        return Card(
          margin: const EdgeInsets.only(bottom: 12),
          child: ListTile(
            leading: CircleAvatar(
              backgroundColor: Colors.green.shade100,
              child: const Icon(Icons.trending_up, color: Colors.green),
            ),
            title: Text(inc['source']),
            subtitle: Text('₹${inc['amount']}'),
            trailing: IconButton(
              icon: const Icon(Icons.delete, color: Colors.red),
              onPressed: () {
                setState(() {
                  income.removeAt(index);
                });
              },
            ),
          ),
        );
      },
    );
  }

  Widget _buildProducts() {
    return ListView.builder(
      padding: const EdgeInsets.all(16),
      itemCount: products.length,
      itemBuilder: (context, index) {
        final product = products[index];
        return Card(
          margin: const EdgeInsets.only(bottom: 12),
          child: ListTile(
            leading: CircleAvatar(
              backgroundColor: Colors.blue.shade100,
              child: const Icon(Icons.shopping_bag, color: Colors.blue),
            ),
            title: Text(product['name']),
            subtitle: Text(
              '₹${product['price']} × ${product['quantity']}',
            ),
            trailing: ElevatedButton(
              onPressed: () {
                ScaffoldMessenger.of(context).showSnackBar(
                  SnackBar(
                    content: Text('${product['name']} added to cart'),
                    duration: const Duration(seconds: 1),
                  ),
                );
              },
              child: const Text('Add'),
            ),
          ),
        );
      },
    );
  }

  Widget _buildKPICard(String title, String value, Color color) {
    return Card(
      elevation: 4,
      shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(12)),
      child: Container(
        decoration: BoxDecoration(
          borderRadius: BorderRadius.circular(12),
          gradient: LinearGradient(
            colors: [color, color.withOpacity(0.7)],
            begin: Alignment.topLeft,
            end: Alignment.bottomRight,
          ),
        ),
        padding: const EdgeInsets.all(16),
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            Text(
              title,
              style: const TextStyle(
                color: Colors.white70,
                fontSize: 12,
                fontWeight: FontWeight.w500,
              ),
            ),
            const SizedBox(height: 8),
            Text(
              value,
              style: const TextStyle(
                color: Colors.white,
                fontSize: 20,
                fontWeight: FontWeight.bold,
              ),
              textAlign: TextAlign.center,
            ),
          ],
        ),
      ),
    );
  }

  List<PieChartSectionData> _buildExpenseSections() {
    final total = expenses.fold<double>(0, (sum, item) => sum + item['amount']);
    final colors = [
      Colors.red,
      Colors.orange,
      Colors.yellow,
      Colors.green,
      Colors.blue,
    ];

    return List.generate(expenses.length, (index) {
      final expense = expenses[index];
      final percentage = (expense['amount'] / total) * 100;

      return PieChartSectionData(
        color: colors[index % colors.length],
        value: expense['amount'].toDouble(),
        title: '${percentage.toStringAsFixed(1)}%',
        radius: 80,
        titleStyle: const TextStyle(
          fontSize: 12,
          fontWeight: FontWeight.bold,
          color: Colors.white,
        ),
      );
    });
  }
}
