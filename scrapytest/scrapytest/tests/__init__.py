import sys
import os

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
sys.path.append(os.path.join(BASE_DIR, '../../mappingsite'))
os.environ['DJANGO_SETTINGS_MODULE'] = 'mappingsite.settings'