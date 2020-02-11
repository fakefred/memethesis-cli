from setuptools import setup, find_packages

setup(
    name='memethesis',
    version='2.2.0',
    description='A CLI tool to visualize your memes',
    long_description=open('./README.md').read(),
    long_description_content_type='text/markdown',
    keywords='meme',
    license='GPLv3',
    url='https://github.com/fakefred/memethesis-cli',
    author='fakefred',
    author_email='fakefred@protonmail.ch',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: End Users/Desktop',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Natural Language :: English',
        'Topic :: Multimedia :: Graphics'
    ],
    packages=find_packages(),
    include_package_data=True,
    entry_points={
        'console_scripts': [
            'memethesis=memethesis.__main__:main'
        ]
    },
    python_requires='>=3.5',
    install_requires=['Pillow', 'PyInquirer', 'colored'],
    project_urls={
        'LiberaPay': 'https://liberapay.com/fakefred/donate'
    }
)
