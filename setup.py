from setuptools import find_packages, setup

setup(
    name='todo',
    version='1.1.0',
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'blinker==1.8.2',
        'click==8.1.7',
        'Flask==3.0.3',
        'itsdangerous==2.2.0',
        'Jinja2==3.1.4',
        'MarkupSafe==2.1.5',
        'Werkzeug==3.0.4',
        'setuptools==59.6.0',
        'SQLAlchemy==2.0.32',
        'pytest==8.3.2',
        'coverage==7.6.1'
    ]
)