'use strict';

const minimist = require('minimist');
const fs = require('fs');
const path = require('path');

const INPUT_FILE = path.join(__dirname, 'input.txt');
const TEST_FILE = path.join(__dirname, 'test.txt');

function parseInput(content) {
    const sections = content.trim().split('\n\n');
    const tiles = sections[0].split(',').map(Number);
    const boards = [];

    for (const section of sections.slice(1)) {
        const board = section.split('\n').map(line =>
            line.trim().split(/\s+/).map(Number)
        );
        boards.push(board);
    }

    return { tiles, boards };
}

function isBingo(board) {
    let bingo = false;

    for (let i = 0; i < board.length; i++) {
        if (board[i].every(cell => typeof cell === 'string')) {
            bingo = true;
        }
        let valid = true;
        for (let j = 0; j < board.length; j++) {
            if (typeof board[j][i] === 'number') {
                valid = false;
            }
        }
        if (valid) {
            bingo = true;
        }
    }

    return bingo;
}

async function silver(content, test = false) {
    let data = parseInput(content);

    for (const number of data.tiles) {
        for (let board of data.boards) {
            board.forEach(row => {
                if (row.includes(number)) {
                    row[row.indexOf(number)] = `${number}`;
                }
            });

            if (isBingo(board)) {
                return number * board
                    .flat()
                    .map(cell => typeof cell === 'string' ? 0 : cell)
                    .reduce((a, b) => a + b)
            }
        }
    }
}

async function gold(content, test = false) {
    let data = parseInput(content);
    let last = 0;

    for (const number of data.tiles) {
        for (let board of data.boards) {
            board.forEach(row => {
                if (row.includes(number)) {
                    row[row.indexOf(number)] = `${number}`;
                }
            });
        }

        let buffer = [];
        for (let i = 0; i < data.boards.length; i++) {
            if (isBingo(data.boards[i])) {
                last = number * data.boards[i]
                    .flat()
                    .map(cell => typeof cell === 'string' ? 0 : cell)
                    .reduce((a, b) => a + b)
            } else {
                buffer.push(data.boards[i]);
            }
        }

        if (buffer.length === 0) {
            break;
        }

        data.boards = buffer;
    }
    return last;
}

function parseArgs() {
    return minimist(process.argv.slice(2), {
        boolean: 'debug',
        unknown: (arg) => {
            console.error(`Unknown argument: ${arg}`);
            process.exit(1);
        },
    });
}

async function main() {
    const args = parseArgs();
    let content = fs.readFileSync(TEST_FILE, 'utf-8');

    const [silverTest, goldTest] = await Promise.all([
        silver(content, true),
        gold(content, true)
    ]);

    console.log(`Silver test: ${silverTest}`);
    console.log(`Gold test:   ${goldTest}`);

    if (!args.debug) {
        content = fs.readFileSync(INPUT_FILE, 'utf-8');

        const [silverResult, goldResult] = await Promise.all([
            silver(content),
            gold(content)
        ]);

        console.log(`Silver:      ${silverResult}`);
        console.log(`Gold:        ${goldResult}`);
    }
}

main();
