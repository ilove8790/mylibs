from setuptools import setup, find_packages

setup(
    name="mylibs",  # 패키지 이름
    version="0.1.0",  # 버전
    packages=find_packages(),  # 패키지 자동탐지
    install_requires=[],  # 의존 패키지 (필요하면 추가)
    description="A custom library package",
    author="Seungchul Lee",
    author_email="schlee8790@gmail.com",
)