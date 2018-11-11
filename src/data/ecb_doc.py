from os import walk
from os.path import join
from xml.etree import ElementTree

from src.data.mention import Mention
from src.data.sentence import Sentence
from src.data.token import Token


class ECBDoc(object):
    def __init__(self, doc_id, text, tokens):
        self.doc_id = doc_id
        self.text = text
        self.tokens = tokens

    def find_token_and_set_cluster_id(self, tok_id, cluster_num):
        found = False
        for token in self.tokens:
            if token.doc_tok_id_span and tok_id in token.doc_tok_id_span:
                token.within_coref.add(cluster_num)
                found = True

        if not found:
            print("**** Token not found for-" + self.doc_id + ', Allen token-' + str(tok_id))

    def set_within_allen_coref(self, clusters):
        for i in range(0, len(clusters)):
            cluster = clusters[i]
            for coref_span in cluster:
                for tok_id in range(coref_span[0], coref_span[1] + 1):
                    self.find_token_and_set_cluster_id(tok_id, i)

    def set_within_spacy_coref(self, clusters):
        for i in range(0, len(clusters)):
            cluster = clusters[i]
            for mention in cluster:
                coref_span = [mention.start, mention.end]
                for tok_id in range(coref_span[0], coref_span[1]):
                    self.find_token_and_set_cluster_id(tok_id, i)

    def align_with_resource_doc(self, resource_doc):
        x = 0
        for i in range(0, len(resource_doc)):
            for j in range(x, len(self.tokens)):
                if not self.tokens[j].doc_tok_id_span:
                    if str(resource_doc[i]) == self.tokens[j].token_text:
                        self.tokens[j].doc_tok_id_span = [i, i]
                        self.tokens[j].span_closed = True
                        self.tokens[j-1].span_closed = True
                        x = j - 1
                        break
                    elif str(resource_doc[i]) in self.tokens[j].token_text:
                        self.tokens[j].doc_tok_id_span = [i]
                        x = j - 1
                        break
                    elif self.tokens[j].token_text in str(resource_doc[i]):
                        self.tokens[j].doc_tok_id_span = [i]
                        self.tokens[j].span_closed = True
                        self.tokens[j - 1].span_closed = True
                        x = j - 1
                        break
                elif str(resource_doc[i]) in self.tokens[j].token_text:
                    self.tokens[j].doc_tok_id_span.append(i)
                    x = j - 1
                    break

    def create_mentions_data(self):
        mentions_result = list()
        for i in range(0,len(self.tokens)):
            token = self.tokens[i]
            while len(token.within_coref) > 0:
                cur_with = next(iter(token.within_coref))
                token.within_coref.remove(cur_with)
                mention_str = token.token_text
                token_ids = [token.token_id]
                doc_id = self.doc_id
                sent_id = token.sent_id
                for j in range(i+1, len(self.tokens)):
                    if cur_with in self.tokens[j].within_coref:
                        mention_str += ' ' + self.tokens[j].token_text
                        token_ids.append(self.tokens[j].token_id)
                        self.tokens[j].within_coref.remove(cur_with)
                    else:
                        break

                mention_data = Mention(doc_id, int(sent_id), token_ids, mention_str, str(cur_with))
                mentions_result.append(mention_data)

        return mentions_result

    @staticmethod
    def to_sentences(documents):
        sentences = list()
        for doc in documents:
            sent_id = 0
            sentence = Sentence(doc.doc_id, sent_id)
            for token in doc.tokens:
                if token.sent_id != sent_id:
                    sentences.append(sentence)
                    sent_id = token.sent_id
                    sentence = Sentence(doc.doc_id, sent_id)
                    sentence.add_token(token)
                else:
                    sentence.add_token(token)

            sentences.append(sentence)

        return sentences

    @staticmethod
    def read_ecb(ecb_path):
        documents = list()
        for (dirpath, folders, files) in walk(ecb_path):
            for file in files:
                is_ecb_plus = False
                if file.endswith('.xml'):
                    print('processing file-', file)

                    if 'ecbplus' in file:
                        is_ecb_plus = True

                    tree = ElementTree.parse(join(dirpath, file))
                    root = tree.getroot()
                    doc_id = root.attrib['doc_name']
                    tokens = list()
                    doc_text = ''
                    for elem in root:
                        if elem.tag == 'token':
                            sent_id = int(elem.attrib['sentence'])
                            tok_id = elem.attrib['number']
                            tok_text = elem.text
                            if is_ecb_plus and sent_id == 0:
                                continue
                            if is_ecb_plus:
                                sent_id = sent_id - 1

                            tokens.append(Token(sent_id, int(tok_id), tok_text))
                            if doc_text == '':
                                doc_text = tok_text
                            elif tok_text in ['.', ',', '?', '!', '\'re', '\'s', 'n\'t', '\'ve',
                                              '\'m', '\'ll']:
                                doc_text += tok_text
                            else:
                                doc_text += ' ' + tok_text

                    documents.append(ECBDoc(doc_id, doc_text, tokens))

        return documents
