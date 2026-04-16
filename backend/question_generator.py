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


import random   # 👈 add this import at top if not present


def generate_mcqs(text):
    text = text[:500]

    input_text = f"generate question: {text}"

    result = generator(
        input_text,
        max_length=64,
        num_return_sequences=5,
        do_sample=True
    )

    mcqs = []

    for item in result:
        question = item["generated_text"]

        correct_answer = extract_answer(text)
        options = generate_options(correct_answer)

        mcqs.append({
            "question": question,
            "options": options,
            "answer": correct_answer
        })

    return mcqs


def extract_answer(text):
    sentences = text.split(".")
    return sentences[0] if sentences else text[:50]


def generate_options(correct):
    words = correct.split()

    options = [correct]

    while len(options) < 4:
        fake = " ".join(random.sample(words, len(words)))
        if fake not in options:
            options.append(fake)

    random.shuffle(options)
    return options