"""
test_api.py

Script de test manuel de l'API Seattle Energy.

Le script peut tester l'API :
- localement, sur http://localhost:3000 ;
- à distance, en fournissant l'URL du service déployé.

Il exécute :
- une requête valide, attendue en HTTP 200 ;
- une requête métier invalide, attendue en HTTP 400.
"""

import argparse

import requests


DEFAULT_BASE_URL = "http://localhost:3000"


def parse_args():
    """Récupère éventuellement l'URL du service à tester."""

    parser = argparse.ArgumentParser(
        description="Teste l'API Seattle Energy."
    )

    parser.add_argument(
        "--url",
        default=DEFAULT_BASE_URL,
        help=(
            "URL de base du service BentoML. "
            f"Valeur par défaut : {DEFAULT_BASE_URL}"
        ),
    )

    return parser.parse_args()


def send_request(api_url, payload, test_name):
    """Envoie une requête et affiche son résultat."""

    response = requests.post(
        api_url,
        json=payload,
        timeout=30,
    )

    print(f"\n--- {test_name} ---")
    print("URL :", api_url)
    print("Code HTTP :", response.status_code)
    print("Réponse :", response.json())


def main():
    """Teste une requête valide puis une requête invalide."""

    args = parse_args()

    base_url = args.url.rstrip("/")
    api_url = f"{base_url}/predict"

    valid_payload = {
        "data": {
            "PropertyGFATotal": 88434,
            "PropertyGFAParking": 0,
            "NumberofFloors": 12,
            "YearBuilt": 1927,
            "Latitude": 47.6122,
            "Longitude": -122.33799,
            "PrimaryPropertyType": "Hotel",
            "LargestPropertyUseType": "Hotel",
        }
    }

    invalid_payload = {
        "data": {
            "PropertyGFATotal": 50000,
            "PropertyGFAParking": 60000,
            "NumberofFloors": 5,
            "YearBuilt": 1985,
            "Latitude": 47.61,
            "Longitude": -122.33,
            "PrimaryPropertyType": "Large Office",
            "LargestPropertyUseType": "Office",
        }
    }

    send_request(
        api_url,
        valid_payload,
        "Requête valide",
    )

    send_request(
        api_url,
        invalid_payload,
        "Requête invalide",
    )


if __name__ == "__main__":
    main()