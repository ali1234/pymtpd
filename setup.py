from setuptools import setup

setup(
    name='mtp',
    keywords='linux usb gadget functionfs mtp',
    version='0.1',
    author='Alistair Buxton',
    author_email='a.j.buxton@gmail.com',
    url='http://github.com/ali1234/pymtpd',
    license='GPLv3+',
    platforms=['linux'],
    packages=['mtp'],
    scripts=['pymtpd'],
    install_requires=[
        'functionfs', 'libaio', 'construct'
    ],
    classifiers=[
        'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python :: 3',
        'Topic :: Software Development :: Libraries',
        'Topic :: System :: Hardware :: Hardware Drivers',
    ],
)
