# Python Utilities and Unit Testing Project

## This repository contains a set of generic Python utility functions designed to assist in interacting with a GitHub organization client, along with comprehensive unit tests to ensure their correctness and reliability. This project adheres to strict coding standards and documentation requirements.

## Table of Contents

1. Project Description

2. Requirements

3. Project Structure

4. Setup and Installation

5. Usage

6. Testing

7. Code Style



## Project Description
This project focuses on developing robust and well-tested Python utility functions. It includes:

utils.py: A module containing reusable functions such as:

access_nested_map: For safely navigating nested dictionary-like structures.

get_json: For fetching and parsing JSON data from remote URLs.

memoize: A decorator for caching the results of method calls to improve performance.

test_utils.py: A module dedicated to unit testing the functions in utils.py using the unittest framework and parameterized for data-driven tests.

The project emphasizes adherence to Python best practices, including type annotations, comprehensive documentation, and code style guidelines.

## Requirements
All code in this repository must meet the following criteria:

Environment: Interpreted/compiled on Ubuntu 18.04 LTS using python3 (version 3.7).

File Endings: All files must end with a new line.

Shebang: The first line of all Python files must be #!/usr/bin/env python3.

README.md: A README.md file is mandatory at the root of the project folder.

Code Style: Code must adhere to pycodestyle style (version 2.5).

Executability: All Python files must be executable (chmod +x <file>).

Documentation:

All modules must have a documentation string (__doc__).

All classes must have a documentation string.

All functions (inside and outside a class) must have a documentation string.

Documentation strings must be real sentences explaining the purpose, not just single words.

Type Annotations: All functions and coroutines must be type-annotated.

Project Structure
.
├── README.md
├── utils.py
└── test_utils.py

README.md: This file, providing an overview of the project.

utils.py: Contains the core utility functions.

test_utils.py: Contains unit tests for the utils.py functions.

Setup and Installation
To set up this project in your Ubuntu 18.04 environment (e.g., ALX sandbox Webterm or VS Code Remote SSH):

Clone the repository:

git clone https://github.com/your-username/your-repo-name.git
cd your-repo-name # Navigate into the cloned directory

(Replace your-username and your-repo-name with your actual GitHub details.)

Ensure Python 3.7 is available:
Verify your Python version:

python3 --version

If it's not 3.7, ensure your environment is correctly configured (e.g., in the ALX sandbox, it should be pre-configured).

Install dependencies:
This project requires the requests and parameterized libraries.

pip3 install requests parameterized

Make Python files executable:

chmod +x utils.py
chmod +x test_utils.py

## Usage
The utils.py module provides functions that can be imported and used in other Python scripts. For example:

from utils import access_nested_map, get_json, memoize

# Example using access_nested_map
nested_data = {"user": {"profile": {"name": "Alice", "age": 30}}}
name = access_nested_map(nested_data, ("user", "profile", "name"))
print(f"User name: {name}")

# Example using get_json (requires internet access)
# github_api_url = "https://api.github.com/users/google"
# google_user_data = get_json(github_api_url)
# print(f"Google user info: {google_user_data.get('login')}")

# Example using memoize (see utils.py for class example)

## Testing
Unit tests are crucial for verifying the correctness of the utility functions.

To run all tests:

python3 -m unittest test_utils.py

This command will execute all test methods defined in test_utils.py and report the results.

Code Style
This project strictly follows the pycodestyle style guide.

To check code style:

pycodestyle utils.py test_utils.py

Any output indicates style violations that need to be addressed. A clean output means your code adheres to the style guide.