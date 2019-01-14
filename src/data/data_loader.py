from os import walk
from os.path import join
from src.data.doc import Doc
from xml.etree import ElementTree

from src.data.token import Token


class IDataLoader(object):
    def __init__(self):
        pass

    def read_data_from_corpus_folder(self, corpus):
        raise NotImplementedError('Method should be overridden with data loader, example exb_data_loader')


class EcbDataLoader(IDataLoader):
    def __init__(self):
        super(EcbDataLoader, self).__init__()

    def read_data_from_corpus_folder(self, corpus):
        documents = list()
        for (dirpath, folders, files) in walk(corpus):
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

                    documents.append(Doc(doc_id, doc_text, tokens))

        return documents
