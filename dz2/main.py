import os
import toml
import subprocess
import networkx as nx
from typing import Dict, List
from graphviz import Source


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


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Dependency Visualizer")
    parser.add_argument("config", help="Path to the configuration file")
    args = parser.parse_args()

    visualizer = DependencyVisualizer(args.config)
    visualizer.visualize()