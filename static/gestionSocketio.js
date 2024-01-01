// javascript 
        var socket = io.connect('http://' + document.domain + ':' + location.port);
        //var socket = io.connect('http://172.17.31.88:5001');
       // var socket = io.connect('http://172.17.31.88:5001');

        socket.on('message', function(data) {
            var messagesContainer = document.getElementById('messages-container');
            var messageDiv = document.createElement('div');
            var messageContent = document.createElement('div');
            var messageHeader = document.createElement('div');
            var messageTime = document.createElement('div');

            messageHeader.classList.add('message-header');
            messageContent.classList.add('message-content');
            messageTime.classList.add('message-time');
            
                // Si ce n'est pas un fichier, affichez le message texte avec le formatage souhaité
                // Afficher le nom d'utilisateur en gras
                var usernameElement = document.createElement('strong');
                usernameElement.textContent = data.username;
                messageHeader.appendChild(usernameElement);

                // Afficher le message
                messageContent.textContent = data.message;
                messageHeader.appendChild(messageContent);

                // Afficher l'heure en bas de la div avec une petite police
                messageTime.textContent = data.time_stamp;
                messageHeader.appendChild(messageTime);

                messageDiv.appendChild(messageHeader);

                // Appliquer la classe CSS en fonction de l'expéditeur du message
                if (data.username === current_user) {
                    messageDiv.classList.add('message', 'sent');
                } else {
                    messageDiv.classList.add('message', 'received');
                }

                messagesContainer.appendChild(messageDiv);

                // Ajouter le nouveau message à l'historique des messages
                const messageHistory = JSON.parse(sessionStorage.getItem('messageHistory')) || [];
                messageHistory.push(data);
                
                // Mettre à jour le local storage avec le nouvel historique
                sessionStorage.setItem('messageHistory', JSON.stringify(messageHistory));
            
        });


    
        socket.on('image', function(data) {
            displayImage(data); // Appeler la fonction displayImage avec les données reçues du serveur
        });

        //var socket = io();

        function sendMessage() {
            var message = document.getElementById('message').value;
            socket.send({ message: message, username: current_user }); // Envoyer le nom d'utilisateur avec le message
            document.getElementById('message').value = ''; // Vider le champ de saisie après l'envoi du message
        }


            // Définir une fonction pour envoyer le fichier sélectionné
        // Ajoutez la fonction displayMessage pour afficher les fichiers multimédias dans le chat
        function displayMessage(data) {
            var messagesContainer = document.getElementById('messages-container');
            var messageDiv = document.createElement('div');
            var messageHeader = document.createElement('div');
            var messageContent = document.createElement('div');
            var messageTime = document.createElement('div');

            messageHeader.classList.add('message-header');
            messageContent.classList.add('message-content');
            messageTime.classList.add('message-time');

            // Afficher le nom d'utilisateur et le contenu du message
            messageHeader.querySelector('.username').textContent = data.username;
            messageContent.textContent = data.message;

            // Appliquer la classe CSS en fonction de l'expéditeur du message
            if (data.username === current_user) {
                messageDiv.classList.add('message', 'sent');
            } else {
                messageDiv.classList.add('message', 'received');
            }

            // Ajouter le message à l'élément messageDiv
            messageDiv.appendChild(messageHeader);
            messageDiv.appendChild(messageContent);
            messagesContainer.appendChild(messageDiv);
        }

        

        // Intégrer la fonction displayImage pour afficher les images dans le chat
        function displayImage(data) {
            var messagesContainer = document.getElementById('messages-container');
            var messageDiv = document.createElement('div');
            var messageHeader = document.createElement('div');
            //var usernameElement = document.createElement('span'); // Changer en span pour rester en ligne
            var usernameElement = document.createElement('strong'); 
            var imageElement = document.createElement('img');
            var timeElement = document.createElement('span'); // Ajouter un élément pour l'heure

            // Ajouter la classe pour le style de l'image
            messageDiv.classList.add('image-message');


            // Afficher le nom d'utilisateur au-dessus de l'image
            usernameElement.textContent = data.username;
            messageHeader.appendChild(usernameElement);

            // Configurer l'élément de l'image
            imageElement.src =  data.image_url;
            imageElement.style.maxWidth = '100%'; // Ajuster la largeur maximale de l'image pour l'affichage
            imageElement.style.maxHeight = 'auto'; // Ajuster la hauteur maximale de l'image pour l'affichage
            

            // probleme de siposition echange pour l'instant
            if (data.username === current_user) {
                messageDiv.classList.add('image-message', 'received');
            } else {
                messageDiv.classList.add('image-message', 'sent');
            }
            

            // Ajouter l'élément de l'image et le nom d'utilisateur au conteneur du message
            messageDiv.appendChild(messageHeader);
            messageDiv.appendChild(imageElement);

            // Ajouter l'heure au bas du message
            timeElement.classList.add('message-time'); 
            timeElement.textContent = data.time_stamp;
            messageDiv.appendChild(timeElement);

            // Ajouter le messageDiv au conteneur de messages
            messagesContainer.appendChild(messageDiv);
        }
    
