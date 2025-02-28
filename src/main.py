import asyncio
from viam.module.module import Module
from .models.simple_detection import SimpleDetection


if __name__ == '__main__':
    asyncio.run(Module.run_from_registry())
