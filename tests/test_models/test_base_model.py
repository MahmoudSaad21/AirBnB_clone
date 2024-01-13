#!/usr/bin/python3
"""Defines unittests for models/base_model.py.
Unittest classes:
    TestBaseModelInstantiation
    TestBaseInstancePrint
    TestBaseModelSave
    TestBaseFromJsonString
    TestBaseModelToDict
"""
import unittest
from models import storage
from models.base_model import BaseModel
from models.engine.file_storage import FileStorage
from datetime import datetime
from time import sleep
import time
import uuid
import json
import os
import re

class TestBaseModelInstantiation(unittest.TestCase):
    """Unittests for testing instantiation of the BaseModel class."""

    def testIsInstanceOf(self):
        """Test instance"""
        b1 = BaseModel()
        self.assertIsInstance(b1, BaseModel)
        self.assertEqual(str(type(b1)), "<class 'models.base_model.BaseModel'>")
        self.assertTrue(issubclass(type(b1), BaseModel))

    def testContainsId(self):
        """Test if id attribute exists"""
        b1 = BaseModel()
        self.assertTrue(hasattr(b1, "id"))

    def testIdType(self):
        """Test if `id` attribute type"""
        b1 = BaseModel()
        self.assertEqual(type(b1.id), str)

    def testCompareTwoInstancesId(self):
        """Compare distinct instances ids"""
        b1 = BaseModel()
        b2 = BaseModel()
        self.assertNotEqual(b1.id, b2.id)

    def testUuid(self):
        """Test that id is a valid uuid"""
        b1 = BaseModel()
        b2 = BaseModel()
        for inst in [b1, b2]:
            uuid = inst.id
            with self.subTest(uuid=uuid):
                self.assertIs(type(uuid), str)
                self.assertRegex(uuid,
                                 '^[0-9a-f]{8}-[0-9a-f]{4}'
                                 '-[0-9a-f]{4}-[0-9a-f]{4}'
                                 '-[0-9a-f]{12}$')
        self.assertNotEqual(b1.id, b2.id)

    def testUniqId(self):
        """Tests for unique user ids."""
        u = [BaseModel().id for i in range(1000)]
        self.assertEqual(len(set(u)), len(u))

    def testTwoModelsUniqueIds(self):
        b1 = BaseModel()
        b2 = BaseModel()
        self.assertNotEqual(b1.id, b2.id)

    def testNewInstanceStoredInObjects(self):
        self.assertIn(BaseModel(), storage.all().values())

    def testContainsCreatedAt(self):
        """Checks `created_at` attribute existence"""
        b1 = BaseModel()
        self.assertTrue(hasattr(b1, "created_at"))

    def testCreatedAtInstance(self):
        """Checks `created_at` attribute's type"""
        b1 = BaseModel()
        self.assertIsInstance(b1.created_at, datetime)

    def testContainsUpdatedAt(self):
        """Checks `updated_at` attribute existence"""
        b1 = BaseModel()
        self.assertTrue(hasattr(b1, "updated_at"))

    def testUpdatedAtInstance(self):
        """Check `updated_at` attribute type"""
        b1 = BaseModel()
        self.assertIsInstance(b1.updated_at, datetime)

    def testDatetimeCreated(self):
        """Tests if updated_at & created_at are current at creation."""
        date_now = datetime.now()
        b1 = BaseModel()
        diff = b1.updated_at - b1.created_at
        self.assertTrue(abs(diff.total_seconds()) < 0.01)
        diff = b1.created_at - date_now
        self.assertTrue(abs(diff.total_seconds()) < 0.1)

    def testIdIsPublicStr(self):
        self.assertEqual(str, type(BaseModel().id))

    def testCreatedAtIsPublicDatetime(self):
        self.assertEqual(datetime, type(BaseModel().created_at))

    def testUpdatedAtIsPublicDatetime(self):
        self.assertEqual(datetime, type(BaseModel().updated_at))

    def testStrRepresentation(self):
        dt = datetime.today()
        dt_repr = repr(dt)
        b1 = BaseModel()
        b1.id = "123456"
        b1.created_at = b1.updated_at = dt
        b1str = b1.__str__()
        self.assertIn("[BaseModel] (123456)", b1str)
        self.assertIn("'id': '123456'", b1str)
        self.assertIn("'created_at': " + dt_repr, b1str)
        self.assertIn("'updated_at': " + dt_repr, b1str)

    def testArgsUnused(self):
        b1 = BaseModel(None)
        self.assertNotIn(None, b1.__dict__.values())

    def testInstantiationWithKwargs(self):
        dt = datetime.today()
        dt_iso = dt.isoformat()
        b1 = BaseModel(id="345", created_at=dt_iso, updated_at=dt_iso)
        self.assertEqual(b1.id, "345")
        self.assertEqual(b1.created_at, dt)
        self.assertEqual(b1.updated_at, dt)

    def testInstantiationWithNoneKwargs(self):
        with self.assertRaises(TypeError):
            BaseModel(id=None, created_at=None, updated_at=None)

    def testInstantiationWithArgsAndKwargs(self):
        dt = datetime.today()
        dt_iso = dt.isoformat()
        b1 = BaseModel("12", id="345", created_at=dt_iso, updated_at=dt_iso)
        self.assertEqual(b1.id, "345")
        self.assertEqual(b1.created_at, dt)
        self.assertEqual(b1.updated_at, dt)

