from clustering import read_txt_and_tfidf, kmeans_on_text, cluster_assessment, read_txt_and_vectorize
from sentiment import score
from utils import save_text_from_html


def main():
    save_text_from_html('Files', 'Filestxt')
    # save_title('Files', 'Filestitles')
    matrix, vec, texts, doc_name = read_txt_and_tfidf('Filestxt', False, True)
    # matrix, vec, texts, doc_name = read_txt_and_vectorize('Filestitles', False, False)
    labels = kmeans_on_text(matrix, vec, 3, True)
    labels2 = kmeans_on_text(matrix, vec, 6, True)
    cluster_assessment(matrix, 50)
    score(texts, labels, 3, doc_name)
    score(texts, labels2, 6, doc_name)


main()
