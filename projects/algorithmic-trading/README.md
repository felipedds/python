# Create venv
virtualenv -p python3 venv

# Access venv
. venv/bin/activate

# Build image
docker build -t algorithmic-trade .

# Run container
docker run -ti algorithmic-trade