EVALUATION_DATASET = [
    {
        "question": "How many casual leave days do employees get?",
        "relevant_documents": ["leave_policy.pdf"]
    },
    {
        "question": "How do I reset my password?",
        "relevant_documents": ["password_reset.pdf"]
    },
    {
        "question": "What is the warranty period for the product?",
        "relevant_documents": ["warranty_policy.pdf"]
    },
    {
        "question": "How should a critical support ticket be escalated?",
        "relevant_documents": ["ticket_escalation.pdf"]
    },
    {
        "question": "What are the work from home rules?",
        "relevant_documents": ["work_from_home_policy.pdf"]
    },
    {
        "question": "How do I apply for leave?",
        "relevant_documents": ["leave_policy.pdf"]
    },
    {
        "question": "What are the password requirements?",
        "relevant_documents": ["password_reset.pdf"]
    },
    {
        "question": "What does the warranty cover?",
        "relevant_documents": ["warranty_policy.pdf"]
    }
]


if __name__ == "__main__":
    print(f"Evaluation questions: {len(EVALUATION_DATASET)}")

    for i, item in enumerate(EVALUATION_DATASET, 1):
        print(f"{i}. {item['question']}")
        print(f"   Expected: {item['relevant_documents']}")