import argparse
import distutils
import os

from wd_plus_srl.coref_allen import evaluate_coref
from wd_plus_srl.data.data_loader import IDataLoader
from wd_plus_srl.data.io import create_if_not_exist
from wd_plus_srl.wec_model.cluster import run_clustering, print_results, clean_and_save
from wd_plus_srl.wec_model.generate_wec_predictions import generate_pairs_predictions

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Create Within doc for ECB+ by AllenNLP')
    parser.add_argument('--input_file', type=str, help='corpus root', required=True)
    parser.add_argument('--output_file', type=str, help='output file', required=True)
    parser.add_argument('--loader', type=str, help='data loader (one of ecb/duc)', required=True)
    parser.add_argument('--model_file', type=str, help='wec model file', required=True)
    parser.add_argument('--cuda', type=str, help='wec model file', required=True)

    args = parser.parse_args()
    create_if_not_exist(os.path.dirname(args.output_file))
    _use_cuda = bool(distutils.util.strtobool(args.cuda))

    dataloader = IDataLoader.get_dataloader(args.loader)
    print("Running within document coreference..")
    coref_result_ments, documents = evaluate_coref(args.input_file, dataloader)
    print("Running cross-document coreference (might take a while..)")
    predictions, ments_data = generate_pairs_predictions(coref_result_ments, documents, args.model_file, _use_cuda)
    all_mentions = run_clustering(predictions, ments_data)
    print_results(all_mentions)
    clean_and_save(all_mentions, args.output_file)
