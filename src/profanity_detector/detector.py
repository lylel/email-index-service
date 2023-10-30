# TODO: Figure out where to store and read bad words (read from config store?)
from src.profanity_detector.profanity import PROFANITY_SET


class ProfanityDetector:
    def clean(self, text):
        # TODO: is this readable
        return " ".join(map(self.replace_profanity, text.split()))

    def replace_profanity(self, word):
        return "[profanity]" if word.lower() in PROFANITY_SET else word
