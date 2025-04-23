@echo off
SETLOCAL

echo --- Activation de l'environnement virtuel ---
call backend\venv\Scripts\activate.bat
IF ERRORLEVEL 1 (
    echo Échec de l'activation de l'environnement virtuel. Vérifie le chemin.
    EXIT /B 1
)

cd backend

echo --- Installation des dépendances Python ---
pip install -r requirements.txt

echo --- Installation complémentaire (user-agents et dépendances) ---
pip install pyyaml ua-parser user-agents

echo --- Mise à jour du fichier requirements.txt ---
pip freeze > requirements.txt

echo --- Collecte des fichiers statiques Django ---
python manage.py collectstatic --noinput

echo --- Lancement du serveur Django ---
start cmd /k "cd backend && venv\Scripts\activate && python manage.py runserver"

cd ..
cd frontend

echo --- Installation des dépendances React ---
call npm install

echo --- Compilation du frontend React ---
call npm run build

echo --- Ouverture de l'application dans le navigateur ---
start http://127.0.0.1:8000

ENDLOCAL
