from mlask import MLAsk
import MeCab
from sys import version_info
import re

PY2 = True if version_info < (3,) else False
IS_MECAB_PYTHON3 = bool(getattr(MeCab, "Tagger_version", True))
RE_POS = re.compile('感動|フィラー')
RE_MIDAS = re.compile('^(?:て|ね)(?:え|ぇ)$')

class EditMLAsk(MLAsk):
    def __init__(self, mecab_arg=''):
        super().__init__(mecab_arg)

    def analyze(self, text):
        # Normalizing
        text = self._normalize(text)

        # Lemmatization by MeCab
        lemmas = self._lexical_analysis(text)

        # Finding emoticon
        emoticon = self._find_emoticon(text)

        # Finding intensifiers of emotiveness
        intensifier = self._find_emotem(lemmas, emoticon)
        intension = len(list(intensifier.values()))

        # Finding emotional words
        emotions = self._find_emotion(lemmas)

        # Estimating sentiment orientation {POSITIVE, NEUTRAL, NEGATIVE}
        orientation = self._estimate_sentiment_orientation(emotions)

        # Estimating activeness {ACTIVE, NEUTRAL, PASSIVE}
        activation = self._estimate_activation(emotions)

        if emotions:
            result = {
                'text': text,
                'emotion': emotions,
                'orientation': orientation,
                'activation': activation,
                'emoticon': emoticon if emoticon else None,
                'intension': intension,
                'intensifier': intensifier,
                'representative': self._get_representative_emotion(emotions)
                }
        else:
            result = {
                'text': text,
                'emotion': None
            }
        return result
    
    def _lexical_analysis(self, text):
        """ By MeCab, doing lemmatization and finding emotive indicator """
        lemmas = {'all': '', 'interjections': [], 'no_emotem': [], 'lemma_words': []}

        if PY2:
            text = text.encode('utf8')
        for line in self.mecab.parse(text).splitlines():
            try:
                if PY2:
                    line = line.decode('utf8')
                row = line.split('\t')
                if len(row) < 2:
                    continue
                surface = row[0]
                if IS_MECAB_PYTHON3:
                    features = row[1:]
                else:
                    features = row[1].split(',')
                if len(features) > 7:
                    (pos, subpos, lemma) = features[0], features[1], features[6]
                elif len(features) == 1:
                    pos = None
                    subpos = None
                    lemma = None
                else:
                    (pos, subpos, lemma) = features[0], features[1], surface
                if pos and subpos and lemma:
                    lemmas['lemma_words'].append(lemma)
                    if RE_POS.search(pos + subpos) or RE_MIDAS.search(surface):
                        lemmas['interjections'].append(surface)
                    else:
                        lemmas['no_emotem'].append(surface)
            except UnicodeDecodeError:
                pass

        lemmas['all'] = ''.join(lemmas['lemma_words']).replace('*', '')
        lemmas['no_emotem'] = ''.join(lemmas['no_emotem'])

        return lemmas