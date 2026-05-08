import numpy as np
from pathlib import Path
from sentence_transformers import SentenceTransformer
from sklearn.cluster import KMeans
from sklearn.feature_extraction.text import TfidfVectorizer
from stop_words import get_stop_words


EMBEDDING_MODEL = 'sentence-transformers/all-MiniLM-L6-v2'
KEYWORDS_PER_THEME = 8
DUTCH_STOP_WORDS = get_stop_words('dutch')


def get_video_themes(video_folder, num_themes=5):
    transcripts = _load_transcripts(video_folder)
    if len(transcripts) == 0:
        return

    num_themes = min(num_themes, len(transcripts))
    texts = list(transcripts.values())
    cluster_labels = _cluster_texts(texts, num_themes)
    themes = _describe_clusters(texts, cluster_labels, num_themes)
    _save_themes(themes, video_folder)


def _load_transcripts(folder):
    transcript_paths = [
        p for p in Path(folder).iterdir()
        if p.suffix == '.txt' and p.stem != 'themes'
    ]
    return {p.stem: p.read_text(encoding='utf-8').strip() for p in transcript_paths if p.stat().st_size > 0}


def _cluster_texts(texts, num_clusters):
    model = SentenceTransformer(EMBEDDING_MODEL)
    embeddings = model.encode(texts, show_progress_bar=False)
    kmeans = KMeans(n_clusters=num_clusters, random_state=42, n_init='auto')
    return kmeans.fit_predict(embeddings)


def _describe_clusters(texts, labels, num_clusters):
    vectorizer = TfidfVectorizer(max_features=100, stop_words=DUTCH_STOP_WORDS)
    vectorizer.fit(texts)
    feature_names = vectorizer.get_feature_names_out()

    themes = []
    for cluster_id in range(num_clusters):
        cluster_texts = [t for t, l in zip(texts, labels) if l == cluster_id]
        keywords = _extract_keywords(cluster_texts, vectorizer, feature_names)
        themes.append(f"Thema {cluster_id + 1}: {', '.join(keywords)}")

    return themes


def _extract_keywords(cluster_texts, vectorizer, feature_names):
    if not cluster_texts:
        return []
    matrix = vectorizer.transform(cluster_texts)
    scores = np.asarray(matrix.sum(axis=0)).flatten()
    top_indices = scores.argsort()[-KEYWORDS_PER_THEME:][::-1]
    return [feature_names[i] for i in top_indices]


def _save_themes(themes, video_folder):
    themes_path = Path(video_folder) / 'themes.txt'
    themes_path.write_text('\n'.join(themes), encoding='utf-8')
