"""Developer regression cases for TASK-049's exact native-value contract."""
import unittest

from qa_master._paired_contract import PairedEvaluationError, strict_json, typed


class NativeValueContractTests(unittest.TestCase):
    def test_negative_zero_is_rejected_before_integer_information_is_lost(self):
        for raw in (b'-0', b'{"n":-0}', b'[1,-0]'):
            with self.subTest(raw=raw), self.assertRaisesRegex(
                PairedEvaluationError, 'NONCANONICAL_INTEGER'
            ):
                strict_json(raw)
        self.assertEqual(strict_json(b'{"text":"-0","n":0}'), {'text': '-0', 'n': 0})

    def test_nested_container_depth_boundary(self):
        value = 0
        for _ in range(16):
            value = [value]
        typed('JSON', value)
        with self.assertRaisesRegex(PairedEvaluationError, 'JSON_DEPTH_LIMIT'):
            typed('JSON', [value])

    def test_nodes_include_object_keys_and_container_roots(self):
        typed('JSON', {'x': [0] * 4093})
        with self.assertRaisesRegex(PairedEvaluationError, 'JSON_NODE_LIMIT'):
            typed('JSON', {'x': [0] * 4094})

    def test_native_types_are_not_coerced(self):
        for kind, value in [('BOOLEAN', 1), ('INTEGER', True), ('INTEGER', '1'),
                            ('STRING_SET', '["a"]')]:
            with self.subTest(kind=kind), self.assertRaises(PairedEvaluationError):
                typed(kind, value)
        typed('JSON', '1')
        typed('INTEGER', 1)
        typed('DECIMAL', '1')
