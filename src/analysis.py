from pathlib import Path
import datetime

import pandas as pd
import numpy as np
import shapefile
import pupygrib
import ogr
from osgeo import gdal
from scipy.io import netcdf


class Analysis:
    ELEMENTS = ['O3', 'NO2', 'CO']

    def __init__(self):
        self.data_folder = Path('data')
        self.shp_folder = self.data_folder / 'shp'
        self.nc_folder = self.data_folder / 'nc'
        # self.grib_folder = self.data_folder / 'grib'

        self.grib = []
        self.shp = []


    # def get_data(self, date: datetime.date = None):
    #     """
    #     Get shapefile(s) by date, if provided, or all of them in data folder.
    #
    #     :param date: datetime.date, when flight took place, mentioned in
    #     shapefiles names
    #     """
    #     self.shp = []
    #
    #     if date:
    #         date_str =  date.strftime("%Y%m%d")
    #         for file_ in self.shp_folder.iterdir():
    #             if date_str in file_.name and file_.suffix == '.shp':
    #                 self._get_shp(file_)
    #                 break
    #     else:
    #         for file_ in self.shp_folder.iterdir():
    #             self._get_shp(file_)

    # def _get_shp(self, file_):
    #     with shapefile.Reader(str(file_)) as shp_file:
    #         self.shp.append(shp_file)

    # def get_grib(self, file_, date: datetime.datetime):
    #     self.grib = []
    #
    #     date_str = date.strftime("%Y%m%d%H")
    #     if date_str in file_.name:
    #         with file_.open() as grib_file:
    #             grib, = pupygrib.read(grib_file)
    #         self.grib.append(grib)


    def get_nc(self, file_, date: datetime.datetime, element: str):
        date_str = date.strftime("%Y%m%d%H")
        if date_str in file_.name and element in file_.name:
            return netcdf.netcdf_file(file_, 'r')

    def analyse(self, date: datetime.date = None):
        # Get data
        # self.get_data()
        data = []
        if date:
            date_str = date.strftime("%Y%m%d")
            for file_ in self.shp_folder.iterdir():
                if date_str in file_.name and file_.suffix == '.shp':
                    with shapefile.Reader(str(file_)) as shp_file:
                        # self.shp.append(shp_file)

                        records = shp_file.records()
                        fields = shp_file.fields[1:]
                        fields_names = [field[0] for field in fields]

                        data = pd.DataFrame(
                            np.array(records), columns=fields_names
                        )

                        points_x = np.empty(len(records))
                        points_y = np.empty(len(records))

                        shp = ogr.Open(shapefile)
                        layer = shp.GetLayer()
                        i = 0
                        while i < len(records):
                            point = layer.GetFeature(i)
                            geom = point.GetGeometryRef()
                            points_x[i] = geom.GetPoint(0)[0]
                            points_y[i] = geom.GetPoint(0)[1]
                            i += 1

                        data['lat'] = points_x
                        data['long'] = points_y

                        for element in self.ELEMENTS:
                            data_clean = data.dropna(axis=1, how='all')
                            if element in data_clean.columns:
                                data_clean = data_clean.dropna(how='any', axis=0, subset=[element])
                                print(data_clean)
                            else:
                                continue

        return data

        # for shp in self.shp:
        #     records = shp.records()
        #     fields = shp.fields[1:]
        #     fields_names = [field[0] for field in fields]
        #
        #     data = pd.DataFrame(np.array(records), columns=fields_names)
