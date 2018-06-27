#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Provides ORCID, a simple class to fetch records from the ORCID database
"""

import sys
from exceptions import UserWarning
import requests

__author__ = 'Manuel Torrinha'
__credits__ = ["Manuel Torrinha", u'Sérgio almeida']
__license__ = "GPL"
__version__ = "0.1"
__maintainer__ = "Manuel Torrinha"
__email__ = "manuel.torrinha@tecnico.ulisboa.pt"
__status__ = "Development"


class HTTPException(Exception):
    pass


class ORCID:
    config = dict()

    def __init__(self):
        self.config['uri'] = 'https://pub.orcid.org'
        self.config['works'] = 'works'

    def get_works(self, orcid_id=None):
        if orcid_id is None:
            raise UserWarning('Provide a valid ORCID identifier, passed {}'.format(orcid_id))

        r = requests.get("{}/{}/{}".format(self.config['uri'], orcid_id, self.config['works']),
                         headers={'Accept': 'application/orcid+json'})
        if r.status_code == 200:
            works = r.json()['group']
        else:
            raise HTTPException('Error fetching data, status code: {}'.format(r.status_code))
        return works


if __name__ == "__main__":
    if len(sys.argv) != 1:
        raise UserWarning('{} takes one mandatory argument, the member\'s ORCID id'.format(sys.argv[0]))

    _id = sys.argv[1]
    o = ORCID()
    o.get_works(orcid_id=_id)
