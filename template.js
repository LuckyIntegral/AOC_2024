'use strict';

const minimist = require('minimist');
const fs = require('fs');
const path = require('path');

const INPUT_FILE = path.join(__dirname, 'input.txt');
const TEST_FILE = path.join(__dirname, 'test.txt');

function parseInput(content) {
    return content.split('\n');
}

async function silver(content, test = false) {
    let data = parseInput(content);
    return 42;
}

async function gold(content, test = false) {
    let data = parseInput(content);
    return 42;
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
