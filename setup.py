
from setuptools import setup, find_packages

setup(
    name="dash_website",
    version="0.1",
    description="Website that shows the results on the comparison between age prediction and survival prediction.",
    packages=["website"],
    requires=["setuptools", "wheel"],
    install_requires=[
        "gunicorn",
        "dash_bootstrap_components",
        "dash_core_components",
        "dash_html_components",
        "dash-gif-component",
        "dash_table",
        "dash",
        "sklearn",
        "numpy",
        "scipy",
        "pandas",
        "plotly",
        "boto3",
        "matplotlib",
        "pyarrow",
    ],
    extras_require={
        "dev": ["tqdm", "openpyxl", "ipykernel", "nbformat", "black", "pyyaml"],
    },
    entry_points={"console_scripts": ["launch_local_website=website.index:launch_local_website"]},
)