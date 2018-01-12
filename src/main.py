from flask import Flask, render_template, request

app = Flask(__name__)
app.config.from_object('dev_config')


@app.route('/', methods=['GET'])
def form():
    return render_template('index.html')

@app.route('/', methods=['POST'])
def receive():
    print(request.form)
    print(len(request.files))
    print(request.files)
    return "Success", 200

if __name__ == '__main__':
    app.run()
