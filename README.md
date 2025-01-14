# Configuration Docker Compose pour l'application Rotate

Ce dépôt contient les fichiers de configuration nécessaires pour déployer l'application Rotate à l'aide de Docker Compose. Voici un guide détaillé pour configurer et exécuter l'application.

## Prérequis

Assurez-vous que les outils suivants sont installés sur votre machine :

- [Docker](https://docs.docker.com/get-docker/)
- [Docker Compose](https://docs.docker.com/compose/install/)

## Structure des dossiers

```plaintext
.
├── app.py
├── docker-compose.yml
├── nginx.conf
├── secrets
│   └── postgres_password
├── secret-example
│   └── postgres_password
├── .env
├── .env-example
```

## Configuration

### Étape 1 : Créer les secrets

1. Accédez au dossier `secret-example`.
2. Copiez le fichier `postgres_password` dans le dossier `secrets` :
   ```bash
   cp secret-example/postgres_password secrets/postgres_password
   ```
3. Assurez-vous que le dossier `secrets` et les fichiers sont correctement sécurisés avec les permissions appropriées :
   ```bash
   chmod 600 secrets/postgres_password
   ```

### Étape 2 : Configurer le fichier d'environnement

1. Accédez au répertoire racine.
2. Copiez le fichier `.env-example` vers `.env` :
   ```bash
   cp .env-example .env
   ```
3. Ouvrez le fichier `.env` et renseignez les valeurs des variables d'environnement, comme `POSTGRES_PASSWORD`.

### Étape 3 : Construire et déployer l'application

Exécutez les commandes suivantes pour configurer et démarrer l'application :

1. Construisez l'image:
   ```bash
   docker build -t rotate-app .
   ```
2. Démarrez les services :
   ```bash
   docker-compose up
   ```
3. Vérifiez que tous les services sont en cours d'exécution :
   ```bash
   docker ps
   ```


### Étape 4 : Initialiser Docker Swarm et répartir les réplicas

1. **Recherchez l'adresse IP de votre machine** :
   ```bash
   ip addr show
   ```
   Notez l'adresse IP de votre interface réseau principale (par exemple, `192.168.1.10`).

2. **Initialisez Docker Swarm** :
   ```bash
   docker swarm init --advertise-addr <votre_adresse_ip>
   ```

3. **Déployez la stack avec Docker Swarm** :
   ```bash
   docker stack deploy -c docker-stack.yml rotate_stack
   ```

6. **Testez et accédez à l'application** :
   - Accédez à votre application via http://<manager-IP>. 
   - Accédez à l'interface Portainer via http://<manager-IP>:9000

## Remarques

- Assurez-vous que les fichiers `.env` et `secrets/postgres_password` ne sont jamais ajoutés au contrôle de version.
- Pour la production, remplacez les configurations de développement par des paramètres adaptés à la production.

## Fichiers d'exemple

### `secret-example/postgres_password`
Contient un exemple pour le secret du mot de passe PostgreSQL.

### `.env-example`
Fournit un modèle pour le fichier `.env`. Exemple :

```plaintext
POSTGRES_PASSWORD=yourpassword
```

Remplacez `yourpassword` par un mot de passe sécurisé.

## Arrêt de l'application

Pour arrêter tous les conteneurs en cours d'exécution :

```bash
docker-compose down
```

## Dépannage

- **Problèmes de connexion à la base de données** :
  Vérifiez que le `POSTGRES_PASSWORD` dans le fichier `.env` correspond au secret `postgres_password`.

## Améliorations futures

- Finaliser la répartition des réplicas sur plusieurs nœuds via Docker Swarm.
