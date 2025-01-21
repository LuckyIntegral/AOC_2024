from dotenv import load_dotenv
from bs4 import BeautifulSoup
import requests
import argparse
import time
import os


URI_INPUT = 'https://adventofcode.com/{year}/day/{day}/input'
URI_REFER = 'https://adventofcode.com/{year}/day/{day}'
URI_SUBMIT = 'https://adventofcode.com/{year}/day/{day}/answer'
USER_AGENT = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36'
LOCAL_PATH = os.path.dirname(os.path.abspath(__file__))
CACHE_FILE = os.path.join(LOCAL_PATH, '.cache')
EXECUTABLES = {'py': 'python3.11', 'js': 'node'}


class AdventOfCode:
    def __init__(self, year: int, day: int, lang: str, session_id: str):
        '''Initializes the class with the year and day'''
        self.year = year
        self.day = day
        self.lang = lang
        self.executable = EXECUTABLES[lang]
        self.cookies = session_id
        self.start = time.time()
        self.submissions = []
        self.silver = None
        self.golden = None
        self.optional_write(CACHE_FILE, '')

    def __del__(self):
        '''Destructor'''
        def stringify(status: str) -> str:
            return time.strftime('%H:%M:%S', time.gmtime(status))
        print(f"Time passed: {stringify(time.time() - self.start)} seconds")
        print("Submissions:")
        for timestamp, status in self.submissions:
            print(f"{stringify(timestamp - self.start)}: {status}")

    def lookup_cache(self, key: str) -> bool:
        '''Looks up the cache for the key'''
        with open(CACHE_FILE) as f:
            content = f.readlines()
        for line in content:
            if key in line:
                return True
        return False

    def write_cache(self, key: str):
        '''Writes the key to the cache'''
        with open(CACHE_FILE, 'a') as f:
            f.write(key + '\n')

    def http_error(self, message: str, response: requests.Response):
        '''Prints an error message and exits'''
        print(message)
        print("Status code: ", response.status_code)
        print(response.content)
        exit(1)

    def submit(self, part: str, answer: str):
        '''Solves the problem and submits the answer'''
        if self.lookup_cache(f'{self.year}-{self.day}-{part}={answer}'):
            print("Already submitted")
            return

        response = requests.post(
            URI_SUBMIT.format(year=self.year, day=self.day),
            cookies={'session': self.cookies},
            data={'level': part, 'answer': answer},
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
            self.submissions.append(
                (time.time(), f'Correct solution for part {part}')
            )
            self.write_cache(f'{self.year}-{self.day}-{part}={answer}')
        elif "That's not the right answer" in content:
            print(f"Wrong answer: your answer is {answer}")
            self.submissions.append(
                (time.time(), f'Wrong solution for part {part}')
            )
            self.write_cache(f'{self.year}-{self.day}-{part}={answer}')
        elif "To play, please identify yourself" in content:
            print("Invalid cookie")
            self.submissions.append(
                (time.time(), f'Invalid cookie for part {part}')
            )
        elif "You gave an answer too recently" in content:
            print("You gave an answer too recently, please wait a few seconds")
            self.submissions.append(
                (time.time(), f'Timeout before submitting part {part}')
            )
        else:
            print("Unexpected response:")
            print(content)
            self.submissions.append(
                (time.time(), f'Unexpected response for part {part}')
            )

    def get_input(self) -> str:
        '''Returns the input file for the given day'''
        response = requests.get(
            URI_INPUT.format(year=self.year, day=self.day),
            cookies={'session': self.cookies},
            headers={'User-Agent': USER_AGENT},
        )

        if response.status_code != 200:
            self.http_error('Submission failed', response)

        return response.text

    def scrap_test(self) -> str:
        '''Returns the test file for the given day'''
        response = requests.get(
            URI_REFER.format(year=self.year, day=self.day),
            cookies={'session': self.cookies},
            headers={'User-Agent': USER_AGENT},
        )

        if response.status_code != 200:
            self.http_error('Submission failed', response)

        soup = BeautifulSoup(response.text, 'html.parser')
        pre_tags = soup.find('pre')
        if not pre_tags:
            print('No test cases found')
            return ''
        return pre_tags.text

    def get_template_content(self) -> str:
        '''Returns the template file for the given day'''
        with open(f'template.{self.lang}') as f:
            template = f.read()
        return template

    def optional_write(self, file: str, content: str):
        '''Writes the content to the file if it does not exist'''
        if not os.path.exists(file):
            with open(file, 'w') as f:
                f.write(content)

    def generate_template(self):
        '''Generates the template file for the given day'''

        input_file = self.get_input()
        test_file = self.scrap_test()
        template = self.get_template_content()

        os.makedirs(f'{self.year}/day{self.day}', exist_ok=True)

        self.optional_write(f'{self.year}/day{self.day}/main.{self.lang}', template)
        self.optional_write(f'{self.year}/day{self.day}/input.txt', input_file)
        self.optional_write(f'{self.year}/day{self.day}/test.txt', test_file)

    def run_solution(self, debug: bool = False):
        '''Runs the subprocess
        debug: runs the test samples only
        '''
        command = f'{self.executable} {self.year}/day{self.day}/main.{self.lang}'
        if debug:
            command += ' --debug'
        output = os.popen(command).readlines()
        for line in output:
            line = line.strip('\n')
            print(line)
            if 'Silver:' in line:
                self.silver = line.split()[-1]
            elif 'Gold:' in line:
                self.golden = line.split()[-1]

    def interactive(self):
        '''Interacts with the user'''
        print('Advent of Code')
        print(f'https://adventofcode.com/{self.year}/day/{self.day}')
        print()
        print('Options:')
        print('p: print the solution')
        print('d: debug the solution (run the test samples only)')
        print('s: submit the first solution (silver star)')
        print('g: submit the second solution (golden star)')
        print('c: clear the screen')
        print()

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
                elif user == 'd':
                    self.run_solution(debug=True)
                elif user == 'c':
                    os.system('clear')
                else:
                    print('Invalid option')
        except EOFError:
            print('\nBye')
        except KeyboardInterrupt:
            print('\nBye')
        except Exception as e:
            print(e.with_traceback())


def validate_env():
    '''Validates the environment variables'''
    load_dotenv()
    if not os.getenv('SESSION'):
        print('SESSION environment variable not found in .env file')
        exit(1)


def parse_args():
    '''Parses the arguments'''
    parser = argparse.ArgumentParser()
    parser.add_argument('lang', choices=['py', 'js'], help='The template language')
    parser.add_argument('year', type=int, help='The year to run')
    parser.add_argument('day', type=int, help='The day to run')
    return parser.parse_args()


def main():
    '''Parses the input and creates a template'''
    validate_env()
    args = parse_args()
    aoc = AdventOfCode(args.year, args.day, args.lang, os.getenv('SESSION'))
    aoc.generate_template()
    aoc.interactive()


if __name__ == "__main__":
    main()
