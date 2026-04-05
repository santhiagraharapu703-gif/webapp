from flask_frozen import Freezer
from app import app   # mee app.py file name correct undali

freezer = Freezer(app)

# Correct decorator
@freezer.register_generator
def all_urls():
    yield '/'  
    yield '/login'
    yield '/signup'
    yield '/environmental-dashboard'
    yield '/forest-dashboard'
    yield '/pollution-dashboard'
    yield '/alerts'   # unte add cheyyi

# Correct main
if __name__ == '__main__':
    freezer.freeze()