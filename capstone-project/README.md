# Loan Risk Analysis Dashboard

An interactive web application for analyzing loan data and calculating risk ratings.

## Features

- Interactive data visualization dashboard
- Risk rating calculator with machine learning
- Currency conversion (EUR to USD)
- Data filtering and analysis
- CSV export functionality

## Prerequisites

- Python 3.8+
- Windows/Linux/Mac OS
- Excel files with loan data

## Project Structure

```
capstone-project/
├── input/              # Input data directory
│   ├── Dataset1.xlsx
│   └── Dataset2.xlsx
├── output/             # Processed data output
├── src/               
│   ├── app.py         # Streamlit dashboard
│   ├── main.py        # Data processing script
│   └── utils/         # Helper functions
├── .env.template      # Environment template
└── requirements.txt   # Project dependencies
```

## Quick Start

1. **Clone and Setup**
   ```bash
   git clone <repository-url>
   cd capstone-project
   python -m venv venv
   .\venv\Scripts\activate
   pip install -r requirements.txt
   ```

2. **Environment Configuration**
   ```bash
   copy .env.template .env
   # Edit .env with your configurations
   ```

3. **Run Application**
   ```bash
   python -m streamlit run app.py 
   ```

## Data Requirements

Required Excel columns:
- Age
- Gender
- Education_Level
- Income (EUR/USD)
- Credit_Score
- Loan_Purpose
- Debt_to_Income_Ratio
- Loan_Amount (EUR/USD)

## Usage

### Dashboard
1. Upload Excel file through web interface
2. Use sidebar filters for data analysis
3. View interactive visualizations
4. Download processed data as CSV

### Risk Calculator
1. Input loan application details
2. Get instant risk assessment
3. View detailed risk analysis

## Development

### Running Tests
```bash
pytest tests/
```

### Adding New Features
1. Create feature branch
2. Implement changes
3. Add tests
4. Submit pull request

## Troubleshooting

Common issues and solutions:
- **Streamlit not found**: Activate virtual environment
- **Data loading errors**: Check input file format
- **Currency conversion issues**: Verify amount format
