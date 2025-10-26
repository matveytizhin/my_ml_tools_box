from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="matvey_toolbox",
    version="0.1.0",
    author="Tizhin Matvey",
    author_email="your.email@example.com",  
    description="Personal utility library for code analysis, vulnerability detection, and data science tasks",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/matvey_toolbox", 
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
    # install_requires=[
    #     "pandas>=1.3.0",
    #     "numpy>=1.21.0",
    #     "matplotlib>=3.4.0",
    #     "seaborn>=0.11.0",
    #     "scikit-learn>=1.0.0",
    #     "torch>=1.12.0",              
    #     "transformers>=4.30.0",      
    #     "tqdm>=4.60.0",
    #     "pygments>=2.10.0",          
    # ],
    # extras_require={
    #     "dev": [
    #         "pytest>=7.0",
    #         "black",
    #         "flake8",
    #     ],
    #     "viz": [
    #         "plotly>=5.0",
    #         "ipywidgets",
    #     ],
    # },
    include_package_data=True,
    zip_safe=False,
)
