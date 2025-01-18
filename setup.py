from setuptools import setup, find_packages

setup(
    name="dressing_room_simulation",
    version="1.0.0",
    description="A multithreaded simulation of dressing room usage",
    author="Your Name",
    author_email="your_email@example.com",
    packages=find_packages(),
    entry_points={
        "console_scripts": [
            "dressing_room_simulation=dressing_room_simulation:main"
        ]
    },
    install_requires=[],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
