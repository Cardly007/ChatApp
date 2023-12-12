                                                    # Fichier du serveur Flask 


from flask import Flask, render_template, request, redirect, url_for, jsonify, session, send_from_directory
from flask_socketio import SocketIO, send
from flask_login import current_user
from flask_wtf import FlaskForm
from time import localtime, strftime
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import InputRequired, Length, EqualTo
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from flask_basicauth import BasicAuth
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship
from flask_migrate import Migrate
import os
import base64


# Configuration de l'application Flask
app = Flask(__name__)
app.secret_key = 'Real_Madrid_better_than_PSG'  # Assurez-vous d'avoir une clé secrète unique pour votre application
app.config['SECRET_KEY'] = 'mysecret'
socketio = SocketIO(app, cors_allowed_origins="*")  # Ajoutez cors_allowed_origins si nécessaire

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # Limitez la taille maximale du fichier (ici, 16 Mo)
app.config['UPLOAD_FOLDER'] = '/Users/cardly/Downloads/PROJET/upload'  #remplacez le par l'emplacement de votre fichier upload
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(BASE_DIR, 'clients.db')

db = SQLAlchemy(app)
migrate = Migrate(app, db) # initialisation d'une instance de migration pour l'application Flask

'''
creation de la BD
flask db init  # Initialisez les migrations
flask db migrate -m "Initial migration."  # Créez une migration
flask db upgrade  # Appliquez la migration pour créer la base de données

'''


# mise en place d'une authentification administrateur pour pourvoir acceder au donne des clients 
# Configuration de Flask-BasicAuth
app.config['BASIC_AUTH_USERNAME'] = 'admin'
app.config['BASIC_AUTH_PASSWORD'] = 'IMPOSSIBLE_IS_NOTHING'
basic_auth = BasicAuth(app)




# Configuration de Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)

# Classe User pour Flask-Login
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    password = db.Column(db.String(80), nullable=False)

#exemple de modele de table 
class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    author_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)



# GESTION DE L'AUTHETIFICATION 


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


# Définition du formulaire de connexion
class LoginForm(FlaskForm):
    username = StringField('Nom d\'utilisateur', validators=[InputRequired(), Length(min=4, max=20)])
    password = PasswordField('Mot de passe', validators=[InputRequired(), Length(min=8, max=80,)])
    submit = SubmitField('Se connecter')

# Définition du formulaire d'inscription
class RegistrationForm(FlaskForm):
    username = StringField('Nom d\'utilisateur', validators=[InputRequired(), Length(min=4, max=20)])
    password = PasswordField('Mot de passe', validators=[InputRequired(), Length(min=8, max=80)])
    confirm = PasswordField('Confirmer le mot de passe',validators=[InputRequired(), Length(min=8, max=80),EqualTo('password', message='Les mots de passe doivent correspondre')])
    submit = SubmitField('S\'inscrire')


# Route pour la page d'acceuil
@app.route('/')
def home():
    message = request.args.get('message') # Récupérer le message de la requête s'il y en a 
    if message:
        return render_template('h2.html', message=message)
    return render_template('h2.html')



# Route pour la page de connexion
@app.route('/login', methods=['GET', 'POST'])
def login():
    login_form = LoginForm()

    if login_form.validate_on_submit():
        username = login_form.username.data
        password = login_form.password.data

        user = User.query.filter_by(username=username).first()

        if user and check_password_hash(user.password, password):
            login_user(user)
            return redirect(url_for('index'))
        else:
            error_message = 'Identifiant ou mot de passe incorrect'
            return render_template('l2.html', form=login_form, error_message=error_message)
    return render_template('l2.html', form=login_form)

# Route où l'on est redirigé apres la connexion 
@app.route('/index')
@login_required
def index():
    return render_template('img.html', username = current_user.username)


# Route pour la déconnexion de l'utilisateur
@app.route('/logout')
@login_required #  protégée par le décorateur @login_required, ce qui signifie que seuls les utilisateurs connectés pourront accéder à cette page. 
def logout():
    logout_user()
    return redirect(url_for('home'))

