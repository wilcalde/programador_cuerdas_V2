import sys
import os

# Añadir el directorio raíz al path para que pueda encontrar app.py
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import app as application

# Esto es lo que Vercel usará
app = application
