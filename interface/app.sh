rm -rf tracker
mkdir tracker 

python create_tracker.py
python -u app.py > app.log
