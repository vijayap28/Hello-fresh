import unittest
from unittest.mock import patch, mock_open
from hf_bi_python_excercise.main import process_recipes, convert_time

# Your test_data goes here...

test_data = [
    {
        "name": "Green Curry with Tofu",
        "ingredients": "Ingredients for chili paste:\n2 green hot chilies (Thai chilies)\n1 tablespoon chopped shallots\n1 teaspoon chopped galangal \n1/2 teaspoon chopped kaffir lime rind\n1 tablespoon chopped garlic\n1 tablespoon chopped lemongrass\n1 tablespoon chopped krachai\n1/4 teaspoon roasted cumin seeds\n1/4 teaspoon roasted coriander seeds\n1/2 teaspoon salt\nOther ingredients:\n1 cup sliced eggplants\n1/4 cup smaller pea-like eggplants (makheau phuang)\n1/3 cup sliced onion\n70 grams sliced chicken (or firm tofu)\n1 teaspoon sugar\n1 tablespoon fish sauce (or soy sauce for vegetarians)\n3 kaffir lime leaves\n2 stems sweet basil (horapaa)\n1 cup coconut milk\n1 cup water\n(Again, chicken can be replaced tofu)",
        "url": "http://www.101cookbooks.com/archives/000130.html",
        "image": "http://www.101cookbooks.com/mt-static/images/food/.jpg",
        "cookTime": "",
        "recipeYield": "",
        "datePublished": "2004-12-01",
        "prepTime": "",
        "description": "101 Cookbooks: Green Curry with Tofu Recipe"
    },
    {
        "name": "Full Moon Brownie Recipe",
        "ingredients": "7 ounces Black Pearl bar (about 2 bars) or Black Pearl chips (1 3/4 bags)\n1 stick unsalted butter {4 oz.},\n3 tablespoons cocoa powder\n3 large eggs\n1 1/4 cup sugar\n1 tablespoon vanilla extract\n1 teaspoon salt\n1 tablespoon fresh ginger, peeled and minced\n3/4 cup mini marshmallows\n1 cup all purpose flour",
        "url": "http://www.101cookbooks.com/archives/000137.html",
        "image": "http://www.101cookbooks.com/mt-static/images/food/moonbrownies.jpg",
        "cookTime": "PT18M",
        "recipeYield": "",
        "datePublished": "2005-01-17",
        "prepTime": "PT15M",
        "description": "101 Cookbooks: Full Moon Brownies Recipe"
    }
]

test_data_2 = [
    {
        "name": "White Chili",
        "ingredients": "1 whole Fryer Chicken, Cut Up (or 3 Cups Cooked Chicken)\n1 whole Medium Onion, Diced\n4 cloves Garlic, Minced\n2 whole Cans Green Chilies, Chopped\n1 pound Dried Great Northern Beans, Rinsed\n8 cups Chicken Broth\n1 whole Jalapeno, Sliced\n1-1/2 Tablespoon Ground Cumin\n1/2 teaspoon Paprika\n1/2 teaspoon Cayenne Pepper\n Salt To Taste\n White Pepper, To Taste\n1 cup Whole Milk\n2 Tablespoons Masa (corn Flour) OR Cornmeal\n Grated Monterey Jack, To Taste\n Sour Cream For Garnish\n Cilantro For Garnish\n Guacamole (optional)\n Pico De Gallo (optional)\n Corn Tortillas, Warmed",
        "url": "http://thepioneerwoman.com/cooking/2010/01/simple-hearty-white-chili/",
        "image": "http://static.thepioneerwoman.com/cooking/files/2010/07/4243109382_1a797f44d2.jpg",
        "cookTime": "PT2H",
        "recipeYield": "8",
        "datePublished": "2010-01-04",
        "prepTime": "PT25M",
        "description": "I love white chili. And just like regular chili, there are as many incarnations as there are "
                       "grains of sand in all the beache..."
    },
    {
        "name": "Easy Green Chile Enchiladas",
        "ingredients": "1 whole Onion, Diced\n2 Tablespoons Butter\n1 can (15 Ounce) Green Enchilada Sauce\n2 cans (4 Ounce) Chopped Green Chilies\n12 whole Corn Tortillas\n2 cups Freshly Grated Cheddar (or Cheddar-jack) Cheese (or Any Cheese You'd Like)\n Sour Cream\n Salsa\n Pico De Gallo (optional)\n Guacamole (optional)\n Cilantro Leaves, Optional",
        "url": "http://thepioneerwoman.com/cooking/2012/05/easy-green-chile-enchiladas/",
        "image": "http://static.thepioneerwoman.com/cooking/files/2012/05/enchilada.jpg",
        "cookTime": "PT10M",
        "recipeYield": "4",
        "datePublished": "2012-05-31",
        "prepTime": "PT5M",
        "description": "When I was in Albuquerque with Marlboro Man and the boys a month ago, I had a really fun book signing. Such incredibly nice a..."
    }
]

