VALID_TAGS = [
    "Long_Duration_(>2_Hrs)",
    "Short_Duration_(<2_Hrs)",
    "Labor_Intensive",
    "Construction",
    "Moving",
    "Food_Bank"
    ]

DISPLAY_TAGS = [entry.replace('_', ' ') for entry in VALID_TAGS]

NUM_TAGS = len(VALID_TAGS)

DATABASE_PATH = "static/"
IMAGE_PATH = "images/"
USER_IMAGES = IMAGE_PATH + "users/"
EVENT_IMAGES = IMAGE_PATH + "events/"

# Check if uploaded image is of an allowed filetype
# Returns the file extension if it is, False otherwise
def allowedImageFile(filename):
    if ('.' in filename):
        extension = filename.rsplit('.', 1)[1].lower()
        if (extension in ["png", "jpg", "jpeg"]):
            return '.' + extension
        else:
            return False
    else:
        return False