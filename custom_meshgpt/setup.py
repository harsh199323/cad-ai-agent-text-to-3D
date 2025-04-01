from setuptools import setup, find_packages

setup(
  name = 'custom_meshgpt',
  packages = find_packages(exclude=[]),
  install_requires=[
    'accelerate>=0.25.0',
    'beartype',
    "huggingface_hub>=0.21.4",
    'classifier-free-guidance-pytorch>=0.7.1',
    'einops>=0.8.0',
    'einx[torch]>=0.3.0',
    'ema-pytorch>=0.5.1',
    'environs',
    'gateloop-transformer>=0.2.2',
    'jaxtyping',
    'local-attention>=1.9.11',
    'numpy',
    'pytorch-custom-utils>=0.0.9',
    'rotary-embedding-torch>=0.6.4',
    'sentencepiece',
    'taylor-series-linear-attention==0.1.11',
    'torch>=2.1',
    'torch_geometric',
    'tqdm',
    'vector-quantize-pytorch>=1.18.1',
    'x-transformers>=1.43.4',
    "trimesh==4.6.0",
    "torchtyping==0.1.5"
  ]
)
import os
os.system("pip install git+https://github.com/MarcusLoppe/meshgpt-pytorch.git")