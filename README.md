# Time Duration Calculator: using TDD

Implementation of a calculator that allows to <b>calculate the duration between two dates/times</b>, using TDD in Python.

## Description

This is class method that takes the time and date of the event as arguments, as well as the time and date of reference (by default set to the present moment) 
and returns the text in natural language, in Polish, which describes the relative time of the event, e.g .: 
* za 5 godzin i 2 minuty, 
* jutro o 10:10, 
* w przyszły czwartek o 17:00, 
* za 4 miesiące i 27 dni, 
* za 10 lat, 11 miesięcy i 30 dni etc.

Code was written in <b>Test Driven Development</b> programming practice, using only Python Standard Libraries.

### Language/Framework/Libraries

* <b>Python 3+</b>
* datetime: module for manipulating dates and times

<b>For TDD:</b>
* unittest: built-in testing framework 
* parameterized: to parameterized testing for unittest

### Need to Install

parametrized:
```$ pip install parameterized```

### Code View
![obraz](https://user-images.githubusercontent.com/86662368/155246669-6fa903a5-46d7-4208-b605-bc81a831557c.png)
