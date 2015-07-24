Some regexes may require Python 3.5 due to bug in earlier Python versions, either install Python 3.5 or comment the corresponding lines. Python 3 is needed for Unicode to work properly anyways (unless you replace `r'` with `ur'` and add [coding header](http://stackoverflow.com/a/6289494/160386)).

Colorama module also should be installed, use python’s package installer (`pip install colorama`) or your distribution’s package manager.

Don’t forget to download and configure pywikibot.

Run using `python3.5 ./pwb/pwb.py ./names-in-other-languages.py`
