from flask import Flask, request

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def greet():
    """
    Accepts:
      - GET /?name=YourName
      - POST /  with JSON {"name":"YourName"} OR form data name=YourName
    Falls back to "stranger" if no name provided.
    """
    name = None

    # GET: query parameter
    if request.method == 'GET':
        name = request.args.get('name')

    # POST: try JSON, then form, then raw body
    else:  # POST
        if request.is_json:
            data = request.get_json(silent=True) or {}
            name = data.get('name')
        else:
            name = request.form.get('name') or request.values.get('name')
            if not name:
                # try raw body (plain text)
                raw = request.data.decode().strip()
                if raw:
                    name = raw

    if not name:
        name = "stranger"

    # Return plain text greeting
    return f"Hello {name}"

if __name__ == '__main__':
    # host 0.0.0.0 so Docker & other hosts can reach it
    app.run(host='0.0.0.0', port=9097)
