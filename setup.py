import io
import re

from setuptools import setup

with io.open("README.md", "rt", encoding="utf8") as f:
    readme = f.read()

with io.open("ansible_filter/__init__.py", "rt", encoding="utf8") as f:
    version = re.search(r'__version__ = "(.*?)"', f.read(), re.M).group(1)

setup(name='ansible-filter',
      version=version,
      description='The filter module for Hetzner',
      long_description=readme,
      long_description_content_type="text/markdown",
      keywords='hetzner ansible filter',
      url='https://github.com/nl2go/ansible-filter',
      project_urls={
          "Code": "https://github.com/nl2go/ansible-filter",
          "Issue tracker": "https://github.com/nl2go/ansible-filter/issues",
      },
      author='Sanan Guliyev',
      author_email='sanan.quliyev@gmail.com',
      maintainer="Newsletter2Go",
      maintainer_email="ops@newsletter2go.com",
      license='MIT',
      packages=['ansible_filter'],
      python_requires='>=2.7,!=3.0.*,!=3.1.*,!=3.2.*,!=3.3.*,!=3.4.*,!=3.5.*',
      install_requires=[],
      classifiers=[
          "Programming Language :: Python :: 2",
          "Programming Language :: Python :: 2.7",
          "Programming Language :: Python :: 3",
          "Programming Language :: Python :: 3.6",
          "Programming Language :: Python :: 3.7",
          "Programming Language :: Python :: 3.8",
          "License :: OSI Approved :: MIT License",
          "Operating System :: OS Independent",
      ],
      zip_safe=False)
