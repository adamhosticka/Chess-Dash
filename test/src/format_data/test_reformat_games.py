"""Test reformat games file."""

import numpy as np
import pandas as pd
import pytest

from app.src.format_data.reformat_games import extract_features_from_pgn, compute_datetimes, get_eco_names, \
    extract_moves_and_clock, extract_time_and_increment, unite_results

PGN = "[Event \"Let's Play!\"]\n[Site \"Chess.com\"]\n[Date \"2009.10.01\"]\n[Round \"-\"]\n[White \"Mainline_Novelty\"]\n[Black \"erik\"]\n[Result \"1-0\"]\n[CurrentPosition \"r2q1rk1/3nppbp/2pp1np1/pp4Nb/3PP1P1/PBN1B2P/1PPQ1P2/R3K2R b KQ g3 1 12\"]\n[Timezone \"UTC\"]\n[ECO \"B07\"]\n[ECOUrl \"https://www.chess.com/openings/Pirc-Defense-Main-Line-4.Be3\"]\n[UTCDate \"2009.10.01\"]\n[UTCTime \"23:14:41\"]\n[WhiteElo \"1633\"]\n[BlackElo \"1920\"]\n[TimeControl \"1/259200\"]\n[Termination \"Mainline_Novelty won by resignation\"]\n[StartTime \"23:14:41\"]\n[EndDate \"2009.10.04\"]\n[EndTime \"15:38:54\"]\n[Link \"https://www.chess.com/game/daily/29099782\"]\n\n1. e4 d6 2. d4 Nf6 3. Nc3 g6 4. Be3 Bg7 5. Qd2 c6 6. Nf3 Bg4 7. Bc4 b5 8. Bb3 a5 9. a3 Nbd7 10. Ng5 O-O 11. h3 Bh5 12. g4 1-0\n"
PGN_WITH_CLOCK = "[Event \"Live Chess\"]\n[Site \"Chess.com\"]\n[Date \"2022.12.21\"]\n[Round \"-\"]\n[White \"ross145\"]\n[Black \"shrimpadamos\"]\n[Result \"1-0\"]\n[CurrentPosition \"r3kbnr/ppp1pppp/2B5/8/3q4/8/PPP2PPP/RNBQK2R b KQkq -\"]\n[Timezone \"UTC\"]\n[ECO \"B01\"]\n[ECOUrl \"https://www.chess.com/openings/Scandinavian-Defense-Mieses-Kotrc-Variation\"]\n[UTCDate \"2022.12.21\"]\n[UTCTime \"13:03:16\"]\n[WhiteElo \"1219\"]\n[BlackElo \"1250\"]\n[TimeControl \"300\"]\n[Termination \"ross145 won by resignation\"]\n[StartTime \"13:03:16\"]\n[EndDate \"2022.12.21\"]\n[EndTime \"13:03:47\"]\n[Link \"https://www.chess.com/game/live/65366973545\"]\n\n1. e4 {[%clk 0:05:00]} 1... d5 {[%clk 0:04:59.5]} 2. exd5 {[%clk 0:04:58.1]} 2... Qxd5 {[%clk 0:04:59.3]} 3. d4 {[%clk 0:04:56.1]} 3... Nc6 {[%clk 0:04:57.3]} 4. Nf3 {[%clk 0:04:53.1]} 4... Bg4 {[%clk 0:04:56.6]} 5. Be2 {[%clk 0:04:50.6]} 5... Bxf3 {[%clk 0:04:53.8]} 6. Bxf3 {[%clk 0:04:49.6]} 6... Qxd4 {[%clk 0:04:53.1]} 7. Bxc6+ {[%clk 0:04:48.4]} 1-0\n"


@pytest.mark.parametrize(
    ['df', 'expected'],
    [
        (
            pd.DataFrame({
                'pgn': [PGN]
            }),
            pd.DataFrame({
                'pgn': [PGN],
                'start_date': ["2009.10.01"],
                'end_date': ["2009.10.04"],
                'start_time': ["23:14:41"],
                'end_time': ["15:38:54"],
                'eco': ["B07"],
                'eco_url': ["https://www.chess.com/openings/Pirc-Defense-Main-Line-4.Be3"],
                'result': ["1-0"]
            })
        )
    ]
)
def test_extract_features_from_pgn(df: pd.DataFrame, expected: pd.DataFrame):
    assert expected.equals(extract_features_from_pgn(df))


