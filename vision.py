from transformers import BlipProcessor, BlipForConditionalGeneration
from PIL import Image
import re

# ================================
# LOAD MODEL
# ================================
processor = BlipProcessor.from_pretrained("Salesforce/blip-image-captioning-base")
model = BlipForConditionalGeneration.from_pretrained("Salesforce/blip-image-captioning-base")


# ================================
# STOPWORDS
# ================================
STOPWORDS = {
    "a","an","the","is","are","on","in","at","of","and","to",
    "with","for","this","that","there","here","showing","image"
}


# ================================
# EXTRACT BEST TAGS
# ================================
def extract_tags(caption, max_tags=3):

    # clean text
    words = re.findall(r'\b[a-zA-Z]+\b', caption.lower())

    # remove stopwords
    words = [w for w in words if w not in STOPWORDS]

    # count frequency
    freq = {}
    for w in words:
        freq[w] = freq.get(w, 0) + 1

    # sort by importance:
    # 1. frequency
    # 2. word length (longer = more meaningful)
    sorted_words = sorted(
        freq.items(),
        key=lambda x: (x[1], len(x[0])),
        reverse=True
    )

    # take top N tags
    tags = [word for word, _ in sorted_words[:max_tags]]

    return tags


# ================================
# MAIN FUNCTION
# ================================
def caption_image(image_path):

    image = Image.open(image_path).convert('RGB')

    inputs = processor(image, return_tensors="pt")
    output = model.generate(**inputs)

    caption = processor.decode(output[0], skip_special_tokens=True)

    tags = extract_tags(caption, max_tags=3)

    return caption, tags