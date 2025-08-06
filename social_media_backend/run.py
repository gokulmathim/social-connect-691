from app import app

if __name__ == "__main__":
    # Run on all interfaces and port 3001 for proper container access
    app.run(host="0.0.0.0", port=3001)
