from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="poly402",
    version="1.0.0",
    author="poly402",
    description="Programmatic prediction market trading via HTTP payment protocol",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/poly402",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    python_requires=">=3.9",
    install_requires=[
        "requests>=2.31.0",
        "click>=8.1.7",
        "web3>=6.11.0",
        "eth-account>=0.10.0",
        "python-dotenv>=1.0.0",
        "pydantic>=2.5.0",
        "httpx>=0.25.0",
        "py-clob-client>=0.22.0",
        "colorama>=0.4.6",
        "tabulate>=0.9.0",
        "cryptography>=41.0.0",
        "aiohttp>=3.9.0",
        "pyyaml>=6.0.1",
        "jsonschema>=4.20.0",
    ],
    entry_points={
        "console_scripts": [
            "poly402=poly402.cli:main",
        ],
    },
)
