from setuptools import setup, find_packages

setup(
    name='memethesis',
    version='3.3.1',
    description='A CLI tool to visualize your memes',
    long_description=open('./README.md').read(),
    long_description_content_type='text/markdown',
    keywords='meme',
    license='GPLv3',
    url='https://github.com/fakefred/memethesis-cli',
    author='fakefred',
    author_email='fakefred@protonmail.ch',
    classifiers=[
        'Development Status :: 4 - Beta',
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
    install_requires=['PyYAML>=5.1', 'Pillow', 'PyInquirer', 'colored', 'ascim'],
    project_urls={
        'LiberaPay': 'https://liberapay.com/fakefred/donate'
    }
)
