function sendMessage() {
    var message = document.getElementById('message').value;
    var userPhoto = "https://logosmarcas.net/wp-content/uploads/2020/11/Real-Madrid-Simbolo.jpg";
    console.log({ message: message, username: "Cardly", user_photo: userPhoto });
    socket.send({ message: message, username: "Cardly", photo: "{{ user.photo_profile }}" });
    document.getElementById('message').value = '';
}

function getAndDisplayMessages() {
            const messagesContainer = document.getElementById('messages-container');
            const currentScrollPosition = messagesContainer.scrollTop;

            fetch('/receive_message')
                .then(response => response.json())
                .then(data => {
                    messagesContainer.innerHTML = '';

                    // Afficher les messages de l'historique
                    messageHistory.forEach(message => {
                        const messageDiv = document.createElement('div');
                        messageDiv.textContent = message;
                        messageDiv.classList.add('message');
                        messagesContainer.appendChild(messageDiv);
                    });

                    // Afficher les nouveaux messages
                    data.messages.forEach(message => {
                        const messageDiv = document.createElement('div');
                        messageDiv.textContent = message;

                        // Ajouter la photo de profil à côté du message
                        if (message.user_photo) {
                            const userPhoto = document.createElement('img');
                            userPhoto.src = message.user_photo;
                            userPhoto.classList.add('user-photo');
                            messageDiv.appendChild(userPhoto);
                        }

                        messageDiv.classList.add('message');
                        messagesContainer.appendChild(messageDiv);

                        // Ajouter le nouveau message à l'historique des messages
                        messageHistory.push(message);
                    });

                    // Mettre à jour le local storage avec le nouvel historique
                    localStorage.setItem('messageHistory', JSON.stringify(messageHistory));

                    // Faites défiler automatiquement si le défilement automatique est activé
                    if (autoScrollEnabled) {
                        messagesContainer.scrollTop = messagesContainer.scrollHeight;
                    } else {
                        // Si l'utilisateur fait défiler vers le haut, désactivez le défilement automatique
                        autoScrollEnabled = (messagesContainer.scrollTop === (messagesContainer.scrollHeight - messagesContainer.offsetHeight));
                    }
                });
        }

        setInterval(getAndDisplayMessages, 2000); //rafraichir page  tous les deux sec 

        document.getElementById('send-button').addEventListener('click', function() {
        sendMessage();
    });

    // function sendMessage() {
    //     var message = document.getElementById('message').value;
    //     // var userPhoto = "{{ user.photo_profile }}"; // Remplacez cela par l'URL réelle de la photo de profil de l'utilisateur
    //     var userPhoto = "https://logosmarcas.net/wp-content/uploads/2020/11/Real-Madrid-Simbolo.jpg"
    //     socket.send({ message: message, username: "Cardly", user_photo: userPhoto });
    //     document.getElementById('message').value = '';
    // }
    

    // Cette fonction empêche le formulaire de se soumettre lors de l'appui sur la touche "Entrée"
    document.getElementById('message').addEventListener('keypress', function(event) {
        if (event.keyCode === 13) {
            event.preventDefault();
            sendMessage();
        }
    });

    // Définir une fonction pour envoyer l'image sélectionnée
    function sendImage() {
        var imageInput = document.getElementById('image-input');
        var image = imageInput.files[0];

        // Utilisez FileReader pour lire le contenu du fichier
        var reader = new FileReader();

        // Lorsque la lecture est terminée
        reader.onloadend = function() {
            // Récupérer les données encodées en base64
            var base64data = reader.result.split(',')[1];
            
            // Envoyer les données via Socket.io
            socket.emit('image', { image: base64data, type: image.type });
        };

        // Lire le fichier en tant que URL de données
        reader.readAsDataURL(image);
    }


    //fonction pour supprimer l'historique des messages 
    function clearMessageHistory() {
        // Effacer l'historique des messages dans le stockage de session
        sessionStorage.removeItem('messageHistory');

        // Effacer l'affichage actuel des messages dans la fenêtre de chat
        const messagesContainer = document.getElementById('messages-container');
        messagesContainer.innerHTML = '';
    }


    

        // Intégrer la fonction displayImage pour afficher les images dans le chat
        function displayImage(data) {
            var messagesContainer = document.getElementById('messages-container');
            var messageDiv = document.createElement('div');
            var messageHeader = document.createElement('div');
            var usernameElement = document.createElement('strong'); // Ajout d'un élément pour le nom d'utilisateur
            var imageElement = document.createElement('img');

            // Afficher le nom d'utilisateur au-dessus de l'image
            usernameElement.textContent = data.username;
            messageHeader.appendChild(usernameElement);

            // Configurer l'élément de l'image
            imageElement.src = "data:image/png;base64," + data.image;
            imageElement.style.maxWidth = '70%'; // Ajuster la largeur maximale de l'image pour l'affichage
            imageElement.style.maxHeight = 'auto'; // Ajuster la hauteur maximale de l'image pour l'affichage

            // Ajouter l'élément de l'image et le nom d'utilisateur au conteneur du message
            messageDiv.appendChild(messageHeader);
            messageDiv.appendChild(imageElement);

            // Appliquer la classe CSS en fonction de l'expéditeur du message
            if (data.username === current_user) {
                messageDiv.classList.add('message', 'sent');
            } else {
                messageDiv.classList.add('message', 'received');
            }

            // Ajouter le messageDiv au conteneur de messages
            messagesContainer.appendChild(messageDiv);
        }
