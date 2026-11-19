
import json
import csv
import requests
from datetime import datetime

# Configuration
OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL_NAME = "llama3.2"

INPUT_FILE = "golden_set.json"
OUTPUT_FILE = "baseline_results.csv"

RELEASE_VERSION = "v0.1"


# Function to get answer from Ollama
def get_llm_answer(question):

    prompt = f"""
Answer the following question clearly and accurately:

{question}
"""

    payload = {
        "model": MODEL_NAME,
        "prompt": prompt,
        "stream": False,
        "options": {
            "temperature": 0,
            "num_predict": 100
        }
    }

    try:
        response = requests.post(
            OLLAMA_URL,
            json=payload,
            timeout=300
        )

        response.raise_for_status()

        result = response.json()

        return result.get("response", "")

    except requests.exceptions.RequestException as e:
        print("Ollama API Error:", e)
        return ""


# Function to calculate keyword coverage
def calculate_score(answer, keywords):

    if not keywords:
        return 0, [], []

    answer_lower = answer.lower()

    matched_keywords = []
    missing_keywords = []

    for keyword in keywords:

        if keyword.lower() in answer_lower:
            matched_keywords.append(keyword)
        else:
            missing_keywords.append(keyword)

    score = (len(matched_keywords) / len(keywords)) * 100

    return score, matched_keywords, missing_keywords


# Main evaluation function
def main():

    print("\n======================================")
    print("       BASELINE RUN STARTED")
    print("======================================")

    # Load golden question set
    try:
        with open(INPUT_FILE, "r", encoding="utf-8") as file:
            golden_set = json.load(file)

    except FileNotFoundError:
        print("Error: golden_set.json file not found.")
        return

    results = []

    total_questions = len(golden_set)
    pass_count = 0
    review_count = 0
    error_count = 0
    total_score = 0

    # Process each question
    for index, item in enumerate(golden_set, start=1):

        question_id = item.get("id", item.get("question_id", f"Q{index:03d}"))
        question = item.get("question", "")
        expected_answer = item.get("expected_answer", "")
        keywords = item.get("keywords", [])
        source = item.get("source", item.get("sources", ""))

        print("\n--------------------------------------")
        print(f"Question {index}: {question_id}")
        print("Question:", question)

        # Get model answer
        answer = get_llm_answer(question)

        if not answer:
            score = 0
            matched_keywords = []
            missing_keywords = keywords
            status = "ERROR"
            error_count += 1

        else:
            score, matched_keywords, missing_keywords = calculate_score(
                answer, keywords
            )

            if score >= 60:
                status = "PASS"
                pass_count += 1
            else:
                status = "REVIEW"
                review_count += 1

        total_score += score

        print("\nLlama 3.2 Answer:")
        print(answer)

        print("\nExpected Answer:")
        print(expected_answer)

        print("\nMatched Keywords:", matched_keywords)
        print("Missing Keywords:", missing_keywords)
        print(f"Score: {score:.1f} %")
        print("Status:", status)

        results.append({
            "Question ID": question_id,
            "Question": question,
            "Expected Answer": expected_answer,
            "Model Answer": answer,
            "Matched Keywords": ", ".join(matched_keywords),
            "Missing Keywords": ", ".join(missing_keywords),
            "Score": round(score, 2),
            "Status": status,
            "Source": source,
            "Release": RELEASE_VERSION
        })

    # Save results to CSV
    fieldnames = [
        "Question ID",
        "Question",
        "Expected Answer",
        "Model Answer",
        "Matched Keywords",
        "Missing Keywords",
        "Score",
        "Status",
        "Source",
        "Release"
    ]

    with open(OUTPUT_FILE, "w", newline="", encoding="utf-8-sig") as file:

        writer = csv.DictWriter(file, fieldnames=fieldnames)

        writer.writeheader()
        writer.writerows(results)

    # Calculate average score
    average_score = (
        total_score / total_questions
        if total_questions > 0 else 0
    )

    # Display final summary
    print("\n======================================")
    print("       BASELINE EVALUATION SUMMARY")
    print("======================================")

    print("Total Questions:", total_questions)
    print("Successful Responses:", total_questions - error_count)
    print("PASS:", pass_count)
    print("REVIEW:", review_count)
    print("ERROR:", error_count)

    print(f"Average Keyword Coverage: {average_score:.2f} %")

    print("Evaluation Date:", datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

    print("Release Version:", RELEASE_VERSION)

    print("\nResults saved to:", OUTPUT_FILE)

    print("\nBASELINE EVALUATION COMPLETED")
    print("======================================")


# Program execution
if __name__ == "__main__":
    main()
