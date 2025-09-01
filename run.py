import os
print("Current working directory:", os.getcwd())

from app import create_app

app = create_app()

# ✅ Health check route
@app.route("/health")
def health():
    return {"status": "ok"}, 200

if __name__ == '__main__':
    # For external access from EC2, set host to 0.0.0.0 and define a port (e.g., 5000)
    app.run(host='0.0.0.0', port=8000)

