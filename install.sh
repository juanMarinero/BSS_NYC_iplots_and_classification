#!/bin/bash

## run current script
# sudo chmod +x install.sh # privileges
# ./install.sh # run


# Function to create and navigate to the repository directory
create_repo_dir() {
    local dir_repo=$1
    mkdir -v $dir_repo  && \
    echo "Repository directory created: $dir_repo"
    echo ""
}

# Function to clone the GitHub repository
clone_repository() {
    local dir_repo=$1
    local git_repo="BSS_NYC_iplots_and_classification"
    sudo apt install -y git  && \
    git clone https://github.com/juanMarinero/$git_repo  && \
    cp -r $git_repo/* $dir_repo && \
    cp -r $git_repo/.git $dir_repo && \
    rm -rf $git_repo && \
    unzip -d $dir_repo/databases/ $dir_repo/databases/pickle.zip && \
    echo "Repository cloned and moved to: $dir_repo"
    echo ""
}

# Function to install Python 3.10
install_python() {
    sudo add-apt-repository -y ppa:deadsnakes/ppa  && \
    sudo apt-get update  && \
    sudo apt-get install -y python3.10  && \
    ls -l /usr/bin/python* # shows python3.10  && \
    sudo update-alternatives --install /usr/bin/python python /usr/bin/python3 10  && \
    sudo update-alternatives --config python3  && \
    sudo mv /usr/bin/python /usr/bin/python_backup  && \
    echo "Python 3.10 installed"
    echo ""
}

# Function to install python3.10-venv
install_python_venv() {
    sudo apt install -y python3.10-venv  && \
    echo "Python 3.10 venv installed"
    echo ""
}

# Function to create a virtual environment
create_virtualenv() {
    local dir_venv=$1
    python -m venv $dir_venv  && \
    echo "Virtual environment created at: $dir_venv"
    echo ""
}

# Function to install dependencies from requirements.txt and other needed packages
install_dependencies() {
    local dir_repo=$1
    local dir_venv=$2
    source $dir_venv/bin/activate  && \
    pip install -r $dir_repo/requirements.txt  && \
    pip install lxml_html_clean lxml[html_clean]  && \
    echo "Dependencies installed from requirements.txt"
    echo ""
}

# Function to install Graphviz and Node.js
install_graphviz_node() {
    sudo apt-get install -y graphviz  && \
    echo "Graphviz installed"
    echo ""
}

# Function to install holoviews
install_holoviews() {
    local dir_repo=$1
    local dir_venv=$2
    git clone https://github.com/holoviz/holoviews.git && \
    cd holoviews || exit
    source $dir_venv/bin/activate  && \
    pip install -e .  && \
    echo "Holoviews installed"
    echo ""
}

# Function to run the Jupyter notebook
run_jupyter() {
    local dir_repo=$1
    local dir_venv=$2
    cd $dir_repo && \
    source $dir_venv/bin/activate  && \
    jupyter notebook
    echo "Jupyter notebook started in: $dir_repo"
    echo ""
}


# Main script execution
main() {

    dir_repo="/home/$USER/Downloads/TFM_repository"
    dir_venv="/home/$USER/Downloads/TFM_venv"
    
    #create_repo_dir $dir_repo && \
    #clone_repository $dir_repo && \
    #install_python && \    
    sudo ln -sf /usr/bin/python3.10 /usr/bin/python && \
    python -V && \ # shows Python 3.10  
    echo "Python 3.10 installed and set as default" && \
    install_python_venv && \
    create_virtualenv $dir_venv && \
    install_dependencies $dir_repo $dir_venv && \
    install_graphviz_node && \
    install_holoviews $dir_venv $dir_venv && \
    run_jupyter $dir_repo $dir_venv
}

# Run the main function
main
