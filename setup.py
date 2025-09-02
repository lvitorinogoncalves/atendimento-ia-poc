from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="atendimento-ia",
    version="0.1.0",
    author="Seu Nome",
    author_email="seu.email@exemplo.com",
    description="Sistema de atendimento por voz com IA",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/seu-usuario/atendimento-ia-poc",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    python_requires=">=3.8",
    install_requires=[
        "openai>=1.3.0",
        "python-dotenv>=1.0.0",
        "pyttsx3>=2.90",
        "SpeechRecognition>=3.10.0",
        "pyaudio>=0.2.13",
    ],
    entry_points={
        "console_scripts": [
            "atendimento-ia=interface.cli.cli_app:main",
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Intended Audience :: Developers",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
    ],
)
