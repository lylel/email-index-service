from src.profanity_detector_v1.profanity import PROFANITY_SET


class ProfanityDetector:
    def clean(self, text) -> str:
        return " ".join(map(self._replace_profanity, text.split()))

    def _replace_profanity(self, word):
        return "[profanity]" if word.lower() in PROFANITY_SET else word
