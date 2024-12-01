from dotenv import load_dotenv
import urllib.request
import argparse
import os


def get_input_file(year: int, day: int) -> str:
    '''Returns the input file for the given day'''
    load_dotenv()
    req = urllib.request.Request(f'http://adventofcode.com/{year}/day/{day}/input')
    req.add_header('cookie', f'session={os.getenv("SESSION")}')
    response = urllib.request.urlopen(req)
    return response.read().decode('utf-8')


def parse_args():
    '''Parses the arguments'''
    parser = argparse.ArgumentParser()
    parser.add_argument('year', type=int, help='The year to run')
    parser.add_argument('day', type=int, help='The day to run')
    return parser.parse_args()


def get_template_file() -> str:
    '''Returns the template file for the given day'''
    with open('template.py') as f:
        template = f.read()
    return template


def generate_template(year: int, day: int, input_file: str, template_file: str):
    '''Generates the template file for the given day'''
    os.makedirs(f'{year}', exist_ok=True)
    os.makedirs(f'{year}/day{day}', exist_ok=True)
    with open(f'{year}/day{day}/main.py', 'w') as f:
        f.write(template_file)
    with open(f'{year}/day{day}/input.txt', 'w') as f:
        f.write(input_file)


def main():
    '''Parses the input and creates a template'''
    args = parse_args()
    day = args.day
    year = args.year
    input_file = get_input_file(year, day)
    template_file = get_template_file()
    generate_template(year, day, input_file, template_file)


if __name__ == "__main__":
    main()