class TestBaseModelInstancePrint(unittest.TestCase):
    """Unittest for testing the __str__ method."""

    def testStrReturn(self):
        """Unittest for testing the return value of __str__ method."""
        b1 = BaseModel()
        Dika = "[{}] ({}) {}".format("BaseModel", b1.id, str(b1.__dict__))
        self.assertEqual(str(b1), Dika)

    def testStr(self):
        """test that the str method has the correct output"""
        b1 = BaseModel()
        string = "[BaseModel] ({}) {}".format(b1.id, b1.__dict__)
        self.assertEqual(string, str(b1))

    def testOfStr(self):
        """Tests for __str__ method."""
        b1 = BaseModel()
        rex = re.compile(r"^\[(.*)\] \((.*)\) (.*)$")
        res = rex.match(str(b1))
        self.assertIsNotNone(res)
        self.assertEqual(res.group(1), "BaseModel")
        self.assertEqual(res.group(2), b1.id)
        s = res.group(3)
        s = re.sub(r"(datetime\.datetime\([^)]*\))", "'\\1'", s)
        d = json.loads(s.replace("'", '"'))
        d2 = b1.__dict__.copy()
        d2["created_at"] = repr(d2["created_at"])
        d2["updated_at"] = repr(d2["updated_at"])
        self.assertEqual(d, d2)

class TestBaseModelSaveMethod(unittest.TestCase):
    """Unittest for testing the save method."""

    def testValidatesSave(self):
        """Check save models"""
        b1 = BaseModel()
        updated_at_1 = b1.updated_at
        b1.save()
        updated_at_2 = b1.updated_at
        self.assertNotEqual(updated_at_1, updated_at_2)

    def testOneSave(self):
        b1 = BaseModel()
        sleep(0.05)
        first_updated_at = b1.updated_at
        b1.save()
        self.assertLess(first_updated_at, b1.updated_at)

    def testTwoSaves(self):
        b1 = BaseModel()
        sleep(0.05)
        first_updated_at = b1.updated_at
        b1.save()
        second_updated_at = b1.updated_at
        self.assertLess(first_updated_at, second_updated_at)
        sleep(0.05)
        b1.save()
        self.assertLess(second_updated_at, b1.updated_at)

    def testSaveWithArg(self):
        b1 = BaseModel()
        with self.assertRaises(TypeError):
            b1.save(None)

class TestBaseModelToDictMethod(unittest.TestCase):
    """Unittest for testing the to_dict method of the BaseModel class."""

    def testClassNamePresent(self):
        """Test className present"""
        b1 = BaseModel()
        dic = b1.to_dict()
        self.assertNotEqual(dic, b1.__dict__)

    def testAttributeISOFormat(self):
        """Test datetime field isoformated"""
        b1 = BaseModel()
        dic = b1.to_dict()
        self.assertEqual(type(dic['created_at']), str)
        self.assertEqual(type(dic['updated_at']), str)

    def testToDictType(self):
        b1 = BaseModel()
        self.assertTrue(dict, type(b1.to_dict()))

    def testToDictContainsCorrectKeys(self):
        b1 = BaseModel()
        self.assertIn("id", b1.to_dict())
        self.assertIn("created_at", b1.to_dict())
        self.assertIn("updated_at", b1.to_dict())
        self.assertIn("__class__", b1.to_dict())

    def testToDictContainsAddedAttributes(self):
        b1 = BaseModel()
        b1.name = "Holberton"
        b1.my_number = 98
        self.assertIn("name", b1.to_dict())
        self.assertIn("my_number", b1.to_dict())

    def testToDictDatetimeAttributesAreStrs(self):
        b1 = BaseModel()
        b1_dict = b1.to_dict()
        self.assertEqual(str, type(b1_dict["created_at"]))
        self.assertEqual(str, type(b1_dict["updated_at"]))

    def testToDictOutput(self):
        dt = datetime.today()
        b1 = BaseModel()
        b1.id = "123456"
        b1.created_at = b1.updated_at = dt
        tdict = {
            'id': '123456',
            '__class__': 'BaseModel',
            'created_at': dt.isoformat(),
            'updated_at': dt.isoformat()
        }
        self.assertDictEqual(b1.to_dict(), tdict)

    def testContrastToDictDunderDict(self):
        b1 = BaseModel()
        self.assertNotEqual(b1.to_dict(), b1.__dict__)

    def testToDictWithArg(self):
        b1 = BaseModel()
        with self.assertRaises(TypeError):
            b1.to_dict(None)

if __name__ == "__main__":
    unittest.main()
