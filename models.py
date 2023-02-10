from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SelectField, FloatField
from wtforms.validators import DataRequired, AnyOf, URL, Optional, NumberRange

db = SQLAlchemy()

DEFAULT_IMAGE_URL = "https://tinyurl.com/demo-cupcake"

class Cupcake(db.Model):
    """Table for basic cupcake info"""

    __tablename__ = 'cupcakes'

    id = db.Column(db.Integer, primary_key = True, auto_increment = True)
    flavor = db.Column(db.Text, nullable = False)
    size = db.Column(db.Text, nullable = False)
    rating = db.Column(db.Float, nullable = False)
    image = db.Column(db.Text, nullable = False, default = DEFAULT_IMAGE_URL)

    def serialize_cupcake(self):
        return {'id':self.id,
                'flavor':self.flavor,
                'size':self.size,
                'rating':self.rating,
                'image':self.image}
    
class AddCupcakeForm(FlaskForm):
    """Form for creating a new cupcake"""

    flavor = StringField("Flavor", validators=[DataRequired()])
    size = SelectField("Size", validators = [DataRequired()], choices=[('sm','Small'),('md','Medium'),('lg','Large')])
    rating = FloatField("Rating", validators=[DataRequired()])
    image = StringField("Image", validators=[URL(), Optional()])
