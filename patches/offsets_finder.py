#!/bin/env python3

import hashlib, subprocess, os, argparse, tarfile, requests

parser = argparse.ArgumentParser()
parser.add_argument("-v", "--version", type=str)
parser.add_argument("-d", "--directory", type=str)

args = parser.parse_args()
version = args.version
directory = args.directory

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


def get_version(bin_file):
    return subprocess.Popen(f"{bin_file} -v".split(), stdout=subprocess.PIPE).communicate()[0].decode("utf-8")

def print_version(bin_file):
    vvv = " | " + get_version(bin_file).strip() + " |"

    print("")
    print("", "-" * (len(vvv) - 1))
    print(vvv)
    print("", "-" * (len(vvv) - 1))
    print("")

def get_md5(bin_file):
    with open(bin_file, "rb") as input_file:
        f = input_file.read()
        print(f" => MD5 Checksum -> {hashlib.md5(f).hexdigest()}")
        print(f" => SHA1 Checksum -> {hashlib.sha1(f).hexdigest()}")
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


    print_version(bin_file)
    get_md5(bin_file)
    
    hex_val = make_bytes_literal(hex_val)
    backup = make_bytes_literal(backup)
    for index, item in enumerate(hex_val):

        # DEBUG
        # if item["status"] != "ok":
        #     continue

        if not get_offset(bin_file, item):
            bak = backup.get(item["id"], None)
            if bak is not None:
                # print(" => Trying Alternative Pattern...")
                hex_val.insert(index + 1, backup[item["id"]])
            else:
                print(f" => {item['name']}: Not found")
                # print(" => No Alternative Pattern Found")
                # break
    print("")


def download(url, path):
    print(" => Downloading...")
    r = requests.get(url, stream = True)
    total_length = int(r.headers.get('content-length'))
    chunk_size = int(total_length/20)
    
    with open(path, "wb") as f:
        for chunk in r.iter_content(chunk_size = chunk_size):
            if chunk:
                f.write(chunk)
    print(f"  # Size: {round(total_length/1048576, 2)}MB")

def extract(path, ext):
    dest = path.replace(ext, "")

    file = tarfile.open(path)
    file.extractall(dest)
    file.close()



def delete(path):
    subprocess.Popen(f"rm -rf {path}".split())

def get_file_names(dir, ext):
    arr = os.listdir(dir)
    return [f"{dir}/{item}" for item in arr if item.endswith(ext)]

def run_find(file_url, ext):
    dir_url = file_url.replace(ext, "")
    extract(file_url, ext)
    bin_file = f"{dir_url}/sublime_text/sublime_text"
    common(bin_file)
    delete(dir_url)

def main():
    if not directory:
        if not version:
            print(" => Directory or Version is required")
            return

        base_url = f"https://download.sublimetext.com/sublime_text_build_{version}_x64.tar.xz"
        file_url = f"/tmp/sublime_text_build_{version}_x64.tar.xz"
        download(base_url, file_url)
        run_find(file_url, ".tar.xz")
        delete(file_url)
    else:
        files = get_file_names(directory, ".tar.xz")
        for file_url in files:
            run_find(file_url, ".tar.xz")


if __name__ == "__main__":
    main()
