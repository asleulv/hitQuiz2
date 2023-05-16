# HitQuiz2 backend

## Setup and run the backend (Linux/MacOS)

```bash
cd backend
python3 -m venv . && source bin/activate
pip install -r requirements.txt
flask --app src/app.py db upgrade
flask --app src/app.py --debug run 
```
