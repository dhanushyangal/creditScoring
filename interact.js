const Web3 = require('web3');
const contract = require('@truffle/contract');
const CreditScoringArtifact = require('./build/contracts/CreditScoring.json');

const web3 = new Web3('http://localhost:7545'); // Ganache local blockchain
const CreditScoring = contract(CreditScoringArtifact);
CreditScoring.setProvider(web3.currentProvider);

const main = async () => {
  const accounts = await web3.eth.getAccounts();
  const creditScoringInstance = await CreditScoring.deployed();

  // Set a credit report
  await creditScoringInstance.setCreditReport(accounts[0], 720, 'Experian', '2023-07-01', { from: accounts[0] });

  // Add a bank statement
  await creditScoringInstance.addBankStatement(accounts[0], 'TX001', '2023-06-10', 'Grocery Store', -50, 'Debit', { from: accounts[0] });

  // Add a loan history
  await creditScoringInstance.addLoanHistory(accounts[0], 'LN001', 10000, '2022-01-01', '2023-01-01', 'Repaid', 10500, { from: accounts[0] });

  // Retrieve data
  const creditReport = await creditScoringInstance.creditReports(accounts[0]);
  console.log('Credit Report:', creditReport);

  const bankStatements = await creditScoringInstance.bankStatements(accounts[0]);
  console.log('Bank Statements:', bankStatements);

  const loanHistories = await creditScoringInstance.loanHistories(accounts[0]);
  console.log('Loan Histories:', loanHistories);
};

main().catch((err) => console.error(err));
