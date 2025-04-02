# ⚡ CodeFlash Optimize-Me 
**Ship fast code from day one.** This repo lets you experience the magic of AI-powered code optimization.

## 🚀 What is this repo?

This repository contains intentionally unoptimized Python code that's perfect for experiencing Codeflash in action. Fork it, run Codeflash, and watch as it automatically discovers optimizations and opens Pull Requests while verifying the optimized code works exactly the same as the original.

## 🔍 What is Codeflash?

Codeflash is an AI-powered code optimizer that automatically finds the most performant version of your Python code through intelligent benchmarking—while verifying it's still correct. It's like having an expert performance engineer review and optimize every line of your code.

**Codeflash can:**
- Improve algorithms and data structures (like converting lists to sets)
- Speed up mathematical operations with NumPy
- Optimize machine learning code for PyTorch
- Make data handling more efficient with Pandas
- Catch and fix inefficient patterns automatically

Leading engineering teams at [Pydantic](https://pydantic.dev/), [Langflow](https://langflow.org/), and [Roboflow](https://roboflow.com) trust Codeflash to ship expert-level, high-performance code.


## ⏱️ Getting Started ( 5 minutes)

1. **Fork this repo** to your GitHub account by clicking "Fork" on the top of the page. This allows Codeflash to open Pull Requests with the optimizations it found on your forked repo.
2. **Clone your fork** to your local machine.

```bash
git clone https://github.com/<your_github_username>/optimize-me.git
cd optimize-me
```
3. **Create a Python virtual environment, and activate it.**
  
Using `venv`:
```bash
python -m venv .venv
source .venv/bin/activate
```

Or with `conda`:
```bash
conda create -n optimize-me python=3.12
conda activate optimize-me
```

4. **Install dependencies**
```bash
pip install -r requirements.txt
```

## 🔮 Set up Codeflash

Run the guided setup:
```bash
codeflash init
```
Since this project already has the codeflash settings pre-configured in pyproject.toml, you will only need to:
- Get a `CODEFLASH_API_KEY` by [signing up](https://app.codeflash.ai/login)
- Install a GitHub App through [this link](https://github.com/apps/codeflash-ai/installations/select_target)

## 💫 Using CodeFlash

**Optimize the entire repo:**

```bash
codeflash --all
```
Codeflash will create Pull Requests with optimizations as it finds them.

**Optimize a single file**

```bash
codeflash --file path/to/file
```

**Optimize a specific function:**

```bash
codeflash --file path/to/file --function function_name
```

## 🔥 What to expect

Watch as Codeflash:
1. Analyzes your code's intent
2. Generates and runs test cases to understand behavior
3. Proposes multiple optimization strategies
4. Benchmarks each strategy for speed
5. Verifies correctness with regression tests
6. Creates a Pull Request with the fastest correct implementation
7. Shows impressive speedups (up to 90x in some cases!)


## 🤝 Need Help?

Join our [Discord community](https://www.codeflash.ai/discord) for support and to connect with other developers who love fast code.

## Contributing

**Please don't** open Pull Requests on this repo with the optimizations you found. We want to keep this project unoptimized for future users to experience Codeflash.

Want to contribute? Here's how:
1. Fork the repository
2. Create a new branch for your changes
3. Add code that demonstrates CodeFlash's optimization capabilities
4. Submit a pull request with a clear description of your changes

We welcome bug reports and feature requests through Github's issues system.

---

Never ship slow code again. Happy optimizing! ⚡

