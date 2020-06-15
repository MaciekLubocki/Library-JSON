from flask import Flask, request, render_template, redirect, url_for
from flask import jsonify, abort, make_response
from forms import ItemForm
from models import items

app = Flask(__name__)
app.config["SECRET_KEY"] = "nasturcja"

@app.route("/", methods=["GET", "POST"])
def index():
    return redirect(url_for("items_list"))

@app.route("/items/", methods=["GET", "POST"])
def items_list():
    form = ItemForm()
    error = ""
    if request.method == "POST":
        if form.validate_on_submit():
            items.create(form.data)
            items.save_all()
        return redirect(url_for("items_list"))

    return render_template("items.html", form=form, items=items.all(), error=error)


@app.route("/items/<int:item_id>/", methods=["GET", "POST"])
def item_details(item_id):
    item = items.get(item_id - 1)
    form = ItemForm(data=item)
    if request.method == "POST":
        if request.form.get('delete'):
            items.delete(item_id - 1)
        elif form.validate_on_submit():
            items.update(item_id - 1, form.data)
        return redirect(url_for("items_list"))
    return render_template("item.html", form=form, item_id=item_id)


# API section

@app.route("/api/v1/items/", methods=["GET"])
def item_list_api_v1():
    return jsonify(items.all())

@app.route("/api/v1/items/<int:item_id>", methods=["GET"])
def get_item(item_id):
    try:
        item = items.get(item_id)
        if not item:
            abort(404)
    except:
        abort(404)
    return jsonify({"item": item})

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found', 'status_code': 404}), 404)

@app.route("/api/v1/items/", methods=["POST"])
def create_item():
    if not request.json or not 'title' in request.json:
        abort(400)
    item = {
        'media': request.json['media'],
        'title': request.json['title'],
        'author': request.json.get('author', ""),
        'year': request.json.get('year', "")
    }
    items.create(item)
    return jsonify({'item': item}), 201

@app.errorhandler(400)
def bad_request(error):
    return make_response(jsonify({'error': 'Bad request', 'status_code': 400}), 400)

@app.route("/api/v1/items/<int:item_id>", methods=['DELETE'])
def delete_item(item_id):
    result = items.delete(item_id)
    if not result:
        abort(404)
    return jsonify({'result': result})

if __name__ == "__main__":
    app.run(debug=True)

