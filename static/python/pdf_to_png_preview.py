import fitz

zoom_x = 2.0
zoom_y = 2.0
mat = fitz.Matrix(zoom_x, zoom_y)


def preview_pdf(filename, output_name):
    try:
        doc = fitz.open(filename)
        for page in doc:
            pix = page.get_pixmap(matrix=mat)
            pix.save(f"../img/products/preview/{output_name}_preview.png")

    except Exception as ex:
        print(ex)