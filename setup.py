from pathlib import Path
from setuptools import find_packages, setup

README = Path(__file__).parent / "README.md"
setup(
    name="quantbot",
    version="0.1.0",
    description="Professional quantitative trading system scaffold for Windows/MetaTrader 5",
    long_description=README.read_text(encoding="utf-8"),
    packages=find_packages(),
    include_package_data=True,
    install_requires=["pytest>=8.0.0"],
)
