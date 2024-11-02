from setuptools import setup, find_packages

setup(
    name="agentic_ai",
    version="0.1.0",
    description="Multi-agent system using OpenAI and APIs as tools",
    author="Your Name",
    packages=find_packages(),
    install_requires=[
        # Core dependencies
        "openai>=1.33.0",
        "pydantic>=2.6.1",
        "pydantic-settings>=2.1.0",
        
        # FastAPI and server
        "fastapi>=0.109.2",
        "uvicorn>=0.27.1",
        
        # Environment and config
        "python-dotenv>=1.0.0",
        
        # HTTP client
        "aiohttp>=3.9.3",
        
        # Type hints
        "typing-extensions>=4.9.0"
    ],
    extras_require={
        'dev': [
            'pytest>=8.0.0',
            'black>=24.1.1',
            'isort>=5.13.2'
        ]
    },
    python_requires='>=3.11',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.11',
    ],
) 