test_data_3 = [
    {
        "name": "Lazy Chiles Rellenos",
        "ingredients": "8 whole Roasted, Peeled, And Seeded Green Chiles\n1-1/2 cup Monterey Jack Cheese, Grated\n5 whole Large Eggs\n2 cups Whole Milk\n Salt And Black Pepper To Taste\n1/2 teaspoon Paprika\n1/4 teaspoon Cayenne Pepper",
        "url": "http://thepioneerwoman.com/cooking/2009/11/lazy-chiles-rellenos/",
        "image": "http://static.thepioneerwoman.com/cooking/files/2010/07/4098250665_65310ab692.jpg",
        "cookTime": "PT45M",
        "recipeYield": "9",
        "datePublished": "2009-11-12",
        "prepTime": "PT5M",
        "description": "This dish ain't fancy.     This dish ain't difficult to make. (Huh. Understatement of the modern era.)    This dish...ain't n..."
    }
]


class TestProcessRecipes(unittest.TestCase):
    def test_convert_time(self):
        cook_time, prep_time = convert_time("1H20M", "1H20M")
        self.assertEqual(cook_time, 80)
        self.assertEqual(prep_time, 80)

        cook_time, prep_time = convert_time("1H", "20M")
        self.assertEqual(cook_time, 60)
        self.assertEqual(prep_time, 20)

        cook_time, prep_time = convert_time("20M", "1H20M")
        self.assertEqual(cook_time, 20)
        self.assertEqual(prep_time, 80)

    @patch("builtins.open", new_callable=mock_open)
    @patch("csv.writer")
    def test_process_recipes(self, mock_csv_writer, mock_open):
        # test_data for unknown difficulty
        chilies_recipes, difficulty_levels = process_recipes(test_data)
        self.assertEqual(len(chilies_recipes), 1)
        self.assertEqual(len(difficulty_levels), 1)
        self.assertEqual(len(difficulty_levels["Unknown"]), 1)

        # test for Hard and Easy difficulty
        chilies_recipes, difficulty_levels = process_recipes(test_data_2)
        self.assertEqual(len(chilies_recipes), 2)
        self.assertEqual(len(difficulty_levels), 2)
        self.assertEqual(len(difficulty_levels["Hard"]), 1)
        self.assertEqual(len(difficulty_levels["Easy"]), 1)
        self.assertEqual(len(difficulty_levels["Medium"]), 0)

        # test for Medium difficulty
        chilies_recipes, difficulty_levels = process_recipes(test_data_3)
        self.assertEqual(len(chilies_recipes), 1)
        self.assertEqual(len(difficulty_levels), 1)
        self.assertEqual(len(difficulty_levels["Easy"]), 0)
        self.assertEqual(len(difficulty_levels["Medium"]), 1)


if __name__ == '__main__':
    unittest.main()
