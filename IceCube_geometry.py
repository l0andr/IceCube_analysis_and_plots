"""

Classes and functions for work and visualisation IceCube sensor geometry

Autor: Andrey Loginov
Date 29.01.2023
"""

import numpy as np
import pandas as pd
import plotly.graph_objects as go


class IceCubeGeometry():

    def __init__(self, path_to_file):
        self.__path_to_file = path_to_file
        self.sensor_geometry_pd = None
        self.read_geometry_file(path_to_file)

    def read_geometry_file(self, path_to_file: str = None):
        """
        Expected CSV file with following columns [sensor_id] [x] [y] [z]
        :param path_to_file: path to csv file with sensor geometry
        :return:
        """
        if path_to_file is None or len(path_to_file) == 0:
            raise RuntimeError(f"{self.__class__.__name__} error path_to_file is mandatory defined")
        self.sensor_geometry_pd = pd.read_csv(path_to_file)
        self.sensor_geometry_pd.set_index('sensor_id', inplace=True)

    @property
    def sensor_geometry(self):
        return self.sensor_geometry_pd

    def match_id_to_coordinate(self, indf, columns_for_matching='sensor_id'):
        return indf.merge(self.sensor_geometry_pd, left_on=[columns_for_matching], right_index=True)


def sensors_plot3d(df: pd.DataFrame, fig=None):
    if fig is None:
        fig = go.FigureWidget()
    fig.add_scatter3d(x=df.x, y=df.y, z=df.z, marker={'size': 1, 'color': 'gray'}
                      , mode='markers', name='Sensors positions')
    return fig


def events_plot3d(df: pd.DataFrame, fig=None, split_column='auxiliary', radius_column='charge', event=""):
    if fig is None:
        fig = go.FigureWidget()
    dfa = df[df[split_column] == True]
    dfna = df[df[split_column] == False]
    fig.add_scatter3d(x=dfa.x, y=dfa.y, z=dfa.z, marker=dict(
        size=dfa[radius_column] / np.min(dfa[radius_column]) * 2 + 1,
        color='red',
        opacity=0.9
    ), mode='markers', name=f"{event} {split_column} = True")
    fig.add_scatter3d(x=dfna.x, y=dfna.y, z=dfna.z, marker=dict(
        size=dfa[radius_column] / np.min(dfa[radius_column]) * 2 + 1,
        color='yellow',
        opacity=0.9
    ), mode='markers', name=f"{event} {split_column} = False")

    return fig
