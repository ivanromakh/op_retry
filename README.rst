openprocurement.middleware.retry
================================

Це middleware призначений для повторення запитів на server. 
Кількість запитів визначення змінною tries яку пепедають в middleware.
Для тестування було реалізовано тестовий сервер на Piramid і бібліотеки webtest і unittest
Реалізовано buidlout і setup.py для встановлення чи тестування
Покриття коду 99%

Тестування
----------
Використовуйте наступні команди для тестування::

 python bootstrap.py
 bin/buildout -N
 bin/nosetests

або цю::

 python setup.py test

для перевірки покриття коду::

 bin/nosetests --with-coverage --cover-package=middleware
