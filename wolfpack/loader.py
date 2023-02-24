# Social Plaform loader
import importlib

class PluginInterface:
    
    @staticmethod
    def initialize() -> None:
        """Initialize the loader"""
        pass

def import_module(name: str) -> PluginInterface:
    """Import a module"""
    return importlib.import_module(name)

def load_plugin(platfroms: list[str]) -> None:
    """Load a plugin"""
    for platform in platfroms:
        print(f"Loading {platform} platform")
        module = import_module(platform)
        module.initialize()

