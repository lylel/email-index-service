from src.profanity_detector.detector import ProfanityDetector
from src.services.constants import PUNCTUATION_CHARS


class TextSearchOptimizer:
    def __init__(self, text, sanitizer=None):
        self._text = text
        self._sanitizer = sanitizer

    @property
    def text(self):
        return self._text

    @text.setter
    def text(self, value):
        self._text = value

    @property
    def sanitizer(self):
        return self._sanitizer or ProfanityDetector

    def optimize(self) -> str:
        self._remove_punctuation()
        self.text = self.text.strip()
        self._replace_whitespace()
        self.text = self.sanitizer().clean(self.text)
        return self.text

    def _replace_whitespace(self):
        self.text = " ".join(self.text.split())

    def _remove_punctuation(self):
        translator = str.maketrans("", "", PUNCTUATION_CHARS)
        self.text = self.text.translate(translator)
