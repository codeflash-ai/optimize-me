# CodeFlash Optimize-Me

**Ship fast code from day one.** This repo lets you experience AI-powered code optimization across Python, Java, and JavaScript/TypeScript.

## What is this repo?

This repository contains intentionally unoptimized code in multiple languages, perfect for experiencing Codeflash in action. Fork it, run Codeflash, and watch as it automatically discovers optimizations and opens Pull Requests while verifying the optimized code works exactly the same as the original.

## What is Codeflash?

Codeflash is an AI-powered code optimizer that automatically finds the most performant version of your code through intelligent benchmarking — while verifying it's still correct.

Leading engineering teams at [Pydantic](https://pydantic.dev/), [Langflow](https://langflow.org/), and [Roboflow](https://roboflow.com) trust Codeflash to ship expert-level, high-performance code.

## Project Structure

```
optimize-me/
├── pyproject.toml                # Python config (includes codeflash settings)
├── src/                          # Python source code
│   ├── algorithms/               # Sorting, search, text analysis, etc.
│   ├── data_processing/          # DataFrame and series operations
│   ├── math/                     # Combinatorics and number theory
│   ├── numerical/                # Calculus, linear algebra, monte carlo
│   ├── signal/                   # Filters, image processing, transforms
│   └── statistics/               # Clustering, decomposition, similarity
├── tests/                        # Python tests
├── java/                         # Java Maven subproject
│   ├── pom.xml                   # Maven config (JUnit 4, Java 11)
│   └── src/
│       ├── main/java/com/optimizeme/
│       │   ├── CollectionUtils.java    # Generics, mergeSorted, groupBy
│       │   └── StringProcessor.java    # isPalindrome, compress, LCP
│       └── test/java/com/optimizeme/
│           ├── CollectionUtilsTest.java
│           └── StringProcessorTest.java
└── js/                           # JavaScript/TypeScript npm subproject
    ├── package.json              # npm config (Vitest)
    ├── tsconfig.json
    └── src/
    │   ├── asyncUtils.js         # retryWithBackoff, batchProcess
    │   └── dataTransform.ts      # pivot, flatten, groupByKey (generics)
    └── tests/
        ├── asyncUtils.test.js
        └── dataTransform.test.ts
```

## Getting Started

### 1. Fork and clone

```bash
git clone https://github.com/<your_github_username>/optimize-me.git
cd optimize-me
```

### 2. Set up each language

**Python** (requires Python 3.11+):
```bash
python -m venv .venv
source .venv/bin/activate
pip install -e .
```

**Java** (requires JDK 11+, Maven):
```bash
cd java
mvn compile
mvn test
cd ..
```

**JavaScript/TypeScript** (requires Node.js, npm):
```bash
cd js
npm install
npm test
cd ..
```

### 3. Set up Codeflash

```bash
codeflash init
```

Since this project already has codeflash settings pre-configured in `pyproject.toml`, you will only need to:
- Get a `CODEFLASH_API_KEY` by [signing up](https://app.codeflash.ai/login)
- Install the GitHub App through [this link](https://github.com/apps/codeflash-ai/installations/select_target)

## Using Codeflash

**Optimize all languages at once** (discovers Python, Java, and JS/TS configs automatically):
```bash
codeflash --all
```

**Optimize a single Python file:**
```bash
codeflash --file src/algorithms/helpers.py --function is_prime
```

**Optimize a single Java file:**
```bash
codeflash --file java/src/main/java/com/optimizeme/StringProcessor.java --function isPalindrome
```

**Optimize a single JS file:**
```bash
codeflash --file js/src/asyncUtils.js --function retryWithBackoff
```

## What to expect

Watch as Codeflash:
1. Discovers all language configs in the project
2. Analyzes your code's intent
3. Generates and runs test cases to understand behavior
4. Proposes multiple optimization strategies
5. Benchmarks each strategy for speed
6. Verifies correctness with regression tests
7. Creates a Pull Request with the fastest correct implementation

## Need Help?

Join our [Discord community](https://www.codeflash.ai/discord) for support and to connect with other developers who love fast code.

## Contributing

**Please don't** open Pull Requests on this repo with the optimizations you found. We want to keep this project unoptimized for future users to experience Codeflash.

Want to contribute? Add code that demonstrates Codeflash's optimization capabilities across any supported language.

---

Never ship slow code again. Happy optimizing!
