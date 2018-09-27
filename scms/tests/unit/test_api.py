"""
DBAPITest
"""
from scms.common import exceptions
from scms.db.api import ChainDao
from scms.db import common
from scms.db.models import ModelBase
from scms.tests.base import BaseTestCase
import unittest


class ChainDAOTest(BaseTestCase):

    def setUp(self):
        ModelBase.metadata.create_all(common.get_engine())

    def tearDown(self):
        # close the session connected to the mysql
        common.get_session().close()
        ModelBase.metadata.drop_all(common.get_engine())
        pass

    def test_add_chain(self):
        chain1 = {'name': ""}
        chain3 = {'name': "chain3"}
        chain_dao = ChainDao()

        self.assertRaises(exceptions.ParamMissing, chain_dao.create_chain, chain1)
        resu = chain_dao.create_chain(chain3)
        self.assertEqual("chain3", resu['name'])

    def test_get_chain(self):
        # test for get_chain_by_name
        chain_dao = ChainDao()
        chain_dao.create_chain({'name': "chain1"})
        res = chain_dao.get_chain_by_name("chain1")
        self.assertEqual("chain1", res['name'])

    def test_delete_chain(self):
        chain_dao = ChainDao()
        chain4 = {'name': "chain4"}
        chain_dao.create_chain(chain4)
        res = chain_dao.get_chain_by_name("chain4")
        self.assertEqual("chain4", res['name'])

        chain_dao.delete_chain("chain4")
        self.assertIsNone(chain_dao.get_chain_by_name("chain4"))

    def test_update_chain(self):
        chain1 = {'name': "chain1"}
        chain_dao = ChainDao()
        chain_dao.create_chain(chain1)
        res = chain_dao.get_chain_by_name("chain1")
        self.assertEqual("chain1", res['name'])

        chain_dao.update_chain('chain1', {'name': "chain1_new"})
        new_res = chain_dao.get_chain_by_id(res['id'])
        self.assertEqual("chain1_new", new_res['name'])

    def test_list_chain_by_attr(self):
        chain1 = {'name': "chain1"}
        chain2 = {'name': "chain2"}
        chain_dao = ChainDao()
        chain_dao.create_chain(chain1)
        chain_dao.create_chain(chain2)

        resu = chain_dao.list_chain_by_attr({})
        self.assertEqual(2, len(resu))


if __name__ == '__main__':
    unittest.main()

