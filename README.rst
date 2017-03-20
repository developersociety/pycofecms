================================
Church of England CMS API Client
================================


.. image:: https://img.shields.io/pypi/v/cofecms.svg
        :target: https://pypi.python.org/pypi/cofecms

.. image:: https://img.shields.io/travis/blancltd/cofecms.svg
        :target: https://travis-ci.org/blancltd/cofecms

.. image:: https://readthedocs.org/projects/cofecms/badge/?version=latest
        :target: https://cofecms.readthedocs.io/en/latest/?badge=latest
        :alt: Documentation Status

.. image:: https://pyup.io/repos/github/blancltd/cofecms/shield.svg
     :target: https://pyup.io/repos/github/blancltd/cofecms/
     :alt: Updates


Before you start, make sure you have access credentials for the Church of England CMS API. You will
need a valid `API_ID` and `API_KEY`. See https://cmsapi.cofeportal.org/security for more
information about this.

Most of the endpoints also require a `diocese_id`. You should be supplied with this when you
receive your access credentials.


* Free software: BSD license
* Documentation: https://cofecms.readthedocs.io.


Features
========

* Python client for the CofE CMS API (https://cmsapi.cofeportal.org/)
* Python 3.5
* 100% test coverage


Quick Start
===========

.. code-block:: python

    >>> from cofecms import CofeCMS
    >>> cofe = CofeCMS(API_ID, API_KEY, diocese_id)
    >>> result = cofe.get_contacts(
        limit=10,
        fields={'contact': ['surname']},
        search_params={'keyword': 'smith', 'keyword_names_only': 'on'},
    )

    >>> # This query has 82 total results.
    >>> print(result.total_count)
    82

    >>> # Spread across 9 pages
    >>> print(result.total_pages)
    9

    >>> # Get the data for the first page for the query
    >>> print(result)
    [{'surname': 'Aynsley-Smith'},
     {'surname': 'Bradford-Smith'},
     {'surname': 'Brothertonsmith'},
     {'surname': 'Busen-Smith'},
     {'surname': 'Cox-Smith'},
     {'surname': 'Drummond Smith'},
     {'surname': 'Goldsmith'},
     {'surname': 'Grout-Smith'},
     {'surname': 'Hall-Smith'},
     {'surname': 'Harcourt-Smith'}]

    >>> # Get a specific page for the query
    >>> print(result.get_data_for_page(4))
    [{'surname': 'Smith-Agent'},
     {'surname': 'Smith-Cherry'},
     {'surname': 'Smith-McSmithSmith'},
     {'surname': 'Smith'},
     {'surname': 'Smith'},
     {'surname': 'Smith'},
     {'surname': 'Smith'},
     {'surname': 'Smith'},
     {'surname': 'Smith'},
     {'surname': 'Smith'}]

    >>> # Loop through all available pages
    >>> for page in result.pages_generator():
            print(len(page))
    10
    10
    10
    10
    10
    10
    10
    9
    0


    >>> # Or retrieve all records for the query
    >>> print(result.all())
    [{'surname': 'Aynsley-Smith'},
     {'surname': 'Bradford-Smith'},
     {'surname': 'Brothertonsmith'},
     {'surname': 'Busen-Smith'},
     {'surname': 'Cox-Smith'},
     {'surname': 'Drummond Smith'},
     {'surname': 'Goldsmith'},
     ...
     {'surname': 'Smith'},
     {'surname': 'Smith'},
     {'surname': 'Smith'},
     {'surname': 'Smitherman'},
     {'surname': 'Smithers'},
     {'surname': 'Sutton-Smith'},
     {'surname': 'Thistleton-Smith'}]
