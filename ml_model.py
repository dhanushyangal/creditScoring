from web3 import Web3 # type: ignore
import json
import pandas as pd
from sklearn.model_selection import train_test_split # type: ignore
from sklearn.ensemble import RandomForestClassifier # type: ignore
from sklearn.metrics import accuracy_score # type: ignore

# Connect to the local Ganache blockchain
web3 = Web3(Web3.HTTPProvider('http://localhost:7545'))

# Check connection
if web3.isConnected():
    print("Connected to blockchain")
else:
    print("Failed to connect to blockchain")

# Load smart contract ABI
with open('build/contracts/CreditScoring.json') as f:
    contract_json = json.load(f)
    contract_abi = contract_json['abi']

# Set the contract address (replace with your deployed contract address)
contract_address = '0xYourContractAddressHere'

# Get contract instance
contract = web3.eth.contract(address=contract_address, abi=contract_abi)

def get_credit_report(user_address):
    credit_report = contract.functions.creditReports(user_address).call()
    return credit_report

def get_bank_statements(user_address):
    statements = contract.functions.bankStatements(user_address).call()
    return statements

def get_loan_histories(user_address):
    loans = contract.functions.loanHistories(user_address).call()
    return loans

user_address = '0xUserAddressHere'  # Replace with a valid user address
credit_report = get_credit_report(user_address)
bank_statements = get_bank_statements(user_address)
loan_histories = get_loan_histories(user_address)

# Example data processing (adjust based on actual data structure)
credit_report_df = pd.DataFrame([credit_report], columns=['CreditScore', 'CreditBureau', 'ReportDate'])
bank_statements_df = pd.DataFrame(bank_statements, columns=['TransactionID', 'Date', 'Description', 'Amount', 'Type'])
loan_histories_df = pd.DataFrame(loan_histories, columns=['LoanID', 'LoanAmount', 'StartDate', 'EndDate', 'Status', 'RepaymentAmount'])

# Combine data into a single DataFrame
combined_df = pd.concat([credit_report_df, bank_statements_df, loan_histories_df], axis=1)

# Preprocess data (dummy example, adjust as needed)
X = combined_df.drop(columns=['CreditScore'])  # Features
y = combined_df['CreditScore']  # Target variable

# Split data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train a RandomForest model
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# Make predictions
y_pred = model.predict(X_test)

# Evaluate the model
accuracy = accuracy_score(y_test, y_pred)
print(f'Model Accuracy: {accuracy * 100:.2f}%')

# Example new data (replace with actual data)
new_data = pd.DataFrame([{
    'CreditBureau': 'Experian',
    'ReportDate': '2023-07-01',
    'TransactionID': 'TX001',
    'Date': '2023-06-10',
    'Description': 'Grocery Store',
    'Amount': -50,
    'Type': 'Debit',
    'LoanID': 'LN001',
    'LoanAmount': 10000,
    'StartDate': '2022-01-01',
    'EndDate': '2023-01-01',
    'Status': 'Repaid',
    'RepaymentAmount': 10500
}])

# Make predictions
predictions = model.predict(new_data)
print("Predicted Credit Score:", predictions)
