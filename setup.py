from setuptools import setup

setup(
    name='hexo2notionnext',
    version='0.0.9',
    description='Convert hexo  to notionnext',
    long_description=open('README.md', 'r').read(),
    long_description_content_type="text/markdown",
    url='https://github.com/zhangweidev/hexo2notionnext',
    author='zhangwei',
    author_email='chxxiu+dev@gmail.com',
    license='MIT',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Topic :: Office/Business :: News/Diary',
        'Topic :: System :: Filesystems',
        'Topic :: Text Processing :: Markup :: Markdown',
        'Topic :: Utilities'
    ],
    install_requires=[
        'md2notion>=2.4.1',
        'notion>=0.0.28',
        'python_dateutil>=2.8.2',
        'PyYAML>=6.0',
    ],
    keywords='hexo notion notion.so notion-py markdown md converter',
    packages=['hexo2notionnext'],
    entry_points = {
        'console_scripts': [
            'hexo2notionnext =hexo2notionnext.hexo2notionnext:main'
        ]
    }
)