from data_analysis import *
import unittest
import hollywood

class TestStringMethods(unittest.TestCase):

        
    def test_max_hub(self):
        data = hollywood.get_json_data()
        hub_actors = get_max_hub_actor(data)
        top_actor = hub_actors[len(hub_actors) - 1]
        self.assertEqual(top_actor, "Bruce Willis")
        
    def test_max_age_group(self):
        data = hollywood.get_json_data()
        age_groups = get_richest_age_group(data)
        max_index = age_groups.index(max(age_groups))
        self.assertEqual(max_index, 8)
        
        

if __name__ == '__main__':
    unittest.main()






