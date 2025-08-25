from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="youtube-tg-bot",
    version="1.0.0",
    author="YouTube TG Bot",
    description="A Telegram bot for downloading YouTube video audio with quality selection and playlist support",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/youtube-tg",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: End Users/Desktop",
        "Topic :: Multimedia :: Sound/Audio",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
    ],
    python_requires=">=3.8",
    install_requires=requirements,
    entry_points={
        "console_scripts": [
            "youtube-tg-bot=bot:main",
        ],
    },
    keywords="telegram bot youtube audio download playlist",
    project_urls={
        "Bug Reports": "https://github.com/yourusername/youtube-tg/issues",
        "Source": "https://github.com/yourusername/youtube-tg",
        "Documentation": "https://github.com/yourusername/youtube-tg#readme",
    },
)
