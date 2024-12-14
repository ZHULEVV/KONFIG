import os
import toml
import subprocess
from pathlib import Path
import networkx as nx
from typing import Dict, List
from graphviz import Source
import unittest


class DependencyVisualizer:
    def __init__(self, config_path: str):
        self.config = self.load_config(config_path)
        self.graph = nx.DiGraph()

    def load_config(self, path: str) -> Dict:
        """Загружает и валидирует конфигурационный файл."""
        if not os.path.exists(path):
            raise FileNotFoundError(f"Config file {path} not found.")
        config = toml.load(path)
        required_keys = ["graphviz_path", "package_name", "output_path", "max_depth", "repository_url"]
        for key in required_keys:
            if key not in config:
                raise ValueError(f"Missing required config key: {key}")
        return config

    def get_dependencies(self, package_name: str, depth: int = 0, max_depth: int = 1) -> Dict[str, List[str]]:
        """Получает зависимости для указанного пакета."""
        if depth > max_depth:
            return {}
        try:
            output = subprocess.check_output(["pip", "show", package_name], text=True)
        except subprocess.CalledProcessError:
            raise ValueError(f"Package {package_name} not found in PyPI.")
        dependencies = {}
        for line in output.splitlines():
            if line.startswith("Requires:"):
                deps = line.split(":")[1].strip().split(", ")
                for dep in deps:
                    if dep:
                        self.graph.add_edge(package_name, dep)
                        dependencies[dep] = self.get_dependencies(dep, depth + 1, max_depth)
        return dependencies

    def generate_graphviz_code(self) -> str:
        """Генерирует код Graphviz для визуализации графа."""
        graphviz_code = "digraph dependencies {\n"
        for node1, node2 in self.graph.edges:
            graphviz_code += f'  "{node1}" -> "{node2}";\n'
        graphviz_code += "}"
        return graphviz_code

    def save_graph(self, output_path: str):
        """Сохраняет граф в файл."""
        code = self.generate_graphviz_code()
        with open(output_path, "w") as f:
            f.write(code)

    def save_png(self, output_path: str):
        """Генерирует PNG-файл из Graphviz-описания."""
        os.environ["PATH"] += os.pathsep + os.path.dirname(self.config["graphviz_path"])
        dot_code = self.generate_graphviz_code()
        dot_file = Source(dot_code)
        png_path = os.path.splitext(output_path)[0] + ".png"
        dot_file.format = "png"
        dot_file.render(png_path, cleanup=True)
        print(f"PNG граф сохранён по пути: {png_path}")

    def visualize(self):
        """Основная функция визуализации."""
        package_name = self.config["package_name"]
        max_depth = int(self.config["max_depth"])
        self.get_dependencies(package_name, max_depth=max_depth)
        graphviz_code = self.generate_graphviz_code()
        print(graphviz_code)
        self.save_graph(self.config["output_path"])
        self.save_png(self.config["output_path"])


class TestDependencyVisualizer(unittest.TestCase):
    def setUp(self):
        self.config_path = "test_config.toml"
        self.test_package = "requests"
        with open(self.config_path, "w") as f:
            f.write(
                f"""
                graphviz_path = "/usr/bin/dot"
                package_name = "{self.test_package}"
                output_path = "test_output.dot"
                max_depth = 1
                repository_url = "https://pypi.org"
                """
            )
        self.visualizer = DependencyVisualizer(self.config_path)

    def tearDown(self):
        if os.path.exists(self.config_path):
            os.remove(self.config_path)
        if os.path.exists("test_output.dot"):
            os.remove("test_output.dot")
        if os.path.exists("test_output.png"):
            os.remove("test_output.png")

    def test_load_config(self):
        config = self.visualizer.config
        self.assertEqual(config["package_name"], self.test_package)
        self.assertEqual(config["max_depth"], 1)

    def test_get_dependencies(self):
        self.visualizer.get_dependencies(self.test_package, max_depth=1)
        self.assertTrue(len(self.visualizer.graph.nodes) > 0)

    def test_generate_graphviz_code(self):
        self.visualizer.get_dependencies(self.test_package, max_depth=1)
        graphviz_code = self.visualizer.generate_graphviz_code()
        self.assertIn("digraph dependencies", graphviz_code)

    def test_save_graph(self):
        self.visualizer.get_dependencies(self.test_package, max_depth=1)
        self.visualizer.save_graph("test_output.dot")
        self.assertTrue(os.path.exists("test_output.dot"))




if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Dependency Visualizer")
    parser.add_argument("config", help="Path to the configuration file")
    args = parser.parse_args()

    visualizer = DependencyVisualizer(args.config)
    visualizer.visualize()
