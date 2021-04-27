from typing import Optional
from unittest import TestCase

from gallium.obj.builder import ObjectBuilder
from gallium.obj.decorator import to_string


class ObjectBuilderTest(TestCase):
    @to_string
    class TargetWithNoConstructorAndDecorator:
        alpha: int
        bravo: str
        charlie: Optional[bool] = False

    @to_string
    class TargetWithNoDecorator:
        alpha: int
        bravo: str
        charlie: Optional[bool] = False

        def __init__(self, alpha, bravo):
            self.alpha = alpha
            self.bravo = bravo

    def test_builder_with_no_constructor_and_no_decorator(self):
        target = ObjectBuilder(ObjectBuilderTest.TargetWithNoConstructorAndDecorator) \
            .alpha(1234) \
            .bravo('foobar') \
            .build()

    def test_builder_with_constructor_and_no_decorator(self):
        target = ObjectBuilder(ObjectBuilderTest.TargetWithNoDecorator) \
            .alpha(1234) \
            .bravo('foobar') \
            .charlie(True) \
            .build()

        self.assertEqual(1234, target.alpha)
        self.assertEqual('foobar', target.bravo)
        self.assertEqual(True, target.charlie)
