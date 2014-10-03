''' Consumer for {{cookiecutter.longName}} '''

import os
import time
from lxml import etree
from datetime import date, timedelta, datetime

import requests

from dateutil.parser import *

from nameparser import HumanName

from scrapi.linter import lint
from scrapi.linter.document import RawDocument, NormalizedDocument

TODAY = date.today()
NAME = '{{cookiecutter.shortName}}'
OAI_DC_BASE_URL = '{{cookiecutter.oaiDcBase}}'
NAMESPACES = '{{cookiecutter.namespaces}}'
DEFAULT = datetime(1970, 01, 01)

def consume(days_back=1):
    start_date = TODAY - timedelta(days_back)
    url = OAI_DC_BASE_URL + '&metadataPrefix={{cookiecutter.metadataPrefix}}&from='
    if '{{cookiecutter.dateGranularity}}' == 'YYYY-MM-DDThh:mm:ssZ'
        url += str(start_date) + 'T00:00:00Z'
    else if '{{cookiecutter.dateGranularity}}' == 'YYYY-MM-DD hh:mm:ss':
        url += str(start_date) + ' 00:00:00'
    else:
        url += str(start_date)

    records = get_records(url)

    xml_list = []
    for record in records:
        set_spec = record.xpath('ns0:header/ns0:setSpec/node()', namespaces=NAMESPACES)[0]
        doc_id = record.xpath('ns0:header/ns0:identifier/node()', namespaces=NAMESPACES)[0]
        record_string = etree.tostring(record, encoding="UTF-8")

        xml_list.append(RawDocument({
                    'doc': record_string,
                    'source': NAME,
                    'docID': doc_id,
                    'filetype': 'xml'
                }))

    return xml_list

def get_records(url):
    data = requests.get(url)
    doc = etree.XML(data.content)
    records = doc.xpath('//ns0:record', namespaces=NAMESPACES)
    token = doc.xpath('//ns0:resumptionToken/node()', namespaces=NAMESPACES)

    if len(token) == 1:
        time.sleep(0.5)
        url = OAI_DC_BASE_URL + '&resumptionToken={}'.format(token[0])
        records += get_records(url)

    return records

def get_contributors(record):
    contributors = record.xpath('//dc:creator/node()', namespaces=NAMESPACES)
    contributor_list = []
    for person in contributors:
        name = HumanName(person)
        contributor = {
            'prefix': name.title,
            'given': name.first,
            'middle': name.middle,
            'family': name.last,
            'suffix': name.suffix,
            'email': '',
            'ORCID': '',
            }
        contributor_list.append(contributor)
    return contributor_list

def get_tags(record):
    tags = record.xpath('//dc:subject/node()', namespaces=NAMESPACES)
    return [tag.lower() for tag in tags]

def get_ids(record, doc):
    serviceID = doc.get('docID')
    all_urls = record.xpath('//dc:identifier/node()', namespaces=NAMESPACES)
    url = ''
    doi = ''
    for identifier in all_urls:
        if 'viewcontent' not in identifier and 'http://' in identifier:
            url = identifier
        if 'doi' in identifier:
            doi = identifier

    return {'serviceID': serviceID, 'url': url, 'doi': ''}

def get_properties(record):
    publisher = record.xpath('//dc:publisher/node()', namespaces=NAMESPACES)
    source = record.xpath('//dc:source/node()', namespaces=NAMESPACES)
    type = record.xpath('//dc:type/node()', namespaces=NAMESPACES)
    format = record.xpath('//dc:format/node()', namespaces=NAMESPACES)
    properties = {
        'type': type,
        'source': source,
        'format': format,
        'publisherInfo': {
            'publisher': publisher,
        },
    }
    return properties

def get_date_created(record):
    date_created = (record.xpath('ns0:metadata/oai_dc:dc/dc:date/node()', namespaces=NAMESPACES) or [''])[0]
    return parse(date_created).isoformat()

def get_date_updated(record):
    dateupdated = (record.xpath('ns0:header/ns0:datestamp/node()', namespaces=NAMESPACES) or [''])[0]
    return parse(dateupdated).isoformat()

def normalize(raw_doc, timestamp):
    doc = raw_doc.get('doc')
    record = etree.XML(doc)

    if '{{hasRestrictedSets}}' == 'True':
        # # load the list of approved series_names as a file
        with open(os.path.join(os.path.dirname(__file__), '{{cookiecutter.approvedSeriesNamesFilename}}')) as series_names:
            series_name_list = [word.replace('\n', '') for word in series_names]

        set_spec = record.xpath('ns0:header/ns0:setSpec/node()', namespaces=NAMESPACES)[0]

        if set_spec.replace('publication:', '') not in series_name_list:
            print('Series not in approved list, not normalizing...')
            return None

    title = record.xpath('//dc:title/node()', namespaces=NAMESPACES)[0]

    description = (record.xpath('ns0:metadata/oai_dc:dc/dc:description/node()', namespaces=NAMESPACES) or [''])[0]

    normalized_dict = {
        'title': title,
        'contributors': get_contributors(record),
        'properties': get_properties(record),
        'description': description,
        'tags': get_tags(record),
        'id': get_ids(record,raw_doc),
        'source': NAME,
        'dateUpdated': get_date_updated(record),
        'dateCreated': get_date_created(record),
        'timestamp': str(timestamp),
    }

    return NormalizedDocument(normalized_dict)
        

if __name__ == '__main__':
    print(lint(consume, normalize))
