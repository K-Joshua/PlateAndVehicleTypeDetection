import re
from paddleocr import PaddleOCR
from ..Helper import plate_detection_helper as gen_plate_num, delete_picture_helper as del_picture

PLATE_PATTERNS = [
    r"^[A-Z]{3}[0-9]{4}$",  # ABC1234
    r"^[0-9]{3}[A-Z]{3}$",  # 123ABC
    r"^[A-Z][0-9]{3}[A-Z]{2}$",  # A123BC
    r"^[A-Z]{2}[0-9]{5}$",  # AB12345
    r"^[A-Z]{3}",
    r"^[0-9]{3}",
]


def is_valid_plate(text):

    text = text.upper().replace(" ", "").strip()

    return any(
        re.fullmatch(pattern, text)
        for pattern in PLATE_PATTERNS
    )


ocr = PaddleOCR(
    use_textline_orientation=True,
    lang="en",
    enable_mkldnn=False
)

print("get path file")
get_path_file = gen_plate_num.generate_plate_jpeg_after_detection.crop_platenumber_N_save_crop_picture_to_assets()
print("done get path file")

print("get result")
print(get_path_file)
results = ocr.predict(str(get_path_file))

for result in results:

    data = result.json["res"]

    for text, confidence in zip(
        data["rec_texts"],
        data["rec_scores"]
    ):

        extracted_text = text.upper().replace(" ", "").strip()
        # if len(extracted_text) == 7 and extracted_text[3] in "1l|IL":
        #     extracted_text.pop([3])

        if is_valid_plate(extracted_text):

            print("Valid Plate:", extracted_text)
            print(f"Confidence: {confidence:.2%}")

        else:

            print("Ignored:", text)
            print(f"Confidence: {confidence:.2%}")

print("delete picture")
del_picture.picture_helper.delete_jpeg_picture(get_path_file)