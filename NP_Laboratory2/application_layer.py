from cryptography.fernet import Fernet

import error_correction


def get_symmetric_key():
    return Fernet.generate_key()


def show_server_result(data, symmetric_encryption):
    humming_decoded_message = error_correction.decode(data.decode())
    message_decrypt = symmetric_encryption.decrypt(humming_decoded_message.encode()).decode('utf-8')
    print(message_decrypt)
