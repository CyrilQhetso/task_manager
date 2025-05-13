from app import create_app, db
from flask import current_app

app = create_app()

# Create a context processor to make the nl2br filter available in templates
@app.template_filter('nl2br')
def nl2br(value):
    if value:
        return value.replace('\n', '<br>')
    return ''

# Create a context block to make current datetime available in templates
@app.context_processor
def inject_now():
    from datetime import datetime
    return {'now': datetime.utcnow()}

# Create all database tables before first request
@app.before_request
def create_tables():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True)