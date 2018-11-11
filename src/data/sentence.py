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

    def align_with_allen(self, allen_phase):
        allen_phrase_split = allen_phase.split()
        x = 0
        tok_ids = list()
        try:
            for i in range(0, len(self.sent_tokens)):
                if allen_phrase_split[0] == self.sent_tokens[i].token_text:
                    x = i
                    for j in range(0, len(allen_phrase_split)):
                        if allen_phrase_split[j] == self.sent_tokens[x].token_text:
                            tok_ids.append(self.sent_tokens[x].token_id)
                            x += 1
                        else:
                            break

                    if j == len(allen_phrase_split) - 1:
                        return tok_ids

                    tok_ids = list()
        except:
            print('Except: Failed to find tokens in document-' + str(self.doc_id) + ', sent-' + str(
                self.sent_id))

        return tok_ids


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

    def add_var(self, var, tok_ids):
        if len(tok_ids) > 0:
            pair = var.split(':')
            if pair[0] == 'ARG0':
                self.arg0 = SRLArg(pair[1].strip(), tok_ids)
            elif pair[0] == 'V':
                self.verb = SRLArg(pair[1].strip(), tok_ids)
            elif pair[0] == 'ARG1':
                self.arg1 = SRLArg(pair[1].strip(), tok_ids)
            elif pair[0] == 'ARGM-TMP':
                self.arg_tmp = SRLArg(pair[1].strip(), tok_ids)
            elif pair[0] == 'ARGM-LOC':
                self.arg_loc = SRLArg(pair[1].strip(), tok_ids)
