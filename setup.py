from setuptools import setup

setup(
    name='binary_mosaic_images',
    version='0.1.1',    
    description='Binary Mosaic Images',
    url='https://github.com/chazzofalf/binary_mosaic_images',
    author='Charles Montgomery',
    author_email='charles.montgomery@charter.net',
    license='',
    packages=['binary_mosaic_images'],
    install_requires=['Pillow==10.1.0'],

    classifiers=[
        'Development Status :: Development/Open Testing',
        'Intended Audience :: Graphics',        
        'Operating System :: POSIX :: Linux',  
        'Programming Language :: Python :: 3.11',
    ],
)