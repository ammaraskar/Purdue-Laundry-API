from api_server import app

app.run(debug=app.config.get('DEBUG'),
        port=app.config.get('PORT'),
        host=app.config.get('HOST'))
