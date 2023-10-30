from src.profanity_detector_v1.profanity import PROFANITY_SET


class ProfanityRemover:
    def clean(self, text) -> str:
        return " ".join(map(self._remove_profanity, text.split()))

    def _remove_profanity(self, word):
        return "" if word.lower() in PROFANITY_SET else word
