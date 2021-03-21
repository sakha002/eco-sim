from setuptools import setup

package_name = 'auctioneer'

setup(
    name=package_name,
    version='0.0.0',
    packages=[package_name],
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='root',
    maintainer_email='hejazi.hossein@gmail.com',
    description=' example package for time publish',
    license='MIT License ',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'auctioneer_server = auctioneer.auctioneer_server:main',
            'auctioneer_test_client = auctioneer.auctioneer_test_client:main',

        ],
    },
)




