from distutils.core import setup

setup(name='snowflakes',
      version='1.0',
      description='Python Distribution Utilities',
      author='Shaleen Anand Taneja',
      author_email='shaleenanand.taneja@pb.com',
      url='none',
      install_requires=['SQLAlchemy','snowflake-connector-python','pandas','snowflake-sqlalchemy']
#      packages=['snowflakes']
     )

