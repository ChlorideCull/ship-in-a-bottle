from bottle import Bottle

application = Bottle()

@application.route("/")
@application.route("/index.html")
def greetings():
    return """
            <html>
            <head>
            <title>Welcome to your Ship in a Bottle setup!</title>
            </head>
            <body>
            <h1>It most likely works!</h1>
            <p>I mean, you're seeing this and all...<br />
            Feel free to dive into the configuration file to see how everything
            is set up, it should be pretty self explainatory.</p>
            </body>
            </html>
           """
