from setuptools import setup, find_packages
import os

readme_path = os.path.join(os.path.dirname(__file__), "README.md")
if os.path.exists(readme_path):
    with open(readme_path, "r", encoding="utf-8") as fh:
        long_description = fh.read()
else:
    long_description = "Personal utility library for code analysis, vulnerability detection, and data science tasks."

setup(
    name="ml_tools",
    version="0.1.0",
    author="Tizhin Matvey",
    author_email="matveytizhin@gmail.com",
    description="Personal utility library for code analysis, vulnerability detection, and data science tasks",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/matveytizhin/my_ml_tools_box",  
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
    ],
    python_requires=">=3.8",
    install_requires=[
        "pandas>=1.3.0",
        "numpy>=1.21.0",
        "matplotlib>=3.4.0",
        "scikit-learn>=1.0.0",
        # "torch>=1.12.0",
        # "transformers>=4.30.0",
        # "seaborn>=0.11.0",
        # "pygments>=2.10.0",
    ],
    extras_require={
        "dev": ["pytest>=7.0", "black", "flake8"],
        "viz": ["seaborn", "plotly>=5.0", "ipywidgets"],
    },
    include_package_data=True,
    zip_safe=False,
)
