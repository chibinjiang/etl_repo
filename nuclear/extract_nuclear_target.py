import json
from datetime import datetime
from nuclear.models import USNuclearTargetModel


def main():
    with open("nuclear/nuclear_targets.json", "r") as fr:
        data = json.load(fr)
        for feature in data['features']:
            point = feature['properties']['City']
            print("Target: ", point)
            model = USNuclearTargetModel()
            model.country = feature['properties']['Country']
            model.point = point
            model.longitude, model.latitude = feature['geometry']['coordinates']
            if not model.id:
                model.updated = datetime.utcnow()
            model.created = datetime.utcnow()
            model.save()


if __name__ == '__main__':
    """
    python -m nuclear.extract_nuclear_target
    """
    main()
