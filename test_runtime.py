import unittest

from app import add
from runtime_probe import run_probe


class TestRuntime(unittest.TestCase):
    def test_add(self) -> None:
        self.assertEqual(add(1, 2), 3)

    def test_probe_marker(self) -> None:
        # Marker for logs (baseline)
        print("PROBE_OK{unittest-ran}")

    def test_runtime_probe(self) -> None:
        out = run_probe()
        print(out)


if __name__ == "__main__":
    unittest.main()
