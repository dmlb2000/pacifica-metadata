#!/usr/bin/python
"""
Test the files ORM object
"""
from datetime import datetime
from time import mktime
from unittest import main
from json import dumps
from metadata.orm.test.base import TestBase
from metadata.orm.files import Files
from metadata.orm.transactions import Transactions
from metadata.orm.test.transactions import SAMPLE_TRANSACTION_HASH, TestTransactions

SAMPLE_FILE_HASH = {
    "_id": 127,
    "name": "test.txt",
    "subdir": "a/b",
    "vtime": int(mktime(datetime.now().timetuple())),
    "mtime": int(mktime(datetime.now().timetuple())),
    "ctime": int(mktime(datetime.now().timetuple())),
    "size": 1234,
    "transaction_id": SAMPLE_TRANSACTION_HASH['_id']
}

class TestFiles(TestBase):
    """
    Test the Files ORM object
    """
    obj_cls = Files
    obj_id = Files.id

    @classmethod
    def dependent_cls(cls):
        """
        Return dependent classes for the Files object
        """
        return TestTransactions.dependent_cls() + [Files]

    @classmethod
    def base_create_dep_objs(cls):
        """
        Create all objects that Files depend on.
        """
        trans = Transactions()
        TestTransactions.base_create_dep_objs()
        trans.from_hash(SAMPLE_TRANSACTION_HASH)
        trans.save(force_insert=True)

    def test_files_hash(self):
        """
        Test the hash portion using base object method.
        """
        self.base_test_hash(SAMPLE_FILE_HASH)

    def test_files_json(self):
        """
        Test the hash portion using base object method.
        """
        self.base_test_json(dumps(SAMPLE_FILE_HASH))

    def test_files_where(self):
        """
        Test the hash portion using base object method.
        """
        self.base_where_clause(SAMPLE_FILE_HASH)

if __name__ == '__main__':
    main()
