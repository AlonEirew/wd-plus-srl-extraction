import argparse
import json
import os
from typing import List

import spacy

from src.data import io
from src.data.ecb_doc import ECBDoc
from src.data.io import json_serialize_default
from src.data.mention import Mention


def evaluate_coref(ecb_path: str) -> List[Mention]:
    documents = ECBDoc.read_ecb(ecb_path)
    all_mentions = list()
    for doc in documents:
        spacy_doc = nlp.tokenizer.tokens_from_list(doc.get_words())
        for pipe in filter(None, nlp.pipeline):
            pipe[1](spacy_doc)

        if spacy_doc._.has_coref:
            doc.align_spacy_with_resource_doc(spacy_doc)
            doc.set_within_spacy_coref(spacy_doc._.coref_clusters)
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
    args = parser.parse_args()

    nlp = spacy.load(args.model)
    io.create_if_not_exist(os.path.dirname(args.output_file))
    coref_result = evaluate_coref(args.ecb_root_path)

    with open(args.output_file, 'w') as f:
        json.dump(coref_result, f, default=json_serialize_default, indent=4, sort_keys=True)
