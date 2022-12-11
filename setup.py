from setuptools import find_packages, setup

setup(
    name="Mawdoo3 TTS",
    version="v0.1.6",
    description="Mawdoo3 TTS comparisions",
    author="Hesham Bataineh",
    author_email="hisham.bataineh@mawdoo3.com",
    license="Proprietary: Mawdoo3 internal use only",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Environment :: Console",
        "Framework :: Flask",
        "Intended Audience :: Developers",
        "License :: Other/Proprietary License",
        "Natural Language :: Arabic",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3.6",
        "Topic :: Software Development :: Libraries :: Application Frameworks",
    ],
    keywords="mawdoo3 speech synthesis comparision",
    packages=find_packages(exclude=["contrib", "docs", "tests"]),
    install_requires=[
        "sox",
        "google-api-core",
        "google-auth",
        "google-cloud-texttospeech",
        "azure-cognitiveservices-speech",
        "argparse",
        "pydub",
        "grpcio",
    ],
    test_suite="nose2.collector.collector",
    include_package_data=True,
    extras_require={
        "test": ["nose2", "filetype"],
        "dev": ["nose2", "autopep8", "pycodestyle", "filetype"],
    },
    entry_points={
        "console_scripts": [
            "tts-vendors=tts.api:tts_vendors_service",
        ],
    },
)
