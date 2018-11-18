import os
import subprocess

def encrypt_db(password):
    db = "pwmanager.sqlite3"
    encrypted_db = f"{db}.gpg"
    command = f" echo '{password}' | /usr/bin/gpg -c -o {encrypted_db} --batch --quiet --no-tty --cipher-algo AES256 --passphrase-fd 0 {db}"
    exec_cmd = subprocess.Popen(command, shell=True, preexec_fn=os.setsid, stdout=subprocess.PIPE)
    exec_cmd.wait()

    try:
        os.killpg(os.getpgid(exec_cmd.pid), signal.SIGTERM)

    except ProcessLookupError:
        pass

    os.remove(db)


def decrypt_db(password):
    db = "pwmanager.sqlite3"
    encrypted_db = f"{db}.gpg"
    command = f" echo '{password}' | /usr/bin/gpg --batch --yes --quiet --no-tty --passphrase-fd 0 {encrypted_db}"

    exec_cmd = subprocess.Popen(command, shell=True, preexec_fn=os.setsid, stdout=subprocess.PIPE)
    exec_cmd.wait()

    try:
        os.killpg(os.getpgid(exec_cmd.pid), signal.SIGTERM)

    except ProcessLookupError:
        pass

    if not os.path.isfile('pwmanager.sqlite3'):
        print("\n[ERROR] Incorrect Passphrase.\n")
        exit(1)

    os.remove(encrypted_db)