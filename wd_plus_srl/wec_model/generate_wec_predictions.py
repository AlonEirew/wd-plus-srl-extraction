import logging
import random
from itertools import product
from typing import List

import numpy as np
import torch
from src.dataobjs.mention_data import MentionData
from src.utils.embed_utils import EmbedInMemory

from wd_plus_srl.data.doc import Doc
from wd_plus_srl.data.mention import Mention

logger = logging.getLogger(__name__)
MAX_ALLOWED_BATCH_SIZE = 20000


def generate_pred_matrix(inference_model, mentions):
    all_pairs = list(product(mentions, repeat=2))
    pairs_chunks = [all_pairs]
    if len(all_pairs) > MAX_ALLOWED_BATCH_SIZE:
        pairs_chunks = [all_pairs[i:i + MAX_ALLOWED_BATCH_SIZE] for i in
                        range(0, len(all_pairs), MAX_ALLOWED_BATCH_SIZE)]
    predictions = np.empty(0)
    with torch.no_grad():
        for chunk in pairs_chunks:
            chunk_predictions, _ = inference_model.predict(chunk, bs=len(chunk))
            for i, pair in enumerate(chunk):
                if pair[0].doc_id == pair[1].doc_id:
                    if pair[0].coref_chain == pair[1].coref_chain:
                        chunk_predictions[i] = 1
                    else:
                        chunk_predictions[i] = 0
            predictions = np.append(predictions, chunk_predictions.detach().cpu().numpy())
    predictions = 1 - predictions
    pred_matrix = predictions.reshape(len(mentions), len(mentions))
    return pred_matrix


def predict(model, mentions: List[MentionData]):
    before_size = len(mentions)
    mentions = [mention for mention in mentions if mention.mention_head_pos not in ["PRON", "DET", "SCONJ"]]
    after_size = len(mentions)
    print("Total Mentions before:" + str(before_size))
    print("Total PRON removed:" + str(before_size - after_size))
    print("Total Mentions after:" + str(after_size))
    return generate_pred_matrix(model, mentions), mentions


def get_pairwise_model(model_file, mentions, use_cuda):
    if use_cuda:
        pairwize_model = torch.load(model_file)
        pairwize_model.cuda()
    else:
        pairwize_model = torch.load(model_file, map_location=torch.device('cpu'))

    pairwize_model.set_embed_utils(EmbedInMemory(mentions=mentions, max_surrounding_contx=250, use_cuda=use_cuda))

    pairwize_model.eval()
    return pairwize_model


def convert_to_mentiondata(mentions: List[Mention], documents: List[Doc]) -> List[MentionData]:
    documents_dict = {doc.doc_id: [tok.token_text for tok in doc.tokens] for doc in documents}
    return [
        MentionData(None, "0", ment.doc_id, ment.sent_id, ment.tokens_number, ment.tokens_str,
                    documents_dict[ment.doc_id], None, None, ment.coref_chain, gen_lemma=True)
        for ment in mentions
    ]


def generate_pairs_predictions(mentions: List[Mention], documents: List[Doc], model_file, use_cuda):
    torch.manual_seed(1)
    random.seed(1)
    np.random.seed(1)
    ments_data = convert_to_mentiondata(mentions, documents)
    print("Loading wec model..")
    pairwise_mode = get_pairwise_model(model_file, ments_data, use_cuda)
    predictions, filter_ments = predict(pairwise_mode, ments_data)
    return predictions, filter_ments
