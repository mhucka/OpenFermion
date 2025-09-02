import os
import unittest
import h5py
import numpy

from openfermion.chem.molecular_data import MolecularData


class MolecularDataSecurityTest(unittest.TestCase):

    def setUp(self):
        self.geometry = [('H', (0., 0., 0.)), ('H', (0., 0., 0.7414))]
        self.basis = 'sto-3g'
        self.multiplicity = 1
        self.charge = 0
        self.description = "H2"
        self.filename = "h2_sto-3g_singlet_0.7414"
        self.molecule = MolecularData(self.geometry, self.basis,
                                      self.multiplicity, self.charge,
                                      self.description, self.filename)
        self.molecule.save()

    def tearDown(self):
        os.remove(self.filename + '.hdf5')
        if os.path.exists('large_file.hdf5'):
            os.remove('large_file.hdf5')

    def test_file_size_limit(self):
        with open('large_file.hdf5', 'wb') as f:
            f.write(os.urandom(101 * 1024 * 1024))  # 101MB
        with self.assertRaises(ValueError):
            MolecularData(filename='large_file').load()

    def test_corrupted_file(self):
        with open('corrupted_file.hdf5', 'wb') as f:
            f.write(b"this is not a hdf5 file")
        with self.assertRaises(ValueError):
            MolecularData(filename='corrupted_file').load()
        os.remove('corrupted_file.hdf5')
