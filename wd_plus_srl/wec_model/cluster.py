import logging

from src.dataobjs.cluster import Clusters
from src.utils.io_utils import write_mention_to_json

from wd_plus_srl.wec_model.clustering_utils import agglomerative_clustering

logger = logging.getLogger(__name__)


def run_clustering(predictions, mentions):
    clustered_ments = agglomerative_clustering(predictions, mentions, 0.6)
    for mention1 in mentions:
        if mention1.mention_head_pos == "PRON":
            for mention2 in clustered_ments:
                if mention1.coref_chain == mention2.coref_chain and mention2.predicted_coref_chain != "NA":
                    mention1.predicted_coref_chain = mention2.predicted_coref_chain
                    clustered_ments.append(mention1)
                    break

    return clustered_ments


def print_results(all_mentions):
    all_clusters = Clusters.from_mentions_to_predicted_clusters(all_mentions)
    for cluster_id, cluster in all_clusters.items():
        print('\n\t## Cluster=' + str(cluster_id) + " ##")
        for mention in cluster:
            mentions_dict = dict()
            mentions_dict['id'] = mention.mention_id
            mentions_dict['text'] = mention.tokens_str
            mentions_dict['gold'] = mention.coref_chain

            if mention.tokens_number[0] >= 10 and (mention.tokens_number[-1] + 10) < len(mention.mention_context):
                id_start = mention.tokens_number[0] - 10
                id_end = mention.tokens_number[-1] + 10
            elif mention.tokens_number[0] < 10 and (mention.tokens_number[-1] + 10) < len(mention.mention_context):
                id_start = 0
                id_end = mention.tokens_number[-1] + 10
            elif mention.tokens_number[0] >= 10 and (mention.tokens_number[-1] + 10) >= len(mention.mention_context):
                id_start = mention.tokens_number[0] - 10
                id_end = len(mention.mention_context)
            else:
                id_start = 0
                id_end = len(mention.mention_context)

            before = " ".join(mention.mention_context[id_start:mention.tokens_number[0]])
            after = " ".join(mention.mention_context[mention.tokens_number[-1] + 1:id_end])
            mention_txt = " <" + mention.tokens_str + "> "
            mentions_dict['context'] = before + mention_txt + after

            print('\t\tMentions='+ str(mentions_dict))


def clean_and_save(all_mentions, out_file):
    final_list = list()
    for ment in all_mentions:
        if len(ment.tokens_number) == 1 and ment.mention_head_pos == "PRON":
            continue

        ment.coref_chain = ment.predicted_coref_chain.item()
        ment.predicted_coref_chain = None
        ment.mention_context = None
        final_list.append(ment)
    write_mention_to_json(out_file, final_list)
