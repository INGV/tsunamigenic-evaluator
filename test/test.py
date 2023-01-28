import unittest
import sys
import json
#from main.api.phase import Phase
sys.path.insert(1, '.')
#from deepdiff import DeepDiff

class Test(unittest.TestCase):
    def test_process(self):

        phases_data = {}
        for type in ['P', 'S']:
            with open(f"assets/json/ttimes_{type}.json", 'r') as f:
                phases_data[type] = json.load(f)

        data = {
            'phases_data': phases_data,
            'lat': 45.492599,
            'lon': 9.19289,
            'depth': 50,
            'time': 100,
            'phases': ['P', 'S'],
            'azimuth_interval': 30
        }
        phase = Phase(**data)
        data, error = phase.get_geojson()
        self.assertEqual(True, bool(data))


if __name__ == '__main__':
    unittest.main()