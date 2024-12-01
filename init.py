from dotenv import load_dotenv
import urllib.request
import argparse
import os


def get_input_file(day: int) -> str:
    '''Returns the input file for the given day'''
    load_dotenv()
    req = urllib.request.Request(f'http://adventofcode.com/2024/day/{day}/input')
    req.add_header('cookie', f'session={os.getenv("SESSION")}')
    response = urllib.request.urlopen(req)
    return response.read().decode('utf-8')


def parse_args():
    '''Parses the arguments'''
    parser = argparse.ArgumentParser()
    parser.add_argument('day', type=int, help='The day to run')
    return parser.parse_args()


def get_template_file(day: int) -> str:
    '''Returns the template file for the given day'''
    with open('template.py') as f:
        template = f.read()
    return template


def generate_template(day: int, input_file: str, template_file: str):
    '''Generates the template file for the given day'''
    os.makedirs(f'day{day}', exist_ok=True)
    with open(f'day{day}/main.py', 'w') as f:
        f.write(template_file)
    with open(f'day{day}/input.txt', 'w') as f:
        f.write(input_file)


def main():
    '''Parses the input and creates a template'''
    args = parse_args()
    day = args.day
    input_file = get_input_file(day)
    template_file = get_template_file(day)
    generate_template(day, input_file, template_file)


if __name__ == "__main__":
    main()
