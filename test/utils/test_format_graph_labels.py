import pytest

from app.utils.format_graph_labels import format_labels


@pytest.mark.parametrize(
    ['to_format', 'expected_formated'],
    [
        ([], {}),
        (
            ['rapid_chess_rating'],
            {'rapid_chess_rating': 'rapid chess rating'}
        ),
        (
             ['blitz_rating', 'time_class', 'w-moves'],
             {'blitz_rating': 'blitz rating', 'time_class': 'time class', 'w-moves': 'w-moves'}
        )
    ]
)
def test_format_labes(to_format: list, expected_formated: dict):
    formated = format_labels(to_format)
    assert formated == expected_formated

