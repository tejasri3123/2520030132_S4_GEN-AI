
from transformers import AutoTokenizer
import pandas as pd

# Load tokenizers
tokenizers = {
    "BPE": AutoTokenizer.from_pretrained("openai-community/gpt2"),
    "WordPiece": AutoTokenizer.from_pretrained(
        "google-bert/bert-base-multilingual-cased"
    ),
    "SentencePiece": AutoTokenizer.from_pretrained("google/mt5-small")
}

# Test sentences in three languages
sentences = {
    "English": "Artificial Intelligence is transforming education and healthcare.",
    "Telugu": "కృత్రిమ మేధస్సు విద్య మరియు వైద్య రంగాలను మారుస్తోంది.",
    "Hindi": "कृत्रिम बुद्धिमत्ता शिक्षा और स्वास्थ्य सेवा को बदल रही है।"
}

results = []

# Compare tokenizers
for language, sentence in sentences.items():
    word_count = len(sentence.split())

    for tokenizer_name, tokenizer in tokenizers.items():
        tokens = tokenizer.tokenize(sentence)
        token_count = len(tokens)

        results.append({
            "Language": language,
            "Tokenizer": tokenizer_name,
            "Sentence": sentence,
            "Tokens": tokens,
            "Token Count": token_count,
            "Word Count": word_count,
            "Token-to-Word Ratio": round(token_count / word_count, 2)
        })

# Display results
df = pd.DataFrame(results)

print("\n========== TOKENIZER COMPARISON ==========\n")
print(df[[
    "Language",
    "Tokenizer",
    "Token Count",
    "Word Count",
    "Token-to-Word Ratio"
]].to_string(index=False))

# Save results to CSV
df.to_csv("tokenizer_results.csv", index=False, encoding="utf-8-sig")

print("\nResults saved successfully to tokenizer_results.csv")
