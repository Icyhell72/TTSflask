import PyPDF2
from fuzzywuzzy import fuzz
from nltk import word_tokenize
from nltk.corpus import stopwords

textCv = ""


def read_pdf(file_path):
    with open(file_path, "rb") as pdf_file:
        pdf_reader = PyPDF2.PdfReader(pdf_file)
        cv_text = ""
        for page_num in range(len(pdf_reader.pages)):
            page = pdf_reader.pages[page_num]
            cv_text += page.extract_text()
    return cv_text


# Function for text preprocessing
def preprocess_text(text):
    text = text.lower()
    words = word_tokenize(text)
    stop_words = set(stopwords.words("english"))
    words = [word for word in words if word.isalpha() and word not in stop_words]
    global textCv
    textCv = "".join(words)
    return " ".join(words)


# Function to generate recommendations
def generate_recommendations():
    programming_languages = ["Python", "Java", "JavaScript", "C++", "C", "C#", "Go", "Rust"]
    frameworks = ["React", "Angular", "Django", "Spring", "Twig", "Symfony"]

    programming_languages_used = {language: 0 for language in programming_languages}
    frameworks_used = {framework: 0 for framework in frameworks}

    for language in programming_languages:
        for word in textCv.split():
            similarity = fuzz.ratio(language.lower(), word.lower())
            if similarity >= 80:
                programming_languages_used[language] += 1

    for framework in frameworks:
        for word in textCv.split():
            similarity = fuzz.ratio(framework.lower(), word.lower())
            if similarity >= 80:
                frameworks_used[framework] += 1

    best_languages = [lang for lang, count in programming_languages_used.items() if count > 0]
    worst_language = min(programming_languages_used, key=programming_languages_used.get, default=None)

    best_frameworks = [framework for framework, count in frameworks_used.items() if count > 0]
    worst_framework = min(frameworks_used, key=frameworks_used.get, default=None)

    recommendations = {
        'best_language': best_languages[0] if best_languages else None,
        'worst_language': worst_language,
        'best_framework': best_frameworks[0] if best_frameworks else None,
        'worst_framework': worst_framework
    }

    return recommendations


# Function to process CV and return recommendations
def process_cv(cv_file):
    cv_text = read_pdf("static/" + cv_file.filename)
    global textCv
    textCv = preprocess_text(cv_text)

    recommendations = generate_recommendations()

    result = {
        'best_language': recommendations['best_language'],
        'worst_language': recommendations['worst_language'],
        'best_framework': recommendations['best_framework'],
        'worst_framework': recommendations['worst_framework']
    }

    return result
