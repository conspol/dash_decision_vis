from setuptools import setup, find_packages

setup(
    name='dash_decision_vis',
    version='0.1',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'dash',
        'pandas',
        'numpy',
        'plotly'
    ],
    # entry_points={
    #     'console_scripts': [
    #     ],
    # },
)
