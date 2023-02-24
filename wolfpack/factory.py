from typing import Callable, Any
from .social_platform import SocialPlatform

social_platform_creation_funcs: dict[str, Callable[..., SocialPlatform]] = {}

def register(social_platform_name: str, creation_func: Callable[..., SocialPlatform]):
    """ Registers a social platform creation function."""

    social_platform_creation_funcs[social_platform_name] = creation_func
    print(f"Registered {social_platform_name} creation function")


def unregister(social_platform_name: str):
    """ Unregisters a social platform creation function."""

    del social_platform_creation_funcs[social_platform_name]
    print(f"Unregistered {social_platform_name} creation function")

def create(arguments: dict[str, Any]) -> SocialPlatform:
    """ Creates a social platform instance."""

    print(f'arguments: {arguments}')
    args_copy = arguments.copy()
    social_platform_name = args_copy.pop('name')
    
    try:
        print(f'social_platform_funcs: {social_platform_creation_funcs}, platform name: {social_platform_name}')
        creation_func = social_platform_creation_funcs[social_platform_name]
        return creation_func(**args_copy)
    except KeyError:
        raise ValueError(f"Unknown social platform name: {social_platform_name}")
