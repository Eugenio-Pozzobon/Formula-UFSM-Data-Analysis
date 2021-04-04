::[Bat To Exe Converter]
::
::YAwzoRdxOk+EWAjk
::fBw5plQjdCqDJH6N4H42JwlZWQiDKW2pC4oY6fz63OWBtlocRucDaJ3U0LGNNOYc5kHhZ6ok1XVU1sIPA3s=
::YAwzuBVtJxjWCl3EqQJgSA==
::ZR4luwNxJguZRRnk
::Yhs/ulQjdF+5
::cxAkpRVqdFKZSjk=
::cBs/ulQjdF+5
::ZR41oxFsdFKZSDk=
::eBoioBt6dFKZSDk=
::cRo6pxp7LAbNWATEpCI=
::egkzugNsPRvcWATEpCI=
::dAsiuh18IRvcCxnZtBJQ
::cRYluBh/LU+EWAnk
::YxY4rhs+aU+IeA==
::cxY6rQJ7JhzQF1fEqQJhZksaHErTXA==
::ZQ05rAF9IBncCkqN+0xwdVsFAlTMbCXrZg==
::ZQ05rAF9IAHYFVzEqQIWJwlZWQiDCU2JK/UvzdzO34o=
::eg0/rx1wNQPfEVWB+kM9LVsJDGQ=
::fBEirQZwNQPfEVWB+kM9LVsJDGQ=
::cRolqwZ3JBvQF1fEqQJQ
::dhA7uBVwLU+EWDk=
::YQ03rBFzNR3SWATElA==
::dhAmsQZ3MwfNWATElA==
::ZQ0/vhVqMQ3MEVWAtB9wSA==
::Zg8zqx1/OA3MEVWAtB9wSA==
::dhA7pRFwIByZRRnk
::Zh4grVQjdCqDJH6N4H42JwlZWQiDKW2pC4oY6fz63OWBtlocRucDXrr96ZmrLOUQ/lfre58uxUVpvf85PFVdZhfL
::YB416Ek+ZW8=
::
::
::978f952a14a936cc963da21a135fa983
@echo

:start

cls

python-3.9.2-amd64.exe

py ./projectfolder/get-pip.py

py -m pip install -U pip

py -m pip install numpy
py -m pip install pandas
py -m pip install bokeh
py -m pip install tkintertable
py -m pip install sockets
py -m pip install pathlib
py -m pip install update-check
py -m pip install pyserial
py -m pip install scipy

exit