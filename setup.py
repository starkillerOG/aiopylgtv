from setuptools import setup

setup(
      name = 'pylgtv',
      packages = ['pylgtv'],
      install_requires = ['websockets', 'asyncio'],
      zip_safe = True,
      version = '0.2.0b1',
      description = 'Library to control webOS based LG Tv devices',
      author = 'Dennis Karpienski',
      author_email = 'dennis@karpienski.de',
      url = 'https://github.com/TheRealLink/pylgtv',
      download_url = 'https://github.com/TheRealLink/pylgtv/archive/0.1.9.tar.gz',
      keywords = ['webos', 'tv'],
      classifiers = [],
      entry_points={
        'console_scripts': [
            'pylgtvcommand=pylgtv.utils:pylgtvcommand',
        ],
      },
)
