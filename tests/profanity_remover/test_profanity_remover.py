from src.profanity_remover_v1.profanity import PROFANITY_SET
from src.profanity_remover_v1.remover import ProfanityRemover


class TestProfanityRemover:
    def test_clean(self):
        for bad_word in PROFANITY_SET:
            assert ProfanityRemover().clean(f"here is an {bad_word}") == "here is an "
