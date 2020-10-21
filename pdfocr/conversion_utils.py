import pdf2image
import pytesseract

def pdf_to_img(pdf_file, path=True):
    if path:
        return pdf2image.convert_from_path(pdf_file)
    else:
        return pdf2image.convert_from_bytes(pdf_file)

def do_ocr(file, lang):
    text = pytesseract.image_to_string(file, lang=lang)
    return text

def print_pages(pdf_file, lang, path=True):
    extracted_text=[]
    images = pdf_to_img(pdf_file, path)
    for pg, img in enumerate(images):
        extracted_text.append(f'--- PAG {pg+1} ---')
        extracted_text.append(do_ocr(img,lang))
    return '\n'.join(extracted_text)
