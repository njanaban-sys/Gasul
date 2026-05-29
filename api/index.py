import os
import sys

# Make the project root importable
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gasul_project.settings')

from gasul_project.wsgi import application
