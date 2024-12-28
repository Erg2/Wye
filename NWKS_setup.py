from setuptools import setup

setup(
    name="Wye",
    options = {
        'build_apps': {
            #'include_patterns': [
            #    '**/*.png',
            #    '**/*.jpg',
            #    '**/*.egg',
            #],
            'exclude_modules': ['_bootlocale', '_posixsubprocess', 'grp'],
            'gui_apps': {
                'Wye V0.1': 'WyeMain.py',
            },
            'log_filename': '$USER_APPDATA/Asteroids/output.log',
            'log_append': False,
            'plugins': [
                'pandagl',
                'p3openal_audio',
            ],
            'platforms':['win_amd64']
        }
    }
)