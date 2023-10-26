import ddddocr

def captcha2text(image_path):
    ocr = ddddocr.DdddOcr()

    with open(image_path, 'rb') as f:
        image_bytes = f.read()

    res = ocr.classification(image_bytes)
    return res