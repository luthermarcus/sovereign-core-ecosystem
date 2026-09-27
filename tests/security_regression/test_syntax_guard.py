import unittest, py_compile, os

class TestSyntaxGuardRegression(unittest.TestCase):
    def test_modules_for_syntax_anomalies(self):
        modules_dir = os.path.expanduser("~/sovereign-core-ecosystem/modules")
        for filename in os.listdir(modules_dir):
            if filename.endswith(".py"):
                filepath = os.path.join(modules_dir, filename)
                try:
                    py_compile.compile(filepath, doraise=True)
                except py_compile.PyCompileError as e:
                    self.fail(f"Regression detected: Syntax anomaly in {filename} -> {e}")

if __name__ == "__main__":
    unittest.main()
