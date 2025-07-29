from setuptools import setup, find_packages

# Read the long description from README.md
with open("README.md", encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="dkenergy",
    version="0.1.0",
    author="Your Name",
    author_email="you@example.com",
    description="Danish Energy Market Analysis Tool",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/<your-github-handle>/dk-energy-market-tool",
    packages=find_packages(exclude=["tests", "docs"]),
    python_requires=">=3.11",
    install_requires=[
        "pandas>=2.2.0",
        "requests==2.32.3",
        "tenacity>=8.3.0",
        "pydantic==2.6.4",
        "matplotlib==3.9.0",
        "statsmodels>=0.14.5",
        "typer==0.12.3",
        "click==8.1.7",
        "jinja2==3.1.4",
        "weasyprint==62.2",
        "python-dateutil==2.9.0",
        "PyYAML==6.0.1",
    ],
    extras_require={
        "dev": [
            "sphinx==7.4.5",
            "pytest==8.2.0",
            "ruff",
            "pyright",
        ]
    },
    entry_points={
        "console_scripts": [
            "dkenergy=dkenergy.cli:app",
        ],
    },
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Topic :: Scientific/Engineering :: Information Analysis",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.11",
    ],
)
