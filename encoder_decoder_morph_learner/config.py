import sys
import os
import shutil
if sys.version_info[0] == 2:
    import ConfigParser as configparser
else:
    import configparser

from .kwargs import ENCODER_DECODER_MORPH_LEARNER_INITIALIZATION_KWARGS



class Config(object):
    def __init__(self, path):
        config = configparser.ConfigParser()
        config.optionxform = str
        config.read(path)

        # Data
        data = config['data']
        self.unimorph_feature_file = data.get('unimorph_feature_file', './unimorph_feats.txt')
        self.train_data = data.get('train_data', './')
        self.cv_data = data.get('cv_data', './')
        self.test_data = data.get('test_data', './')
        self.order = data.getint('order', 2)
        self.save_preprocessed_data = data.getboolean('save_preprocessed_data', True)

        # SETTINGS
        # Output directory
        settings = config['settings']
        self.outdir = settings.get('outdir', None)
        if self.outdir is None:
            self.outdir = settings.get('logdir', None)
        if self.outdir is None:
            self.outdir = './dtsr_model/'
        if not os.path.exists(self.outdir):
            os.makedirs(self.outdir)
        if os.path.realpath(path) != os.path.realpath(self.outdir + '/config.ini'):
            shutil.copy2(path, self.outdir + '/config.ini')

        # Process config settings
        self.model_settings = self.build_encoder_decoder_morph_learner_settings(settings)
        self.model_settings['n_iter'] = settings.getint('n_iter', 1000)
        gpu_frac = settings.get('gpu_frac', None)
        if gpu_frac in [None, 'None']:
            gpu_frac = None
        else:
            try:
                gpu_frac = float(gpu_frac)
            except:
                raise ValueError('gpu_frac parameter invalid: %s' % gpu_frac)
        self.model_settings['gpu_frac'] = gpu_frac
        self.model_settings['use_gpu_if_available'] = settings.getboolean('use_gpu_if_available', True)

    def __getitem__(self, item):
            return self.model_settings[item]

    def build_encoder_decoder_morph_learner_settings(self, settings):
        out = {}

        # Initialization keyword arguments
        out['outdir'] = self.outdir
        for kwarg in ENCODER_DECODER_MORPH_LEARNER_INITIALIZATION_KWARGS:
            out[kwarg.key] = kwarg.kwarg_from_config(settings)

        return out


