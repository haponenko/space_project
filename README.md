# Space project  
## Quick start  
1. Please, register at [http://data.regional.atmosphere.copernicus.eu/openwis-user-portal/srv/en/user.register.get](http://data.regional.atmosphere.copernicus.eu/openwis-user-portal/srv/en/user.register.get) and confirm your email.  
2. Locate to the **src** folder in this repository and run `python3` or just rewrite **src/main.py**.  
3. Examples of data loading:  
```python
import copernicus

api = copernicus.API('your-email', 'your-password')

api.get_data(
    'ENSEMBLE-FORECAST', 'CO', '2019-03-21T02:00:00Z', 1000, 'Ukraine',
    '2019-03-21T00:00:00Z'
)
```  
Parameters explanation:  
1. Service. Available options: `ENSEMBLE-FORECAST`, `ENSEMBLE-FORECAST`.  
2. Specie. Available options: `CO`, `NH3`, `NO`, `NO2`, `O3`.  
3. Validity time. Format: `%Y-%m-%dT%H:%M:%SZ`.  
4. Level. Available options: `0`, `50`, `250`, `500`, `1000`, `2000`, `3000`, `5000`.  
5. Area. Available options: `Ukraine`.  
6. Run base time. Format: `%Y-%m-%dT%H:%M:%SZ`.  
# Analysis  
```bash
docker build -t space .
docker run --rm -p 8888:8888 -p 4040:4040 -e JUPYTER_ENABLE_LAB=yes -v $(pwd):/code space
```  
And navigate to [0.0.0.0:8888](0.0.0.0:8888).  
Note: do not forget your token.  

nc data: https://drive.google.com/drive/u/0/folders/1j95WYrZiWjknKwt7VjZQNIKwu6HhGkNU