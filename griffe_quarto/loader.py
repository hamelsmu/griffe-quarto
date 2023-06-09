# AUTOGENERATED! DO NOT EDIT! File to edit: ../nbs/00_loader.ipynb.

# %% auto 0
__all__ = []

# %% ../nbs/00_loader.ipynb 2
import os
from fastcore.all import Path, test_eq
from contextlib import contextmanager
from jinja2 import Environment, PackageLoader, select_autoescape, FileSystemLoader, ChoiceLoader

# %% ../nbs/00_loader.ipynb 3
@contextmanager
def _set_directory(path: Path):
    """Changes the directory within the context"""
    origin = Path().absolute()
    try:
        os.chdir(path)
        yield
    finally:
        os.chdir(origin)

# %% ../nbs/00_loader.ipynb 4
def _return_pth(pth:Path):
    "return the path if it exists.  If yaml file, allow suffix to be .yml or .yaml"
    pth = Path(pth)
    suffix = pth.suffix
    alt_suffix = '.yaml' if suffix == '.yml' else '.yml'
    alt_pth = pth.parent/f'{pth.stem}{alt_suffix}'
    
    if pth.exists(): 
        return pth
    elif alt_pth.exists(): 
        return alt_pth

# %% ../nbs/00_loader.ipynb 6
def _find_quarto_cfg(tpl_dir='_templates'):
    "find location of the `_quarto.yaml` file from the current directory."
    # Iterate through parent directories
    current_dir = Path(os.getcwd())
    while True:
        nm = _return_pth(current_dir/'_quarto.yml')
        if nm: 
            return nm
            
        # Move to the parent directory
        parent_dir = current_dir.parent

        # Check if the current directory is the root directory
        if parent_dir == current_dir: 
            break

        current_dir = parent_dir

# %% ../nbs/00_loader.ipynb 8
def _proj_templates():
    "Returns path to local project `_quartodoc_templates/` directory if exists."
    # TODO: allow changing the location of templates folder via a config
    cfg = _find_quarto_cfg()
    if cfg: return cfg.parent/'_quartodoc_templates/'

# %% ../nbs/00_loader.ipynb 11
def env():
    "Constructs the Jinja environment with the right template loaders depending on the user's environment."
    base_loaders = [FileSystemLoader("~/.quartodoc/templates"), PackageLoader("griffe_quarto")]
    proj_tpl = _proj_templates()
    loaders = [FileSystemLoader(proj_tpl)] + base_loaders if proj_tpl else base_loaders
    
    return Environment(
        loader=ChoiceLoader(loaders),
        autoescape=select_autoescape(),
        trim_blocks=True,
        lstrip_blocks=True)
