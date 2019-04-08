import copernicus

if __name__ == '__main__':
    api = copernicus.API()

    api.get_data(
        'ENSEMBLE-FORECAST', 'CO', '2019-03-21T00:00:00Z', 1000, 'Ukraine',
        '2019-03-21T02:00:00Z'
    )
