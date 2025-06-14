#!/bin/bash

# Check if conda is installed
if ! command -v conda &> /dev/null; then
    echo "Conda is not installed. Please install Miniconda or Anaconda first."
    exit 1
fi

# Check if environment already exists
if conda env list | grep -q "medlensai"; then
    echo "Environment 'medlensai' already exists. Removing it..."
    conda env remove -n medlensai
fi

# Create conda environment
echo "Creating conda environment..."
conda env create -f environment.yml

# Check if environment creation was successful
if [ $? -ne 0 ]; then
    echo "Failed to create conda environment. Please check the error messages above."
    exit 1
fi

# Activate environment
echo "Activating environment..."
source $(conda info --base)/etc/profile.d/conda.sh
conda activate medlensai

# Check if activation was successful
if [ $? -ne 0 ]; then
    echo "Failed to activate conda environment. Please check the error messages above."
    exit 1
fi

# Create necessary directories
echo "Creating project directories..."
mkdir -p data/uploads data/models
touch data/uploads/.gitkeep data/models/.gitkeep

# Create .env file if it doesn't exist
if [ ! -f .env ]; then
    echo "Creating .env file..."
    cat > .env << EOL
# Database settings
DATABASE_URL=postgresql://localhost/medlensai

# API settings
API_HOST=0.0.0.0
API_PORT=8000
DEBUG=false

# Security
SECRET_KEY=your-secret-key-here

# Model settings
USE_GPU=false
DEVICE=mps

# External API keys
OPENFDA_API_KEY=your-openfda-api-key
WHO_ICD_API_KEY=your-who-icd-api-key
UMLS_API_KEY=your-umls-api-key

# Model parameters
MAX_LENGTH=512
TEMPERATURE=0.7
TOP_P=0.9
NUM_RETURN_SEQUENCES=1
EOL
    echo "Created .env file. Please update it with your API keys and configuration."
fi

# Install additional dependencies for Apple Silicon
echo "Installing additional dependencies for Apple Silicon..."
pip install torch torchvision torchaudio

echo "Setup complete! To activate the environment, run:"
echo "conda activate medlensai" 