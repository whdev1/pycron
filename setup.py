from distutils.core import setup
import setuptools
setup(
  name = 'pycron',
  packages = ['pycron'],
  version = '1.0.0',
  license='MIT',
  description = '',
  author = 'whdev1',
  author_email = 'whdev1@protonmail.com',
  url = 'https://github.com/whdev1/pycron',
  download_url = 'https://github.com/whdev1/pycron/archive/refs/tags/v1.0.0.tar.gz',
  keywords = ['pycron', 'cron', 'timed functions', 'automation'],
  install_requires=['croniter'],
  classifiers=[
    'Development Status :: 3 - Alpha',
    'Intended Audience :: Developers',
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3.9',
    'Programming Language :: Python :: 3.10'
  ],
)