#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Provides ORCID, a simple class to fetch records from the ORCID database
"""

from exceptions import UserWarning
import re
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
    orcid_id = str()

    def __init__(self, orcid_id):
        self.config['uri'] = 'https://pub.orcid.org'
        if self.validate_orcid(orcid_id):
            self.orcid_id = orcid_id
        else:
            raise AttributeError('Please provide a valid ORCID ID')

    '''Fetch all works associated with a specific ORCID id
    '''
    def get_works(self):

        r = requests.get("{}/{}/{}".format(self.config['uri'], self.orcid_id, 'works'),
                         headers={'Accept': 'application/orcid+json'})
        if r.status_code == 200:
            works = r.json()['group']
        else:
            raise HTTPException('Error fetching data, status code: {}'.format(r.status_code))
        return works

    '''Fetch a specific work with citations and contributors included
    '''
    def get_work(self, put_code):
        if not put_code:
            raise UserWarning('Provide a valid ORCID work put code, passed {} for id {}')
        r = requests.get("{}/{}/{}/{}".format(self.config['uri'], self.orcid_id, 'work', put_code),
                         headers={'Accept': 'application/orcid+json'})
        if r.status_code == 200:
            work = r.json()
        else:
            raise HTTPException('Error fetching data, status code: {}'.format(r.status_code))
        return work

    # Validate ORCID ID as XXXX-XXXX-XXXX-XXXX where X is an integer from 0 to 9
    @staticmethod
    def validate_orcid(orcid_id):
        match = re.compile("([0-9]{4}-){3}[0-9]{4}").match(orcid_id)
        if match and match.group() == orcid_id:
            return True
        else:
            return False
