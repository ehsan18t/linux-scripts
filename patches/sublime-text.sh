#!/bin/bash

function stable-4143() {
    md5sum -c <<<"3a8705d6c852ceaca7c4b41092db9c9c  sublime_text" || exit
    echo 003A31F2: 48 31 C0 C3          | xxd -r - sublime_text
    echo 00399387: 90 90 90 90 90       | xxd -r - sublime_text
    echo 0039939D: 90 90 90 90 90       | xxd -r - sublime_text
    echo 003A4E30: 48 31 C0 48 FF C0 C3 | xxd -r - sublime_text
    echo 003A2E82: C3                   | xxd -r - sublime_text
    echo 0038C9F0: C3                   | xxd -r - sublime_text
}

function dev-4147() {
    md5sum -c <<<"3fdb790da646c184dfb8dfd6375ff7f4  sublime_text" || exit
    echo 413CCF: 48 31 C0 C3          | xxd -r - sublime_text # 55 41 57 41
    echo 407CD9: 90 90 90 90 90       | xxd -r - sublime_text
    echo 407CF1: 90 90 90 90 90       | xxd -r - sublime_text
    echo 41594C: 48 31 C0 48 FF C0 C3 | xxd -r - sublime_text
    echo 432C88: C3                   | xxd -r - sublime_text
    echo 3F9280: C3                   | xxd -r - sublime_text
}

function doc() {
    echo ""
    echo "  Usage: $0 [BUILD_NUMBER]"
    echo "  eg: $0 4143"
    echo ""
    echo "  To know the build number, run:"
    echo "  subl -v"
    echo ""
    exit 1
}

function main() {
    # No args
    if [[ $# -eq 0 ]]; then
        doc
    fi

    # patches
    if [[ $1 == "4143" ]]; then
        stable-4143
    elif [[ $1 == "4147" ]]; then
        dev-4147
    else
        echo "Unsupported build number: $1"
    fi
}

cd /opt/sublime_text || exit
main $1
