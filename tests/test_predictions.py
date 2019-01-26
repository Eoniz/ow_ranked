import pytest
import random
from src import app
from src.mod_prediction.helpers import Helpers

@pytest.fixture
def client(request):
    test_client = app.test_client()

    return test_client

def test_d():
    """
    GIVEN prediction helper
    CHECK if the difference between two elo is correct
    """

    # Check for one value first
    assert Helpers.diff_elo(2833, 2842) == -9

    # Check for 10 random, should works
    for _ in range(10):
        first_elo = random.randint(2500, 3000)
        second_elo = first_elo + random.randint(-200, 200)
        diff = first_elo - second_elo
        assert Helpers.diff_elo(first_elo, second_elo) == diff

def test_p_d():
    """
    GIVEN prediction helper
    CHECK if p(d) is correct with the D
    """

    # Check for one value first
    assert Helpers.p_d_elo(0) == 0.5

    # Check for 10 random, should works
    for _ in range(10):
        D = random.randint(-10, 10)
        p_d = 1.0 / (1.0 + 10.0 ** (-D / 400.0))

        assert p_d == Helpers.p_d_elo(D)

def test_elo_after_win():
    """
    GIVEN prediction helper
    CHECK if elo_after_win is correct based on D, p(d), and own_elo
    """

    # Check for one value
    assert Helpers.elo_after_win(2783, 0.4870508551) == 2806

def test_elo_after_lose():
    """
    GIVEN prediction helper
    CHECK if elo_after_defeat is correct based on D, p(d), and own_elo
    """

    # Check for one value
    assert Helpers.elo_after_defeat(2783, 0.4870508551) == 2761

def test_elo_prediction_with_p_d():
    """
    GIVEN prediction helper
    CHECK if elo_after_prediction_with_p_d is correct based on D, p(d), and own_elo
    """

    # Check for two values
    prediction = Helpers.elo_prediction_with_p_d(2783, 0.4712494361)
    assert prediction["win"] == 2807
    assert prediction["lose"] == 2762
    assert prediction["prediction"] == 2762

def test_elo_prediction_with_teams():
    """
    GIVEN prediction helper
    CHECK if elo_after_prediction_with_teams is correct based on D, p(d), and own_elo
    """

    # Check for two values
    prediction = Helpers.elo_prediction_with_teams(2762, 2774, 2769)
    assert prediction["win"] == 2784
    assert prediction["lose"] == 2739
    assert prediction["prediction"] == 2784

def test_calc_mmr():
    """
    GIVEN prediction helper
    CHECK if calc_mmr returns the correct K factor
    """

    own_elos = [
        2783, 2761, 2738, 2760, 2783, 2762, 2739
    ]

    victorys = [
        0, 0, 1, 1, 0, 0, 0
    ]

    first_team_elos = [
        2833, 2773, 2767, 2712, 2760, 2774, 2759
    ]

    second_team_elos = [
        2842, 2763, 2758, 2721, 2780, 2769, 2761
    ]

    mmrs = Helpers.calc_mmr(own_elos, victorys, first_team_elos, second_team_elos)

    assert mmrs["actual"] == 45
    assert mmrs["averrage"] == 45