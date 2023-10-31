from src.services.text_search_optimizer import TextSearchOptimizer


class TestTextSearchOptimizer:
    def test__optimize__returns_text_without_punctuation(self):
        text = "Hello#$%&'()*+,-./:;<=>?@[\]^_`{|}~…"
        expected = "Hello"
        assert TextSearchOptimizer(text=text).optimize() == expected

    def test__optimize__returns_starting_trailing_spaces_stripped(self):
        text = "   Hello World "
        expected = "Hello World"
        assert TextSearchOptimizer(text=text).optimize() == expected

    def test__optimize__returns_text_with_only_single_spaces(self):
        text = "Hello           World"
        expected = "Hello World"
        assert TextSearchOptimizer(text=text).optimize() == expected

    def test__optimize__returns_profanity_replaced(self):
        text = "Hello apple cherry egg World"
        expected = "Hello [profanity] [profanity] [profanity] World"
        assert TextSearchOptimizer(text=text).optimize() == expected

    def test__optimize__returns_with_single_spaces_no_punctuation_(self):
        text = "Hello   #$%&'()*+,-./:;<=>?@[\]^_`{|}~…  World"
        expected = "Hello World"
        assert TextSearchOptimizer(text=text).optimize() == expected

    def test__optimize__returns_profanity_replaced_single_spaces(self):
        text = "Hello  apple   cherry     egg   World"
        expected = "Hello [profanity] [profanity] [profanity] World"
        assert TextSearchOptimizer(text=text).optimize() == expected

    def test__optimize__returns_profanity_replaced_no_punctuation(self):
        text = "Hello #$%&'()*+,-./:;<=>?@[\]^_`{|apple cherry egg World"
        expected = "Hello [profanity] [profanity] [profanity] World"
        assert TextSearchOptimizer(text=text).optimize() == expected

    def test__optimize__returns_profanity_replaced_single_spaces_no_punctuation(self):
        text = "Hello #$%&'()*+,-./:;<=>?@[\]^_`{|   apple cherry     egg World"
        expected = "Hello [profanity] [profanity] [profanity] World"
        assert TextSearchOptimizer(text=text).optimize() == expected

    def test__optimize__returns_stripped_profanity_replaced_single_spaces_no_punctuation(
        self,
    ):
        text = (
            "     Hello #$%&'()*+,-./:;<=>?@[\]^_`{|   apple cherry     egg World     "
        )
        expected = "Hello [profanity] [profanity] [profanity] World"
        assert TextSearchOptimizer(text=text).optimize() == expected
