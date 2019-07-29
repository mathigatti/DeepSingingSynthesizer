import chainer
import dataset
import tqdm
import queue
import numpy as np
from gla.gla_util import GLA
from nets.models import Generator
import sys

def convert(netA_path,netB_path,wave_path):
    with chainer.using_config('train', False):
        with chainer.no_backprop_mode():
            ds = dataset.WaveDataset(wave_path, -1, True)

            netA = Generator()
            netB = Generator()
            chainer.serializers.load_npz(netA_path, netA)
            chainer.serializers.load_npz(netB_path, netB)

            #que_a = queue.deque()
            que_ab = queue.deque()
            #que_aba = queue.deque()

            gla = GLA()

            print('converting...')
            for i in tqdm.tqdm(range(ds.max//dataset.dif)):
                x_a = ds.get_example(i)
                x_a = chainer.dataset.convert.concat_examples([x_a], -1)
                x_a = chainer.Variable(x_a)

                x_ab = netA(x_a)
                #x_aba = netB(x_ab)

                #que_a  .append(x_a  .data[0])
                que_ab .append(x_ab .data[0])
            print('done')

            print('phase estimating...')
            for i, que, name in zip(range(1), [que_ab], [wave_path]):
                wave   = np.concatenate([gla.inverse(c_f) for i_f in tqdm.tqdm(que)   for c_f in dataset.reverse(i_f)])
                print('done...')
                dataset.save(name, 16000, wave)
                print('wave-file saved at', name)

            print('all done')


# Usage example
# python convertor.py trained_model/generator_ab.npz trained_model/generator_ba.npz audios/a-espeak-test-short.wav
def main():
    netA_path = sys.argv[1]
    netB_path = sys.argv[2]
    wave_path = sys.argv[3]
    convert(netA_path,netB_path,wave_path)
