from unittest import TestCase

from src.NMI_Reader.reader import Reader


class TestReader(TestCase):
    def test_compartmentalise(self):
        reader = Reader("NEM12_Test_Data.csv")
        reader.compartmentalise()
        meters = reader.get_meters()
        print('fin')

