import unittest
from utils.calculations import calculate_age, calculate_years_of_service, is_eligible, calculate_annuity

class TestCalculations(unittest.TestCase):
    def test_calculate_age(self):
        age = calculate_age("1980-01-01")
        self.assertTrue(43 <= age <= 44)  # Depends on current year

    def test_calculate_years_of_service(self):
        service = [("2010-01-01", "2020-01-01")]
        years = calculate_years_of_service(service)
        self.assertAlmostEqual(years, 10, places=1)

    def test_is_eligible(self):
        self.assertTrue(is_eligible(55, 10))
        self.assertFalse(is_eligible(50, 5))

    def test_calculate_annuity(self):
        annuity = calculate_annuity(20, 60000)
        self.assertEqual(annuity, 12000)

if __name__ == "__main__":
    unittest.main()