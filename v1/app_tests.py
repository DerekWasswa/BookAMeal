import unittest
from app import signUp, login, getAllMeals, addMeal, updateAMeal, deleteAMeal, setMenuOfTheDay, getMenuOfTheDay, makeOrder, modifyOrder, getAllOrders, appUsers, appVendorAdmins, appMeals, appMenu, appOrders

class AppTest(unittest.TestCase):
    
	def test_sign_up(self):
		self.assertEqual(signUp(), True)

	def test_login(self):
		self.assertFalse(len(appUsers), 0)
		self.assertEqual(bool(appVendorAdmins), True)
		self.assertEqual(login(), True)

	def test_getting_all_meals(self):
		self.assertTrue(isinstance(getAllMeals, dict))

	def test_add_meal(self):
		self.assertFalse(len(appMeals), 0)

	def test_updating_a_meal(self):
		self.assertFalse(len(appMeals), 0)
		self.assertTrue(isinstance(updateAMeal("mealId"), (int, str)))
	
	def test_deleting_a_meal(self):
		self.assertFalse(len(appMeals), 0)
		self.assertTrue(isinstance(deleteAMeal("mealId"), (int, str)))

	def test_set_menu_of_the_day(self):
		self.assertFalse(len(appMenu), 0)

	def test_get_menu_of_the_day(self):
		self.assertTrue(isinstance(getMenuOfTheDay, dict))

	def test_make_an_order(self):
		self.assertFalse(len(appMenu), 0)
		self.assertFalse(len(appUsers), 0)

	def test_modifying_an_order(self):
		self.assertFalse(len(appOrders), 0)
		self.assertTrue(isinstance(modifyOrder("orderlId"), (int, str)))

	def test_retrieving_all_orders(self):
		self.assertTrue(isinstance(getAllOrders, dict))

if __name__ == '__main__':
	unittest.main()
		