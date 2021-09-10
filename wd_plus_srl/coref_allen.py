import argparse
import json
import os
from typing import List, Tuple

from allennlp.predictors import Predictor

from wd_plus_srl.data.data_loader import IDataLoader
from wd_plus_srl.data.doc import Doc
from wd_plus_srl.data.io import json_serialize_default, create_if_not_exist
from wd_plus_srl.data.mention import Mention


def evaluate_coref(input_path: str, data_loader: IDataLoader) -> Tuple[List[Mention], List[Doc]]:
    documents = data_loader.read_data_from_corpus_folder(input_path)
    predictor = Predictor.from_path("https://storage.googleapis.com/allennlp-public-models/coref-spanbert-large-2021.03.10.tar.gz")
    all_mentions = list()
    clust_running_index = 0
    for doc in documents:
        doc.cluster_running_index = clust_running_index
        prediction = predictor.predict_tokenized(tokenized_document=doc.get_words())
        doc.align_with_resource_doc(prediction['document'])
        doc.set_within_allen_coref(prediction['clusters'])
        mention_result = doc.create_mentions_data()
        print(json.dumps(mention_result, default=json_serialize_default))
        all_mentions.extend(mention_result)
        print('Done with Doc-' + doc.doc_id)
        clust_running_index = doc.cluster_running_index

    return all_mentions, documents


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Create Within doc for ECB+ by AllenNLP')
    parser.add_argument('--input_file', type=str, help='corpus root', required=True)
    parser.add_argument('--output_file', type=str, help='output file', required=True)
    parser.add_argument('--loader', type=str, help='data loader (one of ecb/duc)', required=True)

    args = parser.parse_args()
    create_if_not_exist(os.path.dirname(args.output_file))

    dataloader = IDataLoader.get_dataloader(args.loader)

    coref_result, _ = evaluate_coref(args.ecb_root_path, dataloader)

    with open(args.output_file, 'w') as f:
        json.dump(coref_result, f, default=json_serialize_default, indent=4, sort_keys=True)
