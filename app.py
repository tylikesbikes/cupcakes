from flask import Flask, jsonify, request, render_template
from models import db, Cupcake, DEFAULT_IMAGE_URL, AddCupcakeForm

app = Flask(__name__)

app.config['SECRET_KEY'] = 'keeta'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///cupcakes'


app.app_context().push()

db.app = app
db.init_app(app)

@app.route('/', methods=['GET'])
def show_main():
    """Show Main Page"""
    search_term = request.args.get('search_term',None)

    if search_term:
        cupcakes = Cupcake.query.filter(Cupcake.flavor.like(f'%{search_term}%')).order_by(Cupcake.id.desc()).all()
    else:
        cupcakes = Cupcake.query.order_by(Cupcake.id.desc()).all()
    return render_template('home.html', form=AddCupcakeForm(), cupcakes=cupcakes)


@app.route('/api/cupcakes', methods = ['GET'])
def show_cupcakes():
    """Return JSON info about all cupcakes"""
    cupcakes_db = Cupcake.query.all()

    cupcakes_serialized = [cc.serialize_cupcake() for cc in cupcakes_db]

    return jsonify({'cupcakes':cupcakes_serialized})

@app.route('/api/cupcakes/<int:cupcake_id>', methods=['GET'])
def show_single_cupcake(cupcake_id):
    """Return JSON info about a single cupcake"""

    cupcake = Cupcake.query.get_or_404(cupcake_id)

    cupcake_serialized = cupcake.serialize_cupcake()

    return jsonify({'cupcake':cupcake_serialized})

@app.route('/api/cupcakes', methods =['POST'])
def create_cupcake():
    """Create a new cupcake"""

    ccdata = request.form

    cupcake = Cupcake(flavor = ccdata["flavor"],
                      size = ccdata["size"],
                      rating = ccdata["rating"],
                      image = DEFAULT_IMAGE_URL if ccdata['image'] == '' else ccdata['image'])
    
    db.session.add(cupcake)
    db.session.commit()

    new_cupcake = cupcake.serialize_cupcake()

    return (jsonify(cupcake=new_cupcake),201)

@app.route('/api/cupcakes/<int:id>', methods=['PATCH'])
def patch_cupcake(id):
    """Edit part of a cupcake"""

    cupcake = Cupcake.query.get_or_404(id)

    cupcake.flavor = request.json.get('flavor',cupcake.flavor)
    cupcake.size = request.json.get('size', cupcake.size)
    cupcake.rating = request.json.get('rating', cupcake.rating)
    cupcake.image = request.json.get('image', cupcake.image)

    db.session.add(cupcake)
    db.session.commit()

    new_cupcake = Cupcake.query.get_or_404(id)

    return jsonify(cupcake = new_cupcake.serialize_cupcake())

@app.route('/api/cupcakes/<int:cupcake_id>',methods=['DELETE'])
def delete_cupcake(cupcake_id):
    """Delete a cupcake from db"""

    cupcake = Cupcake.query.get_or_404(cupcake_id)

    db.session.delete(cupcake)
    db.session.commit()

    return jsonify(message="deleted")