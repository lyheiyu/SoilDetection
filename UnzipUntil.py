import zipfile

filename = "product.zip."

with open(filename, "rb") as f:
    signature = f.read(4)

if signature == b'PK\x03\x04':
    print("✅ This is a valid ZIP file (starts with PK)")
else:
    print("❌ This file is NOT a standard ZIP (invalid header)")
