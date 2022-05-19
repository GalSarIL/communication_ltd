from website import app

if __name__ == '__main__':
    app.run(debug=True, ssl_context=('cert.pem', 'key.pem'), port=8080)
