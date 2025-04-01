# CodeFlash Optimize-Me 

This repository contains code that can be optimized with Codeflash. The idea is that you can easily get started with Codeflash by optimizing this repository.

Fork this repo, clone it on your machine, then run Codeflash to see how it analyzes your code, suggests improvements, and integrates with your workflow through pull requests.

## What is Codeflash?

Codeflash is an automated AI based code performance optimizer that creates verified optimizations for your code. It improves performance, reduces resource usage, and enhances code efficiency. You can use it to optimize algorithms, speed up mathematical computations, optimize Pytorch, and make data handling more efficient with NumPy and Pandas.

## Getting Started

The below is expected to take about 5 minutes.

- Fork this repo on your GitHub account. You can do it by clicking "Fork" on the top of this repo. This is required so that Codeflash can open Pull Requests with the optimizations it found on your fork.
- Clone the repo to your machine. Any machine works - laptops, PCs, virtual machines.

```bash
git clone https://github.com/<your_github_account>/optimize-me.git
cd optimize-me
```
- Create a new Python virtual environment, and activate it.
  
With `venv` you can do
```bash
python -m venv .venv
source .venv/bin/activate
```

To use `conda` you can do
```bash
conda create -n optimize-me
conda activate optimize-me
```

- Install Package dependencies
```bash
pip install -r requirements.txt
```

## Set up Codeflash

You can now follow the quick guided setup by running -
```bash
codeflash init
```
Since this project already has the codeflash settings pre-configured in pyproject.toml, it will only ask you to get a `CODEFLASH_API_KEY` by [signing up to Codeflash](https://app.codeflash.ai/login) and installing a GitHub App through [this link](https://github.com/apps/codeflash-ai/installations/select_target)

## Using CodeFlash

- Optimize all the Python code in this repo by running

```bash
codeflash --all
```
Codeflash will keep creating Pull Requests with optimizations for you as it keeps finding them.

- Optimize a single file

```bash
codeflash --file path/to/file
```

- Optimize a single function

```bash
codeflash --file path/to/file --function function_name
```

🪄 And just like that you've started on the journey of never shipping slow code again!

## Need Help?

The best way to ask for help is to join our [Discord community](https://www.codeflash.ai/discord)

## Contributing

Please don't open Pull Requests on this repo with the optimizations you found. We want to keep this project unoptimized, so that people can optimize it in the future as well.

Want to contribute? Here's how:

1. Fork the repository
2. Create a new branch for your changes
3. Add code that demonstrates CodeFlash's optimization capabilities
4. Submit a pull request with a clear description of your changes

We welcome bug reports and feature requests through Github's issues system.
