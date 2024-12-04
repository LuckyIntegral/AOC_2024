# Advent of Code Template Generator

This script generates a template for solving Advent of Code problems. It fetches the input and test data for a given year and day, and creates the necessary files to start solving the problem.

## Usage
To use the script, run the following command:

```sh
python init.py <year> <day>
```

Replace `<year>` with the year of the Advent of Code event and `<day>` with the day of the problem you want to solve.

## Requirements
 - Python 3.6 or higher
 - requests library
 - beautifulsoup4 library
 - python-dotenv library

You can install the required libraries using pip:

```sh
pip install -r requirements.txt
```

## Environment Variables
Create a `.env` file in the same directory as `init.py` with the following content:
```
SESSION=<your_session_cookie>
```

Replace `<your_session_cookie>` with your actual session cookie from the Advent of Code website.

## How It Works
The script performs the following steps:
1. Validates the environment variables.
2. Generates the template files for the given day.
3. Interacts with the user to run the solution and submit the answers.

## Example
To generate the template for December 1, 2021, run:

```sh
python init.py 2021 1
```

This will create the necessary files and directories for solving the problem

## Contributing
If you find a bug or have a feature suggestion, **pull requests** are welcome. Please ensure your code follows the project's coding standards and includes appropriate tests.
