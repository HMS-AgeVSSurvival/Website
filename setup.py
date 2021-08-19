from setuptools import setup

setup(
    name="dash_website",
    version="0.1",
    description="Website that shows the results on the comparison between age prediction and survival prediction.",
    packages=["website"],
    requires=["setuptools", "wheel"],
    install_requires=[
        "gunicorn==20.1.0",
        "dash_bootstrap_components==0.12.2",
        "dash_core_components==1.17.1",
        "dash_html_components==1.1.4",
        "dash-gif-component==1.1.0",
        "dash_table==4.12.0",
        "dash==1.21.0",
        "sklearn==0.0",
        "numpy==1.21.1",
        "scipy==1.7.0",
        "pandas==1.3.0",
        "plotly==5.1.0",
        "boto3==1.18.5",
        "pyarrow==4.0.1",
    ],
    extras_require={
        "dev": [
            "tqdm==4.61.2",
            "openpyxl==3.0.7",
            "ipykernel==6.0.3",
            "nbformat==5.1.3",
            "black==21.7b0",
            "pyyaml==5.4.1",
        ],
    },
    entry_points={"console_scripts": ["launch_local_website=website.index:launch_local_website"]},
)
