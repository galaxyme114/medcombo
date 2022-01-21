try:
    from local import *
except ImportError as e:
    pass

try:
    from test import *
except ImportError as e:
    pass

try:
    from production import *
except ImportError as e:
    pass
