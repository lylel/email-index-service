from src.profanity_detector_v1.detector import ProfanityDetector
from src.profanity_detector_v1.profanity import PROFANITY_SET


class TestProfanityDetector:
    def test_clean(self):
        for bad_word in PROFANITY_SET:
            assert (
                ProfanityDetector().clean(f"here is an {bad_word}")
                == "here is an [profanity]"
            )
