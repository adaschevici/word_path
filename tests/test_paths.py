import io
import pytest
from contextlib import contextmanager
from unittest import mock
from wordpath.paths import (heuristic,
                            FilteredWords,
                            BucketBuilder,
                            WordLadder)
from wordpath.constants import DICT_FILE
from wordpath.exceptions import NotFound
from tests import fixtures

@contextmanager
def mock_open(filename, contents=None):
    def mock_file(*args):
        if args[0] == filename:
            return io.StringIO(contents)
        else:
            mocked_file.stop()
            open_file = open(*args)
            mocked_file.start()
            return open_file
    mocked_file = mock.patch('builtins.open', mock_file)
    mocked_file.start()
    yield
    mocked_file.stop()

@pytest.mark.parametrize("size, expected", [
    (3, ["cat", "dog"]),
    (0, []),
])
def test_get_filtered_words(monkeypatch, size, expected):
    with mock_open(DICT_FILE, fixtures.WORDFILE):
        assert FilteredWords(size).get_filtered_words() == expected

@pytest.mark.parametrize("words, nexpected", [
    (fixtures.WORDLIST, fixtures.NEIGHBOURS_EXPECTED),
])
def test_build_buckets(words, nexpected):
    bb = BucketBuilder(words).build_buckets()
    assert bb == nexpected

@pytest.mark.parametrize("wordone, wordtwo, expected", [
    ("doctors", "awesome", 6),
    ("", "", 0),
    ("dog", "dog", 0),
    ("cat", "CAT", 3),
])
def test_heuristic(wordone, wordtwo, expected):
    assert heuristic(wordone, wordtwo) == expected

@pytest.mark.parametrize("wordone, wordtwo", [
    (None, None),
])
def test_heuristic_raises(wordone, wordtwo):
    with pytest.raises(TypeError):
         heuristic(wordone, wordtwo)

@pytest.mark.parametrize("start, end, maxlen, expected", [
    ("dog", "cat", 3, ["dog", "cog", "cag", "cat"]),
])
def test_word_ladder(start, end, maxlen, expected):
    with mock_open(DICT_FILE, fixtures.PATH_FOUND):
        wl = WordLadder(start, end, maxlen)
        assert wl.word_ladder() == expected

@pytest.mark.parametrize("start, end, maxlen, expected", [
    ("dog", "cat", 4, []),
])
def test_word_ladder_not_found(start, end, maxlen, expected):
    with mock_open(DICT_FILE, fixtures.PATH_FOUND):
        wl = WordLadder(start, end, maxlen)
        with pytest.raises(NotFound):
            assert wl.word_ladder() == expected
