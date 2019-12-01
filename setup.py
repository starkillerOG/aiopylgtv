from setuptools import setup

setup(
      name = 'aiopylgtv',
      packages = ['aiopylgtv'],
      install_requires = ['websockets', 'asyncio', 'numpy'],
      zip_safe = True,
      version = '0.2.0b1',
      description = 'Library to control webOS based LG Tv devices',
      author = 'Dennis Karpienski',
      author_email = 'dennis@karpienski.de',
      url = 'https://github.com/bendavid/aiopylgtv',
      download_url = 'https://github.com/bendavid/aiopylgtv/archive/0.2.0b1.tar.gz',
      keywords = ['webos', 'tv'],
      classifiers = [],
      entry_points={
        'console_scripts': [
            'aiopylgtvcommand=aiopylgtv.utils:aiopylgtvcommand',
        ],
      },
)
