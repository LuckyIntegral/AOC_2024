from dotenv import load_dotenv
from bs4 import BeautifulSoup
import requests
import argparse
import time
import sys
import os


URI_INPUT = 'https://adventofcode.com/{year}/day/{day}/input'
URI_REFER = 'https://adventofcode.com/{year}/day/{day}'
URI_SUBMIT = 'https://adventofcode.com/{year}/day/{day}/answer'
USER_AGENT = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36'


class AdventOfCode:
    def __init__(self, year: int, day: int, session_id: str):
        '''Initializes the class with the year and day'''
        self.year = year
        self.day = day
        self.cookies = session_id
        self.start = time.time()
        self.submissions = []
        self.silver = None
        self.golden = None


    def __del__(self):
        '''Destructor'''
        print(f"Time passed: {time.time() - self.start:.2f} seconds")
        print("Submissions:")
        for timestamp, status in self.submissions:
            print(f"{time.time() - timestamp:.2f}: {status}")


    def http_error(self, message: str, response: requests.Response):
        '''Prints an error message and exits'''
        print(message)
        print("Status code: ", response.status_code)
        print(response.content)
        exit(1)


    def submit(self, part: str, answer: str):
        '''Solves the problem and submits the answer'''
        response = requests.post(URI_SUBMIT.format(year=self.year, day=self.day),
            cookies={'session': self.cookies},
            data = {'level': part, 'answer': answer},
            headers={
                'User-Agent': USER_AGENT,
                'Referer': URI_REFER.format(year=self.year, day=self.day)
            },
        )

        if response.status_code != 200:
            self.http_error('Submission failed', response)

        content = response.content.decode()
        if "That's the right answer!" in content:
            print("Correct answer")
            self.submissions.append((time.time(), f'Correct solution for part {part}'))
        elif "That's not the right answer" in content:
            print("Wrong answer: your answer is", content.split("your answer is ")[1].split(".", 1)[0])
            self.submissions.append((time.time(), f'Wrong solution for part {part}'))
        elif "To play, please identify yourself" in content:
            print("Cookie expired")
            self.submissions.append((time.time(), f'Cookie expired before submitting part {part}'))
        elif "You gave an answer too recently" in content:
            print("You gave an answer too recently")
            self.submissions.append((time.time(), f'Timeout before submitting part {part}'))
        else:
            print("Unexpected response:")
            print(content)
            self.submissions.append((time.time(), f'Unexpected response for part {part}'))


    def get_input(self) -> str:
        '''Returns the input file for the given day'''
        response = requests.get(URI_INPUT.format(year=self.year, day=self.day),
            cookies={'session': self.cookies},
            headers={'User-Agent': USER_AGENT},
        )

        if response.status_code != 200:
            self.http_error('Submission failed', response)

        return response.text


    def scrap_test(self) -> str:
        '''Returns the test file for the given day'''
        response = requests.get(URI_REFER.format(year=self.year, day=self.day),
            cookies={'session': self.cookies},
            headers={'User-Agent': USER_AGENT},
        )

        if response.status_code != 200:
            self.http_error('Submission failed', response)

        soup = BeautifulSoup(response.text, 'html.parser')
        pre_tags = soup.find('pre')
        return pre_tags.text


    def get_template_file(self) -> str:
        '''Returns the template file for the given day'''
        with open('template.py') as f:
            template = f.read()
        return template


    def generate_template(self):
        '''Generates the template file for the given day'''
        def optional_write(file: str, content: str):
            if not os.path.exists(file):
                with open(file, 'w') as f:
                    f.write(content)

        input_file = self.get_input()
        test_file = self.scrap_test()
        template_file = self.get_template_file()

        os.makedirs(f'{self.year}/day{self.day}', exist_ok=True)

        optional_write(f'{self.year}/day{self.day}/main.py', template_file)
        optional_write(f'{self.year}/day{self.day}/input.txt', input_file)
        optional_write(f'{self.year}/day{self.day}/test.txt', test_file)


    def run_solution(self):
        '''Runs the subprocess'''
        output = os.popen(f'{sys.executable} {self.year}/day{self.day}/main.py').readlines()
        for line in output:
            line = line.strip()
            print(line)
            if 'Silver' in line:
                self.silver = int(line.split()[-1])
            elif 'Gold' in line:
                self.golden = int(line.split()[-1])


    def interactive(self):
        '''Interacts with the user'''
        print('Options:')
        print('p: print the solution')
        print('s: submit the first solution')
        print('g: submit the second solution')

        try:
            while True:
                user = input('>')
                if user == 'p':
                    self.run_solution()
                elif user == 's':
                    if self.silver is None:
                        print('Run the solution first')
                        self.run_solution()
                    self.submit('1', str(self.silver))
                elif user == 'g':
                    if self.golden is None:
                        print('Run the solution first')
                        self.run_solution()
                    self.submit('2', str(self.golden))
                else:
                    print('Invalid option')
        except EOFError:
            print('\nBye')
        except KeyboardInterrupt:
            print('\nBye')
        except Exception as e:
            print(e.with_traceback())


def parse_args():
    '''Parses the arguments'''
    parser = argparse.ArgumentParser()
    parser.add_argument('year', type=int, help='The year to run')
    parser.add_argument('day', type=int, help='The day to run')
    return parser.parse_args()


def main():
    '''Parses the input and creates a template'''
    args = parse_args()
    aoc = AdventOfCode(args.year, args.day, os.getenv('SESSION'))
    aoc.generate_template()
    aoc.interactive()


if __name__ == "__main__":
    load_dotenv()
    if not os.getenv('SESSION'):
        print('SESSION environment variable not found in .env file')
        exit(1)
    main()
