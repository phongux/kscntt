#session
import sys
sys.path.insert(0,"F:/wsgi/kscntt")
import importlib
import config.module

class Session():
    # Sample:
    module = config.module.Module()
    project = module.project
    """{
            'session.type': 'file',
            'session.cookie_expires':3000000, #True hoac 300 3000 ..v.v..v
        #	'session.data_dir': './data',
            'session.data_dir': '/tmp',
        #'session.domain' = '.domain.com',
        'session.path' : f'{project}',
            'session.auto': True
        }"""
    def session_opts(self):
        session_opts = f"""{{
            "session.type": "file",
            "session.cookie_expires":3000000,
            "session.data_dir": "/tmp",
        "session.path" : "/wsgi/kscntt",
            "session.auto": "True"
        }}"""

        return session_opts
