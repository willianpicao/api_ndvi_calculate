import json
from oauthlib.oauth2 import BackendApplicationClient
from requests_oauthlib import OAuth2Session
from PIL import Image
import io
from dotenv import load_dotenv
import os

load_dotenv()

class LandsatRegionNDVICalculator:
    def __init__(self, client_id, client_secret):
        # Inicializa a instância com as credenciais do cliente e URLs relevantes
        self.client_id = client_id
        self.client_secret = client_secret
        self.base_url = "https://sh.dataspace.copernicus.eu/api/v1/"
        self.token_url = "https://identity.dataspace.copernicus.eu/auth/realms/CDSE/protocol/openid-connect/token"
        self.session = self._create_session()  # Cria a sessão OAuth2

    def _create_session(self):
        # Cria e retorna uma sessão OAuth2 com as credenciais do cliente
        client = BackendApplicationClient(client_id=self.client_id)
        oauth = OAuth2Session(client=client)
        token = oauth.fetch_token(token_url=self.token_url, client_secret=self.client_secret, include_client_id=True)
        return oauth

    def _format_date(self, date):
        # Formata a data no formato esperado pelo serviço Copernicus
        return f"{date}T00:00:00Z"

    def download_image(self, geojson_file_path, start_date, end_date,cloudCoverage, evalscript):
        with open(geojson_file_path, 'r') as file:
            geojson_data = json.load(file)

        coordinates = geojson_data['features'][0]['geometry']['coordinates'][0]

        # Constrói o pedido para o serviço Copernicus
        request = {
            "input": {
                "bounds": {
                    "properties": {
                        "crs": "http://www.opengis.net/def/crs/EPSG/0/4326",
                    },
                    "geometry": {
                        "type": "Polygon",
                        "coordinates": [coordinates],
                    },
                },
                "data": [
                    {
                        "type": "sentinel-2-l2a",
                        "dataFilter": {
                            "maxCloudCoverage": cloudCoverage,
                            "timeRange": {
                                "from": self._format_date(start_date),
                                "to": self._format_date(end_date),
                            }
                        },
                    }
                ],
            },
            "output": {
                "width": 520,
                "height": 520,
                "responses": [
                    {
                        "identifier": "default",
                        "format": {
                            "type": "image/jpeg",
                            "quality": 100,
                        },
                    }
                ],
            },
            "evalscript": evalscript,
        }

        url = f"{self.base_url}process"
        response = self.session.post(url, json=request)  # Faz a solicitação para o serviço Copernicus

        if response.status_code == 200:
            content = response.content
            image = Image.open(io.BytesIO(content))
            image.save('output_image.jpeg', 'JPEG')
            print("Imagem salva com sucesso.")
        else:
            print("Erro ao obter a imagem. Código de status:", response.status_code)
            print(response.text)


