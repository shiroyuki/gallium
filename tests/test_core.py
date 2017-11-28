from unittest import TestCase
from unittest.mock import Mock

from imagination.meta.container  import Entity, Factorization, Lambda

from gallium.core import Core


class UnitTest(TestCase):
    def setUp(self):
        self.container = Mock()

        self.assembler = Mock()
        self.assembler.core = self.container

        self.core = Core(self.assembler)

    def test_get(self):
        self.core.get('something')

        self.assertEqual(1, self.container.get.call_count)

    def test_load(self):
        self.core.load('something.xml')

        self.assertEqual(1, self.assembler.load.call_count)

    def test_set_entity(self):
        expected_type = Entity

        fake_id = 'foo'

        self.container.update_metadata = Mock(
            side_effect = lambda x: self.assertIsInstance(x.get(fake_id), expected_type)
        )

        self.core.set_entity(fake_id, 'app.bar')

    def test_set_factorization(self):
        expected_type = Factorization

        fake_id = 'foo'

        self.container.update_metadata = Mock(
            side_effect = lambda x: self.assertIsInstance(x.get(fake_id), expected_type)
        )

        self.core.set_factorization(fake_id, 'app.bar', 'make')

    def test_set_lambda(self):
        expected_type = Lambda

        fake_id = 'foo'

        self.container.update_metadata = Mock(
            side_effect = lambda x: self.assertIsInstance(x.get(fake_id), expected_type)
        )

        self.core.set_lambda(fake_id, 'app.bar')
