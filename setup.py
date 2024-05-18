from setuptools import setup, find_packages

setup(
      name="watercrawl",
      version="0.4.0",
      author="DONGRU WU",
      description="Python package for watercrawl",
      packages=find_packages(),
      python_requires=">=3.10",
      install_requires=["beautifulsoup4", "requests", "tqdm", "html2text"],
)
