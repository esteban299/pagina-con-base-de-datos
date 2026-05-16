from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
# Conectando SQLite
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///diary.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Creación de la instancia de la base de datos
db = SQLAlchemy(app)

# Asignación #1. Crear una tabla de base de datos
class Card(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    subtitle = db.Column(db.String(100), nullable=False)
    text = db.Column(db.Text, nullable=False)

    # Agregamos el constructor explícito para calmar al editor de código
    def __init__(self, title, subtitle, text):
        self.title = title
        self.subtitle = subtitle
        self.text = text

    def __repr__(self):
        return f'<Card {self.id}>'

# ¡LA MAGIA AQUÍ! Esto reemplaza todos los comandos de terminal.
# Crea la base de datos automáticamente al ejecutar main.py si no existe.
with app.app_context():
    db.create_all()


# Ejecutar la página con contenido
@app.route('/')
def index():
    # Asignación #2. Mostrar los objetos de la DB
    
    # Obtenemos todas las tarjetas ordenadas por ID
    cards = Card.query.order_by(Card.id).all()
    
    return render_template('index.html', cards=cards)

# Ejecutar la página con la tarjeta individual
@app.route('/card/<int:id>')
def card(id):
    # Asignación #2. Mostrar la tarjeta correcta por su id
    # get_or_404 es más seguro que get(), evita que la app crashee si el ID no existe
    card = Card.query.get_or_404(id)
    
    return render_template('card.html', card=card)

# Ejecutar la página para crear la tarjeta
@app.route('/create')
def create():
    return render_template('create_card.html')

# Procesar el formulario de creación
@app.route('/form_create', methods=['GET','POST'])
def form_create():
    if request.method == 'POST':
        title = request.form['title']
        subtitle = request.form['subtitle']
        text = request.form['text']

        # Asignación #2. Crear una forma de almacenar datos en la DB
        nueva_tarjeta = Card(title=title, subtitle=subtitle, text=text)
        db.session.add(nueva_tarjeta)
        db.session.commit()

        return redirect('/')
    else:
        return render_template('create_card.html')

if __name__ == "__main__":
    app.run(debug=True)