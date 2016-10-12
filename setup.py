from setuptools import setup, find_packages

testing_extras = ['nose', 'coverage']

setup(name='middleware',
      test_suite = "middleware.tests",
      extras_require = {
        'testing': testing_extras,
      }
)
