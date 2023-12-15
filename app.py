from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import spacy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app)
nlp = spacy.load('en_core_web_sm')

class Article(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

@app.route('/')
def index():
    try:
        # Try to reflect the table, if it exists
        db.Model.metadata.reflect(db.engine)
    except Exception as e:
        # Create the table if it doesn't exist
        db.create_all()

    articles = Article.query.all()
    return render_template('index.html', articles=articles)

@app.route('/critique', methods=['POST'])
def critique():
    article_text = request.form['article_text']

    # Save the submitted article to the database
    new_article = Article(content=article_text)
    db.session.add(new_article)
    db.session.commit()

    # Perform NLP analysis
    doc = nlp(article_text)

    # Extract information related to the research question
    research_question_description = extract_research_question_description(doc)

    # Extract information about how researchers attempted to answer the questions
    methodology_description = extract_methodology_description(doc)

    # Extract information about the research findings
    research_findings = extract_research_findings(doc)

    # Generate critique result
    critique_result = {
        'Research Question Description': research_question_description,
        'Methodology Description': methodology_description,
        'Research Findings': research_findings
    }

    return render_template('critique_result.html', critique_result=critique_result)

@app.route('/result/<int:article_id>')
def result(article_id):
    article = Article.query.get_or_404(article_id)
    critique_result = {
        'Research Question Description': '',  # Extract this information from the article
        'Methodology Description': '',  # Extract this information from the article
        'Research Findings': ''  # Extract this information from the article
    }
    return render_template('critique_result.html', article=article, critique_result=critique_result)

def extract_research_question_description(doc):
    relevant_keywords = ["research question", "objective", "problem", "background"]
    relevant_sentences = [sent.text for sent in doc.sents if any(keyword in sent.text.lower() for keyword in relevant_keywords)]
    return " ".join(relevant_sentences)

def extract_methodology_description(doc):
    methodology_keywords = ["methodology", "approach", "method", "procedure"]
    methodology_sentences = [sent.text for sent in doc.sents if any(keyword in sent.text.lower() for keyword in methodology_keywords)]
    return " ".join(methodology_sentences)

def extract_research_findings(doc):
    findings_keywords = ["findings", "results", "conclusion"]
    findings_sentences = [sent.text for sent in doc.sents if any(keyword in sent.text.lower() for keyword in findings_keywords)]
    return " ".join(findings_sentences)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)