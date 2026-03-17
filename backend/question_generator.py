from transformers import pipeline

# Load question generation model
generator = pipeline(
    "text2text-generation",
    model="valhalla/t5-base-qg-hl"
)

def generate_questions(text):

    # limit input text size
    text = text[:500]
    
    input_text = f"generate question: {text}"

    result = generator(input_text, max_length=64, num_return_sequences=5, do_sample=True)

    questions = []

    for item in result:
        questions.append(item["generated_text"])

    return questions
