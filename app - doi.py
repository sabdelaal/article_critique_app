from flask import Flask, render_template, request
import requests
import spacy

app = Flask(__name__)
nlp = spacy.load('en_core_web_sm')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/critique', methods=['POST'])
def critique():
    doi_link = request.form['doi_link']

    # Retrieve article text from CrossRef Metadata API
    article_text = get_article_text_from_doi(doi_link)

    if article_text:
        # Perform NLP analysis
        doc = nlp(article_text)

        # Placeholder logic for critique (replace with your actual implementation)
        critique_result = generate_critique(doc)

        return render_template('critique_result.html', critique_result=critique_result)
    else:
        return "Failed to retrieve article text from the provided DOI link."

def get_article_text_from_doi(doi_link):
    try:
        response = requests.get(f'https://api.crossref.org/works/{doi_link}')
        response.raise_for_status()  # Raise an HTTPError for bad responses
        data = response.json()

        # Check if the response contains the article text
        if 'message' in data and 'full-text' in data['message'] and 'content' in data['message']['full-text']:
            article_text = data['message']['full-text']['content']
            return article_text
        else:
            print("Article text not found in the API response.")
            return None

    except requests.exceptions.HTTPError as errh:
        print(f"HTTP Error: {errh}")
    except requests.exceptions.ConnectionError as errc:
        print(f"Error Connecting: {errc}")
    except requests.exceptions.Timeout as errt:
        print(f"Timeout Error: {errt}")
    except requests.exceptions.RequestException as err:
        print(f"Request Exception: {err}")

    return None

def generate_critique(doc):
    # Placeholder logic for generating critique
    # Implement your own NLP-based analysis here
    # This can include extracting information about the research question, methodology, findings, etc.
    # and providing feedback to the user
    critique_result = "Critique: This is a placeholder critique result."

    return critique_result

if __name__ == '__main__':
    app.run(debug=True)
