import pandas as pd

from IceCube_geometry import IceCubeGeometry, sensors_plot3d, events_plot3d
from PlotlyStandaloneViewer import PlotlyViewer

if __name__ == "__main__":
    datafile = '../data/batch_1.parquet'
    df = pd.read_parquet(datafile)
    datafile = '../data/sensor_geometry.csv'
    icubeg = IceCubeGeometry(datafile)
    event_id = 121
    df_select = df[(df.index == event_id)]
    df_select = icubeg.match_id_to_coordinate(df_select)
    f = sensors_plot3d(icubeg.sensor_geometry)
    f = events_plot3d(df_select, fig=f, event=f"event {event_id}")
    win = PlotlyViewer(f)
