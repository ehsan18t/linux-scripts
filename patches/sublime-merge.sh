#!/bin/bash

function stable-2083() {
    md5sum -c <<<"c48eeacb57d71995d24a917b492fbb0d sublime_merge" || exit
    echo 000EFF60: 2F00 0000 0000 0000 0000 0000 0000 0000  | xxd -r - sublime_merge
    echo 000EFF70: 0000 0000 0000 4541 3745 0050 7572 6368  | xxd -r - sublime_merge
    echo 000FB2E0: 6500 2D00 7477 0072 2B62 0054 6875 0000  | xxd -r - sublime_merge
    echo 000FB2F0: 0000 0000 0000 0000 0000 0000 0000 206D  | xxd -r - sublime_merge
    echo 00102DB0: 0000 0000 0000 0000 0000 0000 0000 0000  | xxd -r - sublime_merge
    echo 00102DC0: 0000 0000 0000 7072 6576 696F 7573 5F63  | xxd -r - sublime_merge
    echo 001075A0: 6E64 6F77 003D 3D3D 206E 3633 3333 3337  | xxd -r - sublime_merge
    echo 001075B0: 3320 3D3D 3D00 0000 0000 002E 6D69 7373  | xxd -r - sublime_merge
    echo 0045A360: B819 0100 00C3 5541 5453 4881 EC88 2400  | xxd -r - sublime_merge
    echo 0045D210: 0048 8D3D D00F 0000 BA88 1300 0090 9090  | xxd -r - sublime_merge
    echo 0045D220: 9090 4889 5C24 0848 8BB3 1003 0000 488D  | xxd -r - sublime_merge
    echo 0045D230: 3D10 1200 00BA 983A 0000 9090 9090 9048  | xxd -r - sublime_merge
    echo 0047AF90: 3A00 0090 9090 9090 4C89 E748 89DE E8AB  | xxd -r - sublime_merge
}

function doc() {
    echo ""
    echo "  Usage: $0 [BUILD_NUMBER]"
    echo "  eg: $0 2083"
    echo ""
    echo "  To know the build number, run:"
    echo "  smerge -v"
    echo ""
    exit 1
}

function main() {
    # No args
    if [[ $# -eq 0 ]]; then
        doc
    fi

    # patches
    if [[ $1 == "2083" ]]; then
        stable-2083
    else
        echo "Unsupported build number: $1"
    fi
}

cd /opt/sublime_merge || exit
main $1
