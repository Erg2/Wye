from setuptools import setup

setup(
    name="Wye",
    options = {
        'build_apps': {
            'include_patterns': [
                '**/*.glb',
                '**/*.wav',
            ],
            'exclude_modules': ['_bootlocale', '_posixsubprocess', 'grp'],
            'gui_apps': {
                'WyeV0.3': 'WyeMain.py',

            },
            'log_filename': 'output.log',
            'log_append': False,
            'plugins': [
                'pandagl',
                'p3openal_audio',
            ],
            'platforms':['win_amd64']
        }
    }
)