@pytest.mark.parametrize(
    ['df', 'expected'],
    [
        (
            pd.DataFrame({
                'start_date': ["2009.10.01"],
                'end_date': ["2009.10.04"],
                'start_time': ["23:14:41"],
                'end_time': ["15:38:54"],
            }),
            pd.DataFrame({
                'start_datetime': [pd.to_datetime("2009-10-01 23:14:41")],
                'end_datetime': [pd.to_datetime("2009-10-04 15:38:54")],
            }),
        )
    ]
)
def test_compute_datetimes(df: pd.DataFrame, expected: pd.DataFrame):
    assert expected.equals(compute_datetimes(df))


@pytest.mark.parametrize(
    ['eco_urls', 'expected'],
    [
        (
            pd.Series([
                'https://www.chess.com/openings/Pirc-Defense-Main-Line-4.Be3',
                'https://www.chess.com/openings/Three-Knights-Opening-3...Bc5',
                'https://www.chess.com/openings/Pirc-Defense-Classical-Variation-4...Bg7-5.Bc4-c6',
            ]),
            pd.Series([
                'Pirc-Defense-Main-Line-4.Be3',
                'Three-Knights-Opening-3...Bc5',
                'Pirc-Defense-Classical-Variation-4...Bg7-5.Bc4-c6'
            ])
        )
    ]
)
def test_get_eco_names(eco_urls: pd.Series, expected: pd.Series):
    assert expected.equals(get_eco_names(eco_urls))


@pytest.mark.parametrize(
    ['pgn', 'expected'],
    [
        (
            PGN,
            (
                ['e4', 'd4', 'Nc3', 'Be3', 'Qd2', 'Nf3', 'Bc4', 'Bb3', 'a3', 'Ng5', 'h3', 'g4'],
                ['d6', 'Nf6', 'g6', 'Bg7', 'c6', 'Bg4', 'b5', 'a5', 'Nbd7', 'O-O', 'Bh5'],
                np.nan,
                np.nan
            )
        ),
        (
            PGN_WITH_CLOCK,
            (
                ['e4', 'exd5', 'd4', 'Nf3', 'Be2', 'Bxf3', 'Bxc6+'],
                ['d5', 'Qxd5', 'Nc6', 'Bg4', 'Bxf3', 'Qxd4'],
                ['0:05:00', '0:04:58.1', '0:04:56.1', '0:04:53.1', '0:04:50.6', '0:04:49.6', '0:04:48.4'],
                ['0:04:59.5', '0:04:59.3', '0:04:57.3', '0:04:56.6', '0:04:53.8', '0:04:53.1']
            )
        )
    ]
)
def test_extract_moves_and_clock(pgn: str, expected: tuple):
    assert expected == extract_moves_and_clock(pgn)


@pytest.mark.parametrize(
    ['time_control', 'res'],
    [
        (
            '1/41dads21313',
            (1, 0)
        ),
        (
            '300+1',
            (300, 1)
        ),
        (
            "60",
            (60, 0)
        )
    ]
)
def test_extract_time_and_increment(time_control: str, res: tuple):
    assert res == extract_time_and_increment(time_control)


@pytest.mark.parametrize(
    ['df', 'expected'],
    [
        (
            pd.DataFrame({
                'result': ['1-0', '0-1', '1/2-1/2', '1-0', '1/2-1/2'],
                'white_result': ['win', 'timeout', 'agreed', 'win', 'insufficient'],
                'black_result': ['resigned', 'win', 'agreed', 'checkmated', 'insufficient']
            }),
            pd.DataFrame({
                'result': ['White', 'Black', 'Draw', 'White', 'Draw'],
                'result_type': ['resigned', 'timeout', 'agreed', 'checkmated', 'insufficient'],
            })
        )
    ]
)
def test_unite_results(df: pd.DataFrame, expected: pd.DataFrame):
    assert expected.equals(unite_results(df))
