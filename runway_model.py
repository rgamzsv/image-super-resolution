import runway
import numpy as np
from ISR.models import RDN


@runway.setup(options={'checkpoint': runway.file(extension='.hdf5')})
def setup(opts):
    rdn = RDN(arch_params={'C':6, 'D':20, 'G':64, 'G0':64, 'x':2})
    rdn.model.load_weights(opts['checkpoint'])
    return rdn
    

@runway.command('upscale', inputs={'image': runway.image}, outputs={'upscaled': runway.image})
def upscale(rdn, inputs):
    width, height = inputs['image'].size
    if width >= 1000 or height >= 1000:
        return rdn.predict(np.array(inputs['image']), by_patch_of_size=256)
    else:
        return rdn.predict(np.array(inputs['image']))


if __name__ == '__main__':
    runway.run(port=4231)
