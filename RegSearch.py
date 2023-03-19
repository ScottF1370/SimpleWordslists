import csv
import re
from serpapi import GoogleSearch

# Prompt the user for a search term
search_term = input("Enter a search term: ")

params = {
    "api_key": "SerpiAPIKeyHERE",
    "engine": "google",
    "q": search_term,
    "location": "United States",
    "google_domain": "google.com",
    "gl": "us",
    "hl": "en",
    "num": 100
}

# Query the SERP API and get the search results
search = GoogleSearch(params)
results = search.get_dict()

# Remove links and duplicate words from the search results
words = set()
for result in results["organic_results"]:
    title_words = [word for word in re.findall(r'\b\w+\b', result["title"]) if not re.match(r'^https?://', word)]
    
    if "snippet" in result:
        snippet_words = [word for word in re.findall(r'\b\w+\b', result["snippet"]) if not re.match(r'^https?://', word)]
        words.update(snippet_words)
    
    link_words = [word for word in re.findall(r'\b\w+\b', result["link"]) if not re.match(r'^https?://', word)]
    words.update(title_words)
    words.update(link_words)

# Write the words to a CSV file
with open("search_results.csv", "w", newline="", encoding="utf-8") as csvfile:
    writer = csv.writer(csvfile)
    for word in sorted(words):
        writer.writerow([word])
