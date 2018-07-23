import os
from flask import current_app
import unittest
import tempfile


class FlaskrTestCase(unittest.TestCase):

    def setUp(self):
        self.db_fd, current_app.app.config['DATABASE'] = tempfile.mkstemp()
        current_app.app.config['TESTING'] = True
        self.app = current_app.app.test_client()
        current_app.init_db()

    def tearDown(self):
        os.close(self.db_fd)
        os.unlink(current_app.app.config['DATABASE'])


if __name__ == '__main__':
    unittest.main()
