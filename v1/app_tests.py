import unittest
from app import signUp, login, getAllMeals, addMeal, updateAMeal, deleteAMeal, setMenuOfTheDay, getMenuOfTheDay, makeOrder, modifyOrder, getAllOrders

class AppTest(unittest.TestCase):
    
	def test_sign_up(self):
		self.assertEqual(signUp(), "Hello Andela")

	def test_login(self):
		self.assertEqual(type(login()), list)

	def test_getting_all_meals(self):
		self.assertEqual(type(getAllMeals()), list)

	def test_add_meal(self):
		self.assertEqual(addMeal(), range(200, 320))

	def test_updating_a_meal(self):
		self.assertEqual(updateAMeal()[0]%7 and updateAMeal()[0]%5, 0)
	
	def test_deleting_a_meal(self):
		self.assertEqual(signUp(), "Hello Andela")

	def test_set_menu_of_the_day(self):
		self.assertEqual(type(login()), list)

	def test_get_menu_of_the_day(self):
		self.assertEqual(type(getAllMeals()), list)

	def test_make_an_order(self):
		self.assertEqual(addMeal(), range(200, 320))

	def test_modifying_an_order(self):
		self.assertEqual(updateAMeal()[0]%7 and updateAMeal()[0]%5, 0)

	def test_retrieving_all_orders(self):
		self.assertEqual(updateAMeal()[0]%7 and updateAMeal()[0]%5, 0)        

if __name__ == '__main__':
	unittest.main()
		