#!/bin/bash

function add_keys() {
    sudo rpm -v --import https://download.sublimetext.com/sublimehq-rpm-pub.gpg
}

function add_repo_stable() {
    sudo dnf config-manager --add-repo https://download.sublimetext.com/rpm/stable/x86_64/sublime-text.repo
}

function add_repo_dev() {
    sudo dnf config-manager --add-repo https://download.sublimetext.com/rpm/dev/x86_64/sublime-text.repo
}

function install () {
    sudo dnf update
    sudo dnf install sublime-text -y
}

function main() {
    add_keys

    if [[ $1 == "dev" ]]; then
        add_repo_dev
    else
        add_repo_stable
    fi

    install
}

main $1
