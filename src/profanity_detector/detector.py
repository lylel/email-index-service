# Figure out how to store and read bad words
from src.profanity_detector.profanity import PROFANITY_SET


class ProfanityDetector:
    def sanitize(self, text):
        # is this readable
        return " ".join(map(self.replace_profanity, text.split()))

    def replace_profanity(self, word):
        return "[profanity]" if word.lower() in PROFANITY_SET else word
