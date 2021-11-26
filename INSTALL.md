# Installation du projet

Note : Cette procédure devrait fonctionner sur Linux et Mac. Il faut la tester et la compléter pour Windows.

## Dépendances

Le projet utilise `Python3` et des librairies listées dans le fichier [requirements](requirements.txt). 

Nous recommendons d'installer ces dépendances dans un environnement virtuel.

Tester l'installation de `Python3` et `virtualenv` avec ces commandes

    python3 --version
    pip3 --version
    virtualenv --version
    
Note: selon votre installation de python, vous pouvez remplacer les commandes `python3` et `pip3` par `python` et `pip`

Installer `virtualenv` si besoin avec la commande :  `pip3 install virtualenv`

## Installation 

Cloner le projet en local

    git clone https://gitlab.com/USER/PROJECT.git
    cd PROJECT

Créer un environnement virtuel et l'activer

    virtualenv venv --python=python3.7
    source venv/bin/activate

Note: pour les utilisateurs de Windows, la commande d'activation de l'environnement virtuel est
    
    venv\Scripts\activate.bat

Installer les dépendances python 

    pip3 install -r requirements.txt

Ou si vous utilisez anaconda:

    conda create -n dsp-training python=3.7
    conda activate dsp-training
    conda install ipykernel jupyter
    pip install -r requirements.txt
    python -m ipykernel install --user --name=dsp-training

Tester l'installation

    python -m pytest tests

Lancer le projet en local sans Airflow

    export PYTHONPATH="./src/:$PYTHONPATH"    
    python main.py

## Airflow

Les commandes suivantes peuvent être lancées en local sur les Mac et distributions Linux.
Si vous avez un ordinateur Windows, connectez-vous en ssh à une machine Linux sur le cloud (par exemple, une instance EC2) et suivez les instructions du script [ec2_for_airflow_setup.sh](ec2_for_airflow_setup.sh) en lançant les commandes suivantes:

    git clone https://github.com/xebia-france/dsp-training.git
    cd dsp-training
    git checkout exercice6-solution
    bash ec2_for_airflow_setup.sh

Vous pouvez alors reprendre les instructions à partir de la section "Créer la base de données"

Installation

    AIRFLOW_VERSION=2.0.2
    PYTHON_VERSION="$(python3 --version | cut -d " " -f 2 | cut -d "." -f 1-2)"
    CONSTRAINT_URL="https://raw.githubusercontent.com/apache/airflow/constraints-${AIRFLOW_VERSION}/constraints-${PYTHON_VERSION}.txt"
    pip3 install "apache-airflow[async,postgres]==${AIRFLOW_VERSION}" --constraint "${CONSTRAINT_URL}"

    cd dsp-training # If you are not already at root dir
    
    export PATH=~/.local/bin/:$PATH
    export AIRFLOW_HOME=$(pwd)/airflow

Créer la base de données

    airflow db init

Supprimer les dags d'exemple en modifiant cette ligne dans le fichier airflow.cfg 

    load_examples = False

Créer un utilisateur

    airflow users create \
    --username admin \
    --firstname Peter \
    --lastname Parker \
    --role Admin \
    --email spiderman@superhero.org

Lancer Airflow

    airflow webserver --port 5000

Lancer le scheduler

    # Dans un 2ème terminal :
    cd dsp-training
    export AIRFLOW_HOME=$(pwd)/airflow
    export PATH=~/.local/bin/:$PATH
    airflow scheduler

Documentation Airflow sur AWS: https://airflow.apache.org/docs/apache-airflow-providers-amazon/stable/connections/aws.html
