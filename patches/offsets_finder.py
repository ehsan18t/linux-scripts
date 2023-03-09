#!/bin/env python3

import hashlib
import subprocess

def make_bytes_literal(hex_val):
    for item in hex_val:
        if isinstance(item, str):
            item = hex_val[item]
        item["value"] = bytes.fromhex(item["value"].replace(" ", ""))
        item["size"] = len(item["value"])
    return hex_val

def get_offset(bin_file, data):
    byte, size, off = data["value"], data["size"], data["offset"]
    i = 0
    flag = False

    with open(bin_file, "rb") as input_file:
        while True:
            b = input_file.read(1)
            if not b:
                break

            if b == int.to_bytes(byte[i]):
                i += 1
                if i == size:
                    offset = hex(input_file.tell() - size + off)
                    print(f" => {data['name']}: {offset}")
                    flag = True
                    # reset
                    i = 0
            else:
                i = 0
                
    if not flag:
        return False
    return True


def get_version():
    print("")
    return subprocess.Popen("subl -v".split(), stdout=subprocess.PIPE).communicate()[0].decode("utf-8")

def get_md5(bin_file):
    with open(bin_file, "rb") as input_file:
        file = input_file.read()
        md5 = hashlib.md5(file).hexdigest()
        print(f" => MD5 Checksum -> {md5}")
        print(f" => SHA1 Checksum -> {hashlib.sha1(file).hexdigest()}")
        # print(f" => SHA256 Checksum -> {hashlib.sha256(file).hexdigest()}")
        print("")
    input_file.close()


def common(bin_file):
    hex_val = [
        {
            "id": "1",
            "name": "Initial License Check",
            "value": "AF 31 C0 C3 55 41 57 41 56 41 55",
            "offset": 4,
            "status": "ok",
        },
        {
            "id": "2",
            "name": "Persistent License Check 1",
            "value": "BA 88 13 00 00 E8",
            "offset": 5,
            "status": "ok",
        },
        {
            "id": "3",
            "name": "Persistent License Check 2",
            "value": "BA 98 3A 00 00 E8",
            "offset": 5,
            "status": "ok",
        },
        {
            "id": "4",
            "name": "Disable Server Validation Thread",
            "value": "4D 00 48 89 C5 48 89 DF E8",
            "offset": -59,
            "status": "not ok",
        },
        {
            "id": "5",
            "name": "Disable License Notify Thread",
            "value": "83 AC 03 00",
            "offset": 3,
            "status": "not ok",
        },
        {
            "id": "6",
            "name": "Disable Crash Reporter",
            "value": "D2 C3 CC CC 55",
            "offset": 4,
            "status": "ok",
        },
    ]
    backup = {
        "1": {
                "id": "11",
                "name": "Initial License Check",
                "value": "AC 31 C0 C3 55 41 57 41 56 41 55",
                "offset": 4,
            },
    }


    # print(" => ", get_version())
    get_md5(bin_file)
    
    hex_val = make_bytes_literal(hex_val)
    backup = make_bytes_literal(backup)
    for index, item in enumerate(hex_val):
        if item["status"] != "ok" and not get_offset(bin_file, item):
            bak = backup.get(item["id"], None)
            if bak is not None:
                # print(" => Trying Alternative Pattern...")
                hex_val.insert(index + 1, backup[item["id"]])
            else:
                print(f" => {item['name']}: Not found")
                # print(" => No Alternative Pattern Found")
                # break




def main():
    print("\n\n => Dev Build 4141 ")
    bin_file = "/home/ehsan/Documents/st/dev/sublime_text"
    common(bin_file)

    print("\n\n => Dev Build 4147 ")
    bin_file = "/home/ehsan/Documents/st/dev/sublime_text.bak"
    common(bin_file)

    print("\n\n => Stable Build 4143 ")
    bin_file = "/home/ehsan/Documents/st/stable/sublime_text"
    common(bin_file)

if __name__ == "__main__":
    main()
