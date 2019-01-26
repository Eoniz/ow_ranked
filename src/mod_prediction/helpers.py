
import statistics

class Helpers:

    @staticmethod
    def diff_elo(first_elo : int, second_elo : int) -> int:
        """
        Helper function for getting the elo difference between
        two elo

        :first_elo: <int> : The first elo
        :second_elo: <int> : The second elo

        returns <int> : The difference
        """

        return first_elo - second_elo

    @staticmethod
    def p_d_elo(d : int) -> float:
        """
        Helper function for getting the probability based on D

        :d: <int> : The diff elo

        return <float> : The p(d), value is [0.0, 1.0]
        """
        return 1.0 / (1.0 + 10.0 ** (-d / 400.0))
    
    @staticmethod
    def elo_after_win(own_elo : int, p_d : float, K : int = 45) -> int:
        """
        Helper function for getting the prediction elo after a win

        :own_elo: <int> : The player elo
        :p_d: <float> : The p(D) (probability of win)
        :K: <int> : The constant

        return <int> : The next elo
        """
        return round(own_elo + K * (1 - p_d))
    
    @staticmethod
    def elo_after_defeat(own_elo : int, p_d : float, K : int = 45) -> int:
        """
        Helper function for getting the prediction elo after a lose

        :own_elo: <int> : The player elo
        :p_d: <float> : The p(D) (probability of win)
        :K: <int> : The constant

        return <int> : The next elo
        """

        return round(own_elo + K * (0 - p_d))

    @staticmethod
    def elo_prediction_with_p_d(own_elo : int, p_d : float, K : int = 45):
        """
        Helper function for getting the prediction based on the own elo and the p(D)

        :own_elo: <int> : The player elo
        :p_d: <float> : The p(D) (probability of win)
        :K: <int> : The constant

        return <dict> : The prediction

        Ex :
            elo_prediction_with_p_d(2783, 0.4712494361)
                -> {
                    'win':          2807
                    'lose':         2762
                    'prediction':   2762
                }
        """
        win = Helpers.elo_after_win(own_elo, p_d, K)
        lose = Helpers.elo_after_defeat(own_elo, p_d, K)
        prediction = win if p_d > 0.5 else lose if p_d < 0.5 else own_elo
        return { 
            "win" : win,
            "lose" : lose,
            "prediction" : prediction
        }


    @staticmethod
    def elo_prediction_with_teams(own_elo : int, first_team_elo : int, second_team_elo : int, K : int = 45):
        """
        Helper function for getting the prediction based on the own elo and teams elo

        :own_elo: <int> : The player elo
        :first_team_elo: <int> : The player's team elo
        :second_team_elo: <int> : The player's opponent tema elo

        return <dict> : The prediction

        Ex :
            elo_prediction_with_teams(2762, 2774, 2769)
                -> {
                    'win':          2784
                    'lose':         2739
                    'prediction':   2784
                }
        """
        d = Helpers.diff_elo(first_team_elo, second_team_elo)
        p_d = Helpers.p_d_elo(d)

        win = Helpers.elo_after_win(own_elo, p_d, K)
        lose = Helpers.elo_after_defeat(own_elo, p_d, K)
        prediction = win if p_d > 0.5 else lose if p_d < 0.5 else own_elo

        return { 
            "win" : win,
            "lose" : lose,
            "prediction" : prediction
        }

    @staticmethod
    def calc_mmr(own_elos : [int], victorys : [bool], first_team_elos : [int], second_team_elos : [int]) -> int:
        """
        Helper function for getting the mmr (Aka the K constant)

        :own_elos: [<int>] : The player elos
        :victorys: [<bool>] : The player wins or not
        :first_team_elos: [<int>] : The player's team elos
        :second_team_elos: [<int>] : The player's second team elos

        return <dict> : The mmrs

        Ex :
            own_elos = [ 2783, 2761, 2738, 2760, 2783, 2762, 2739 ]
            victorys = [ 0, 0, 1, 1, 0, 0, 0 ]
            first_team_elos = [ 2833, 2773, 2767, 2712, 2760, 2774, 2759 ]
            second_team_elos = [ 2842, 2763, 2758, 2721, 2780, 2769, 2761 ]
            
            calc_mmr(own_elos, victorys, first_team_elos, second_team_elos)
                -> {
                    'averrage': 45
                    'actual': 45
                }
        """
        
        mmrs = []
        for i in range(len(own_elos) - 1):
            own_elo = own_elos[i]
            next_own_elo = own_elos[i + 1]
            d = Helpers.diff_elo(first_team_elos[i], second_team_elos[i])
            p_d = Helpers.p_d_elo(d)

            mmr = (next_own_elo - own_elo) / ((1 if victorys[i] else 0) - p_d)
            mmrs.append(mmr)

        rounded_mmrs = round(statistics.mean(mmrs))
        final_mmr = round(mmrs[len(mmrs) - 1])

        # Return the rounded value between the mean of mmrs and
        # the last mmr

        ret = {
            "averrage" : rounded_mmrs,
            "actual" : final_mmr
        }

        return ret
