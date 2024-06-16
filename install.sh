#!/bin/bash

## run current script
# sudo chmod +x install.sh # privileges
# ./install.sh # run


# Function to create and navigate to the repository directory
create_repo_dir() {
    local dir_repo=$1
    mkdir -v $dir_repo
    echo "Repository directory created: $dir_repo"
}

# Function to clone the GitHub repository
clone_repository() {
    local dir_repo=$1
    git clone https://github.com/juanMarinero/BSS_NYC_iplots_and_classification
    mv BSS_NYC_iplots_and_classification $dir_repo
    echo "Repository cloned and moved to: $dir_repo"
}

# Function to install Python 3.10
install_python() {
    sudo add-apt-repository -y ppa:deadsnakes/ppa
    sudo apt-get update
    sudo apt-get install -y python3.10
    ls -l /usr/bin/python* # shows python3.10
    sudo update-alternatives --install /usr/bin/python python /usr/bin/python3 10
    sudo update-alternatives --config python3
    sudo mv /usr/bin/python /usr/bin/python_backup
    sudo ln -sf /usr/bin/python3.10 /usr/bin/python
    python -V # shows Python 3.10
    echo "Python 3.10 installed and set as default"
}

# Function to install python3.10-venv
install_python_venv() {
    sudo apt install -y python3.10-venv
    echo "Python 3.10 venv installed"
}

# Function to create a virtual environment
create_virtualenv() {
    local dir_venv=$1
    python -m venv $dir_venv
    source $dir_venv/bin/activate
    python -V # Python 3.10
    echo "Virtual environment created and activated at: $dir_venv"
}

# Function to install dependencies from requirements.txt and other needed packages
install_dependencies() {
    local dir_repo=$1
    pip install -r $dir_repo/requirements.txt
    pip install lxml_html_clean lxml[html_clean]
    echo "Dependencies installed from requirements.txt"
}

# Function to install Graphviz and Node.js
install_graphviz_node() {
    sudo apt-get install -y graphviz
    # sudo apt install -y nodejs npm # TODO !!!! either uncomment or delete and rename fcn here and in main !!!
    # sudo ln -s /usr/bin/nodejs /usr/bin/node
    echo "Graphviz and Node.js installed" # TODO change this too if removed !!!
}

# Function to install holoviews
install_holoviews() {
    git clone https://github.com/holoviz/holoviews.git
    cd holoviews || exit
    pip install -e .
    echo "Holoviews installed"
}

# Function to run the Jupyter notebook
run_jupyter() {
    local dir_repo=$1
    cd $dir_repo || exit
    jupyter notebook
    echo "Jupyter notebook started in: $dir_repo"
}


# Main script execution
main() {

    dir_repo="/home/$USER/Downloads/TFM_repository"
    dir_venv="/home/$USER/Downloads/TFM_venv"
    
    create_repo_dir $dir_repo && \
    clone_repository $dir_repo && \
    install_python && \
    install_python_venv && \
    create_virtualenv $dir_venv && \
    install_dependencies $dir_repo && \
    install_graphviz_node && \
    install_holoviews && \
    run_jupyter $dir_repo
}

# Run the main function
main
