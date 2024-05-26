# Projet JO 2024 Paris

## Description
Ce projet est une plateforme de billetterie pour les Jeux Olympiques de Paris 2024. Les utilisateurs peuvent s'inscrire, se connecter, consulter les offres de tickets, ajouter des tickets à leur panier et finaliser leurs achats. Le site permet également aux utilisateurs de consulter leurs commandes passées.

## Fonctionnalités
- Inscription et connexion des utilisateurs
- Gestion de profil utilisateur
- Consultation des offres de tickets disponibles
- Ajout de tickets au panier
- Paiement et finalisation des achats
- Consultation des commandes passées
- Affichage des QR codes des tickets achetés

## Prérequis
- Python 3.8 ou plus
- Django 3.2 ou plus
- MariaDB (ou un autre SGBD compatible)

## Installation
1. Clonez le dépôt :
    ```bash
    git clone https://github.com/Bmalik73/Jo_Bloc3.git
    cd Jo_Bloc3
    ```

2. Créez un environnement virtuel et activez-le :
    ```bash
    python -m venv .env
    source .env/bin/activate  # Sur Windows, utilisez `.env\Scripts\activate`
    ```

3. Installez les dépendances :
    ```bash
    pip install -r requirements.txt
    ```

4. Configurez la base de données dans `settings.py` :
    ```python
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.mysql',
            'NAME': 'nom_de_votre_base_de_donnees',
            'USER': 'votre_utilisateur',
            'PASSWORD': 'votre_mot_de_passe',
            'HOST': 'localhost',
            'PORT': '3306',
        }
    }
    ```

5. Appliquez les migrations :
    ```bash
    python manage.py migrate
    ```

6. Créez un super utilisateur pour accéder à l'administration Django :
    ```bash
    python manage.py createsuperuser
    ```

7. Collectez les fichiers statiques :
    ```bash
    python manage.py collectstatic
    ```

8. Démarrez le serveur de développement :
    ```bash
    python manage.py runserver
    ```

9. Accédez au site à l'adresse [http://127.0.0.1:8000](http://127.0.0.1:8000).

## Déploiement
Pour déployer ce projet sur un serveur de production, suivez ces étapes supplémentaires :

1. Configurez un serveur web (par exemple, Nginx) pour servir le site.
2. Utilisez un serveur WSGI (par exemple, Gunicorn) pour exécuter l'application Django.
3. Assurez-vous que toutes les dépendances sont installées sur le serveur de production.
4. Configurez la base de données et les paramètres appropriés dans `settings.py`.
5. Collectez les fichiers statiques et appliquez les migrations comme indiqué dans les instructions d'installation.

## Utilisation
### Inscription et Connexion
Les utilisateurs peuvent s'inscrire et se connecter via les formulaires disponibles sur le site. Une fois connectés, ils peuvent accéder à leur profil et modifier leurs informations personnelles.

### Gestion du Panier
Les utilisateurs peuvent ajouter des tickets à leur panier depuis la page des offres de tickets. Le panier est accessible via la barre de navigation et affiche le nombre de tickets ajoutés. Les utilisateurs peuvent finaliser leur achat et procéder au paiement depuis la page du panier.

### Consultation des Commandes
Les utilisateurs peuvent consulter leurs commandes passées dans la section "Mes Commandes" de leur profil. Chaque commande affiche les détails des tickets achetés et permet de visualiser les QR codes associés.

## Technologies Utilisées
- Django : Framework web principal
- Tailwind CSS : Framework CSS pour le style
- JavaScript : Pour les interactions dynamiques (affichage des QR codes dans une modale)
- MariaDB : Base de données
- HTML/CSS : Structure et style des pages

## Contribuer
Les contributions sont les bienvenues ! Si vous souhaitez contribuer à ce projet, veuillez soumettre une pull request avec une description des modifications que vous proposez.

## Auteurs
- Bokarka Abdelmalik

## Licence
Ce projet est sous licence MIT. Consultez le fichier `LICENSE` pour plus d'informations.

## Lien GitHub
[https://github.com/Bmalik73/Jo_Bloc3](https://github.com/Bmalik73/Jo_Bloc3)
