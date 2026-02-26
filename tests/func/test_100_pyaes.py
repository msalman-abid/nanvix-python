"""Test: pyaes"""
import sys
sys.stdout.reconfigure(line_buffering=True)
try:
    import pyaes
    key = b"This_key_for_demo_purposes_only!"
    plaintext = b"nanvix"
    aes = pyaes.AESModeOfOperationCTR(key)
    ciphertext = aes.encrypt(plaintext)
    aes = pyaes.AESModeOfOperationCTR(key)
    decrypted = aes.decrypt(ciphertext)
    assert decrypted == plaintext
    print("pyaes: PASS")
except Exception as e:
    print(f"pyaes: FAIL: {e}")
    sys.exit(1)
