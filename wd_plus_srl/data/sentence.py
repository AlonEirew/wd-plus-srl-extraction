class Sentence(object):
    def __init__(self, doc_id, sent_id):
        self.doc_id = doc_id
        self.sent_id = sent_id
        self.sent_tokens = list()
        self.sent_text = ''

    def add_token(self, token):
        self.sent_tokens.append(token)

    def _gen_text(self):
        for token in self.sent_tokens:
            tok_text = token.token_text
            if self.sent_text == '':
                self.sent_text = tok_text
            elif tok_text in ['.', ',', '?', '!', '\'re', '\'s', 'n\'t', '\'ve', '\'m', '\'ll', '’s']:
                self.sent_text += tok_text
            else:
                self.sent_text += ' ' + tok_text

        return self.sent_text

    def get_sentence_words(self):
        words = list()
        for token in self.sent_tokens:
            words.append(token.token_text)
        return words

    @staticmethod
    def align_text(text):
        last_tok = ''
        sent_text = ''
        for tok_text in text.split():
            if sent_text == '':
                sent_text = tok_text
            elif tok_text in ['.', ',', '?', '!', '\'re', '\'s', 'n\'t', '\'ve', '\'m', '\'ll', '’s', '\'', '-', '/']:
                sent_text += tok_text
            elif last_tok in ['-', '/']:
                sent_text += tok_text
            else:
                sent_text += ' ' + tok_text

            last_tok = tok_text

        return sent_text

    def get_text(self):
        if self.sent_text == '':
            return self._gen_text()
        return self.sent_text


class SRLSentence(object):
    def __init__(self, doc_id, sent_id):
        self.ecb_doc_id = doc_id
        self.ecb_sent_id = sent_id
        self.srl = list()

    def add_srl_vrb(self, srl_vrb):
        if srl_vrb.verb and (srl_vrb.arg0 or srl_vrb.arg1 or srl_vrb.arg_tmp or srl_vrb.arg_loc):
            self.srl.append(srl_vrb)


class SRLArg(object):
    def __init__(self, text, tok_ids):
        self.text = text
        self.ecb_tok_ids = tok_ids


class SRLVerb(object):
    def __init__(self):
        self.verb = None
        self.arg0 = None
        self.arg1 = None
        self.arg_tmp = None
        self.arg_loc = None
        self.arg_neg = None

    def add_var(self, tags, words):
        arg0_text = ''
        arg1_text = ''
        verb_text = ''
        arg_temp_text = ''
        arg_loc_text = ''
        arg0_toks = list()
        arg1_toks = list()
        verb_toks = list()
        arg_temp_toks = list()
        arg_loc_toks = list()
        for i in range(0, len(tags)):
            if '-ARG0' in tags[i]:
                arg0_text += words[i] + ' '
                arg0_toks.append(i)
            elif '-V' in tags[i]:
                verb_text += words[i] + ' '
                verb_toks.append(i)
            elif '-ARG1' in tags[i]:
                arg1_text += words[i] + ' '
                arg1_toks.append(i)
            elif '-ARGM-TMP' in tags[i]:
                arg_temp_text += words[i] + ' '
                arg_temp_toks.append(i)
            elif '-ARGM-LOC' in tags[i]:
                arg_loc_text += words[i] + ' '
                arg_loc_toks.append(i)

        if arg0_toks and arg0_text:
            self.arg0 = SRLArg(arg0_text.strip(), arg0_toks)
        if verb_toks and verb_text:
            self.verb = SRLArg(verb_text.strip(), verb_toks)
        if arg1_toks and arg1_text:
            self.arg1 = SRLArg(arg1_text.strip(), arg1_toks)
        if arg_temp_toks and arg_temp_text:
            self.arg_tmp = SRLArg(arg_temp_text.strip(), arg_temp_toks)
        if arg_loc_toks and arg_loc_text:
            self.arg_loc = SRLArg(arg_loc_text.strip(), arg_loc_toks)
