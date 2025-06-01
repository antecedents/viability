"""Module structures.py"""
import pandas as pd

import src.elements.master as mr
import src.elements.structures as st


class Structures:
    """
    Builds the training, testing, and futures data structures
    """

    def __init__(self, master: mr.Master, arguments: dict):
        """

        :param master:
        :param arguments:
        """

        self.__master = master
        self.__arguments = arguments

        # Estimates
        estimates = master.estimates
        estimates['date'] = pd.to_datetime(estimates['timestamp'], unit='us')
        estimates.drop(columns='timestamp', inplace=True)
        self.__estimates = estimates.sort_values(by='date', ascending=True, inplace=False)
        
    def __get_structures(self, section: str) -> pd.DataFrame:
        """
        
        :param section: training or testing
        :return: 
        """
        
        match section:
            case 'training':
                instances = self.__master.training.copy()
            case 'testing':
                instances = self.__master.testing.copy()
            case _:
                raise ValueError(f'Invalid Section: {section}')
        
        instances['date'] = pd.to_datetime(instances['week_ending_date'], format='%Y-%m-%d')
        instances.drop(columns='week_ending_date', inplace=True)
        
        data = instances[['date']].merge(self.__estimates, how='left', on='date')
        
        return data    

    def __futures(self) -> pd.DataFrame:
        """

        :return:
        """

        return self.__estimates[-self.__arguments.get('ahead'):]

    def exc(self) -> st.Structures:
        """

        :return:
        """

        return st.Structures(
            training=self.__get_structures(section='training'), 
            testing=self.__get_structures(section='testing'), 
            futures=self.__futures())
