from statistics import mean

from app.provider import generate_answer

questions = [
    "What is the return policy?",
    "How long does delivery take?",
    "What is the warranty period?",
    "How do refunds work?",
    "Can an order be cancelled?",
]

scores = []

for question in questions:
    result = generate_answer(question)
    answer = result["answer"]

    expected = f"Primary answer for: {question}"

    faithfulness = 5 if answer == expected else 1
    relevance = 5 if answer == expected else 1

    scores.append((faithfulness, relevance))

mean_faithfulness = mean(s[0] for s in scores)

assert mean_faithfulness >= 4.0
assert all(min(s) >= 2 for s in scores)

print("5-question evaluation gate: PASS")
