FLASK_APP="app:create_app('config')" FLASK_DEBUG=true flask db migrate -m "remove uniqueness"
