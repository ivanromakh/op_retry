from setuptools import setup, find_packages

testing_extras = ['nose', 'coverage']

setup(name='middleware',
      test_suite = "middleware.tests",
      install_requires= ['pyramid', 'webtest', 'wsgiref'],
      tests_require= ['pyramid', 'webtest'],
      extras_require = {
        'testing': testing_extras,
      }
)
