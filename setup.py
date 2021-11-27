from setuptools import setup

import djangocms_formbuilder

setup(
    name='djangocms-formbuilder',
    version=djangocms_formbuilder.__version__,
    packages=[],
    url='https://github.com/Aiky30/djangocms-formbuilder',
    license='BSDv3',
    author='Aiky30',
    author_email='',
    description='A form builder for django cms 4+',
    classifiers=[
        "Framework :: Django",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
        "Topic :: Software Development",
    ],
    test_suite="test_runner.run",
)
