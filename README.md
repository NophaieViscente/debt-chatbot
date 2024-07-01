# Debt Chatbot Application
## Overview
This project is a chatbot application designed to assist customers by providing information regarding their debts. 
The chatbot verifies the customer's CPF (Brazilian Individual Taxpayer Registry) and date of birth before delivering debt details. 
This ensures that sensitive information is only shared with the correct individual.

## Features
Introduction and Greeting: The chatbot starts by introducing itself and welcoming the user.
*CPF Validation*: When a customer requests debt information, the bot prompts for the CPF and validates it.
*Date of Birth Validation*: Upon successful CPF validation, the bot requests and validates the customer's date of birth.
*Debt Information Retrieval*: If both CPF and date of birth are valid, the bot retrieves and displays the customer's debt information.
*Additional Assistance*: If the CPF or date of birth is invalid, the bot politely asks if it can assist with anything else.

## Technologies Used
*Python*: The core programming language used to develop the chatbot.
*Langchain*: Utilized for create prompts and tools.
*Langgraph: Utilized for manage flow and state conversation.
*SQLite*: A lightweight database used for storing and retrieving customer data securely.

## Project Structure
```
src/
├── utils/
│   ├── __pycache__/
│   ├── agent.py
│   ├── clean_data.py
│   ├── graph.py
│   ├── load_data.py
│   ├── sql_handler.py
│   ├── state.py
│   ├── tools.py
│   ├── utilities.py
├── chatbot.py
├── create_database_from_excel.py
.gitignore
README.md
requirements.txt
```

## File Descriptions
**src/**: Main directory containing the source code.
**utils/**: Directory containing utility modules and helper scripts.
**agent.py**: Implementation of the main chatbot agent.
**clean_data.py**: Script for data cleaning.
**graph.py**: Module for generating graphs.
**load_data.py**: Script for loading data.
**sql_handler.py**: Module for handling SQL operations to insert data on database.
**state.py**: Manages the state of the chatbot.
**tools.py**: Additional tools used by the project.
**utilities.py**: General utility functions.
**chatbot.py**: Main chatbot script.
**create_database_from_excel.py**: Script for creating a database from an csv file.
**.gitignore**: Specifies which files and directories to ignore in Git.
**README.md**: This documentation file.
**requirements.txt**: List of project dependencies.

## Getting Started
### Prerequisites

Python 3.8 or higher

SQLite
### Installation

Clone the repository:
```git clone https://github.com/yourusername/debt-chatbot.git```

Navigate to the project directory:
```cd debt-chatbot```

Install the required dependencies:
```pip install -r requirements.txt```

## Running the Application
Set up the SQLite database with the required schema (see database_setup.sql for reference).

Start the chatbot application:
```python chatbot.py```

## Usage
Interact with the chatbot through the command line interface. Follow the prompts to enter your CPF and date of birth to retrieve debt information.
