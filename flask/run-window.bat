docker run -t -d -p 5000:5000 --name my-running-script --mount type=bind,source="%cd%",target=/usr/src/myapp -w /usr/src/myapp python:3  bash
docker exec -d my-running-script pip install --no-cache-dir -r requirements.txt 
docker exec -d my-running-script python3 app.py 
