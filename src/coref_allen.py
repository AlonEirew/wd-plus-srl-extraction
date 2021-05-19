import argparse
import json
import os

from allennlp_models import pretrained
from src.data import io
from src.data.data_loader import EcbDataLoader, IDataLoader
from src.data.io import json_serialize_default


def evaluate_coref(ecb_path: str, data_loader: IDataLoader):
    documents = data_loader.read_data_from_corpus_folder(ecb_path)
    # predictor = Predictor.from_path(
    #     "/Users/aeirew/workspace/ecb-wd-plus-srl-extraction/data/coref-spanbert-large-2021.03.10.tar.gz")
    predictor = pretrained.load_predictor("coref-spanbert")
    all_mentions = list()
    for doc in documents:
        prediction = predictor.predict(
            document="Paul Allen was born on January 21, 1953, in Seattle, Washington, to Kenneth Sam Allen and Edna Faye Allen. Allen attended Lakeside School, a private school in Seattle, where he befriended Bill Gates, two years younger, with whom he shared an enthusiasm for computers."
        )
        prediction = predictor.predict(tokenized_document=doc.get_words())
        doc.align_with_resource_doc(prediction['document'])
        doc.set_within_allen_coref(prediction['clusters'])
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

    ecb_data_loader = EcbDataLoader()
    coref_result = evaluate_coref(args.ecb_root_path, ecb_data_loader)

    with open(args.output_file, 'w') as f:
        json.dump(coref_result, f, default=json_serialize_default, indent=4, sort_keys=True)
