import argparse
import json
import os
from typing import List

import logging
import neuralcoref
import spacy

from wd_plus_srl.data import io
from wd_plus_srl.data.data_loader import EcbDataLoader, IDataLoader, Duc2006Loader
from wd_plus_srl.data.io import json_serialize_default
from wd_plus_srl.data.mention import Mention

logging.basicConfig(level=logging.INFO)


def evaluate_coref(data_path: str, data_loader: IDataLoader) -> List[Mention]:
    documents = data_loader.read_data_from_corpus_folder(data_path)
    all_mentions = list()
    clust_running_index = 0
    for doc in documents:
        doc.cluster_running_index = clust_running_index
        spacy_doc = nlp.tokenizer.tokens_from_list(doc.get_words())
        for pipe in filter(None, nlp.pipeline):
            pipe[1](spacy_doc)

        if spacy_doc._.has_coref:
            doc.align_with_resource_doc(spacy_doc)
            doc.set_within_spacy_coref(spacy_doc._.coref_clusters)
            mention_result = doc.create_mentions_data()
            print(json.dumps(mention_result, default=json_serialize_default))
            all_mentions.extend(mention_result)
            print('Done with Doc-' + doc.doc_id)

        clust_running_index = doc.cluster_running_index

    return all_mentions


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Create Within doc for ECB+ by SpaCy')
    parser.add_argument('--input_file', type=str, help='corpus root', required=True)
    parser.add_argument('--output_file', type=str, help='output file', required=True)
    parser.add_argument('--model', type=str, help='spacy model', required=True)
    args = parser.parse_args()

    nlp = spacy.load("en")
    neuralcoref.add_to_pipe(nlp)
    io.create_if_not_exist(os.path.dirname(args.output_file))

    data_loader = Duc2006Loader()
    coref_result = evaluate_coref(args.input_file, data_loader)

    with open(args.output_file, 'w') as f:
        json.dump(coref_result, f, default=json_serialize_default, indent=4, sort_keys=True)
