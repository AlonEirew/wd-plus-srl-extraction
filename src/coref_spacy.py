import argparse
import json
import os

import spacy

from src.data import io
from src.data.ecb_doc import ECBDoc
from src.data.io import json_serialize_default


def evaluate_coref(ecb_path):
    documents = ECBDoc.read_ecb(ecb_path)
    all_mentions = list()
    for doc in documents:
        spacy_doc = nlp(doc.text)
        if spacy_doc._.has_coref:
            doc.align_with_spacy_doc(spacy_doc)
            # doc.align_with_allen_doc(prediction['document'])
            # doc.set_within_coref(prediction['clusters'])
            mention_result = doc.create_mentions_data()
            print(json.dumps(mention_result, default=json_serialize_default))
            all_mentions.extend(mention_result)
            print('Done with Doc-' + doc.doc_id)

    return all_mentions


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Create Within doc for ECB+ by SpaCy')
    parser.add_argument('--ecb_root_path', type=str, help='corpus root', required=True)
    parser.add_argument('--output_file', type=str, help='output file', required=True)
    parser.add_argument('--model', type=str, help='spacy model', required=True)

    nlp = spacy.load('en_coref_lg')

    args = parser.parse_args()
    io.create_if_not_exist(os.path.dirname(args.output_file))
    coref_result = evaluate_coref(args.ecb_root_path)

    with open(args.output_file, 'w') as f:
        json.dump(coref_result, f, default=json_serialize_default, indent=4, sort_keys=True)
