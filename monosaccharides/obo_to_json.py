import json
from collections import OrderedDict
from psims.controlled_vocabulary import ControlledVocabulary

cv = ControlledVocabulary.from_obo(open("mono.obo", 'rb'))


def term_to_json(term):
    data = term.data.copy()
    data.pop('property_value', None)
    if data.get('value_type') is None:
        data.pop('value_type', None)
    return data


def cv_to_json(cv):
    header = cv.metadata.copy()
    obj = OrderedDict()
    for key, term in cv.items():
        obj[key] = term_to_json(term)
    return {'metadata': header, 'terms': obj}


with open("mono.obo.json", 'wt') as fh:
    json.dump(cv_to_json(cv), fh, indent=2, sort_keys=True)
