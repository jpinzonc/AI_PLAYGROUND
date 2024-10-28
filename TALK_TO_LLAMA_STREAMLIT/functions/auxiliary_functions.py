import io

def byteiogenerator(file):
    with open(file, 'rb') as f:
        file_content = f.read()
    return io.BytesIO(file_content)