from setuptools import setup

setup(
    name="LearnTracking",
    version="0.1",
    packages=["dataprep"],  
    install_requires=[
        "opencv-python",
        "pyyaml",
        "deeplabcut==2.3.10",
        "tensorpack", 
        "tensorflow==2.10.0",
    ],
    description="A library for learning tracking",
    author="WL",
    author_email="wl0777@outlook.com",
    url="https://github.com/WLi0777/LearnTracking",
)
