import argparse
import json
import os

from allennlp.predictors.predictor import Predictor

from src.data import io
from src.data.ecb_doc import ECBDoc
from src.data.io import json_serialize_default


def evaluate_coref(ecb_path):
    documents = ECBDoc.read_ecb(ecb_path)
    predictor = Predictor.from_path(
        "https://s3-us-west-2.amazonaws.com/allennlp/models/coref-model-2018.02.05.tar.gz")
    all_mentions = list()
    for doc in documents:
        prediction = predictor.predict(document=doc.text)
        doc.align_with_allen_doc(prediction['document'])
        doc.set_within_coref(prediction['clusters'])
        mention_result = doc.create_mentions_data()
        print(json.dumps(mention_result, default=json_serialize_default))
        all_mentions.extend(mention_result)
        print('Done with Doc-' + doc.doc_id)

    return all_mentions


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Create Within doc for ECB+ by AllenNLP')
    parser.add_argument('--ecb_root_path', type=str, help='corpus root', required=True)
    parser.add_argument('--output_file', type=str, help='output file', required=True)

    args = parser.parse_args()
    io.create_if_not_exist(os.path.dirname(args.output_file))
    coref_result = evaluate_coref(args.ecb_root_path)

    with open(args.output_file, 'w') as f:
        json.dump(coref_result, f, default=json_serialize_default, indent=4, sort_keys=True)
