"""
service.py

Service BentoML exposant le modèle de prédiction de consommation énergétique.

Le service :
- reçoit et valide les informations métier d'un bâtiment ;
- calcule les variables dérivées attendues par le pipeline ;
- construit les features dans l'ordre utilisé à l'entraînement ;
- appelle le pipeline scikit-learn sauvegardé avec BentoML ;
- renvoie la consommation énergétique annuelle prédite.
"""

import bentoml
import pandas as pd

from api.schemas import BuildingInput, PredictionOutput


@bentoml.service
class SeattleEnergyService:
    """Service de prédiction de la consommation énergétique des bâtiments."""

    def __init__(self):
        """Charge le pipeline enregistré dans le Model Store BentoML."""

        self.model = bentoml.sklearn.load_model(
            "seattle_energy_model:g2scdqmsgk6gjlax"
        )

    @bentoml.api
    def predict(self, data: BuildingInput) -> PredictionOutput:
        """
        Prédit la consommation énergétique annuelle d'un bâtiment.

        Les données métier validées sont transformées en variables
        compatibles avec le pipeline entraîné avant l'inférence.
        """

        # Variables dérivées créées lors de la Mission 1
        floor_area_per_floor = (
            data.PropertyGFATotal / data.NumberofFloors
        )

        has_parking = int(data.PropertyGFAParking > 0)

        building_age = 2016 - data.YearBuilt

        # Construction des features dans l'ordre exact attendu par le pipeline
        model_input = pd.DataFrame(
            [
                {
                    "PropertyGFATotal": data.PropertyGFATotal,
                    "NumberofFloors": data.NumberofFloors,
                    "FloorAreaPerFloor": floor_area_per_floor,
                    "HasParking": has_parking,
                    "BuildingAge": building_age,
                    "Latitude": data.Latitude,
                    "Longitude": data.Longitude,
                    "PrimaryPropertyType": data.PrimaryPropertyType.value,
                    "LargestPropertyUseType": data.LargestPropertyUseType.value,                    
                }
            ],
            columns=[
                "PropertyGFATotal",
                "NumberofFloors",
                "FloorAreaPerFloor",
                "HasParking",
                "BuildingAge",
                "Latitude",
                "Longitude",
                "PrimaryPropertyType",
                "LargestPropertyUseType",
            ],
        )

        # Prédiction de la consommation énergétique
        prediction = self.model.predict(model_input)[0]

        return PredictionOutput(
            predicted_site_energy_kbtu=float(prediction)
        )