# Route pour l'inscription de l'utilisateur    
@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = generate_password_hash(form.password.data, method='pbkdf2:sha256')
        new_user = User(username=form.username.data, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('home', message='Nouvel utilisateur créé ! Connectez vous mmaintenant'))  # Redirection vers la page d'accueil avec un message
    return render_template('r2.html', form=form)

# Route pour supprimer un client de la base de donnee 
@app.route('/delete_client/<int:user_id>', methods=['POST'])
def delete_client(user_id):
    user = User.query.get(user_id)
    if user:
        db.session.delete(user)
        db.session.commit()
    return redirect(url_for('clients'))




# Route pour la page clients securise avec un systeme d'authetification admin 
@app.route('/clients')
@basic_auth.required #  protégée par le décorateur @basic_auth.required, ce qui signifie que seuls les administrateurs  pourront accéder à cette page. 
def clients():
    username = request.authorization.username
    password = request.authorization.password

    if not check_credentials(username, password):
        return render_template('unauthorized.html'), 401

    all_users = User.query.all()
    return render_template('dataClient.html', users=all_users)


def check_credentials(username, password):
    if username == app.config['BASIC_AUTH_USERNAME'] and password == app.config['BASIC_AUTH_PASSWORD']:
        return True
    else:
        return False


#@basic_auth.error_handler  en cas de donne admin incorrect redirection vers une page d'erreur 
def unauthorized():
    return render_template('unauthorized.html'), 401






# GESTION DES MESSAGES 



# Dans la route send_message
@app.route('/send_message', methods=['POST'])
@login_required #  protégée par le décorateur @login_required, ce qui signifie que seuls les utilisateurs connectés pourront accéder à cette page. 
def send_message():
    if request.method == 'POST':
        message = request.json['message']

        username = current_user.username 
        full_message = f"{username}: {message}"  # Associe le message au nom de l'utilisateur
        #client_socket.sendall(full_message.encode())
        socketio.emit('message', {'message': msg['message'], 'username': msg['username'], 'time_stamp': strftime('%I:%M%p', localtime())}, broadcast=True)

        return jsonify({'status': 'success'})

# Dans la fonction pour la gestion des message  
@socketio.on('message')
def handle_message(msg):
    print('Message:', str(msg))
    send({'message': msg['message'], 'username': msg['username'], 'time_stamp': strftime('%I:%M%p', localtime())}, broadcast=True)




@socketio.on('image')
def handle_image(image_data):

    image = image_data['image']  # Récupérez les données de l'image à partir de image_data
    username = current_user.username
    print(f'{username} a envoyé une image.')

     # Assurez-vous que le répertoire d'upload existe
    if not os.path.exists(app.config['UPLOAD_FOLDER']):
        os.makedirs(app.config['UPLOAD_FOLDER'])

    # Par exemple, vous pouvez enregistrer l'image dans un répertoire spécifique avec un nom de fichier unique
    image_filename = f"{username}_{strftime('%Y%m%d%H%M%S', localtime())}.png"
    image_path = os.path.join(app.config['UPLOAD_FOLDER'], image_filename)

    with open(image_path, "wb") as image_file:
        image_file.write(base64.b64decode(image))


    image_url = url_for('uploaded_file', filename=image_filename)
    socketio.emit('image', {'image_url': image_url, 'username': username, 'time_stamp': strftime('%I:%M%p', localtime())})


@app.route('/uploads/<filename>')
@login_required
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)


# Gérer le téléchargement du fichier
@app.route('/upload_image', methods=['POST'])
@login_required
def upload_image():
    if 'image' not in request.files:
        return jsonify({'error': 'No image part'})

    image = request.files['image']

    if image.filename == '':
        return jsonify({'error': 'No selected image'})

    if image and allowed_image(image.filename):
        filename = secure_filename(image.filename)
        image.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        image_url = url_for('uploaded_file', filename=filename)
        return jsonify({'message': 'Image uploaded successfully', 'image_url': image_url})
    else:
        return jsonify({'error': 'Image type not allowed'})


# Route pour servir les images téléchargées
@app.route('/images/<filename>')
@login_required
def uploaded_image(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

# Vérifiez si l'extension du fichier est autorisée
def allowed_image(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_IMAGE_EXTENSIONS

           
if __name__ == '__main__':
    socketio.run(app, debug=True)



