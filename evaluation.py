import re
from dotenv import load_dotenv
import warnings
from src.scripts.database import load_chroma_db
from src.scripts.prompts import create_chain
from src.resources.red_questions import red_questions
from src.resources.green_questions import green_questions
from nltk.translate.bleu_score import sentence_bleu, SmoothingFunction
from rouge_score import rouge_scorer


loaded_db = load_chroma_db()
retriever = loaded_db.as_retriever(
    search_type="mmr",
    search_kwargs={"k": 2}
)

chain = create_chain(retriever)

# Удаляем знаки препинания и приводит к нижнему регистру
def tokenize(text):
    return set(re.findall(r'\w+', text.lower()))

# Метрика Answer Relevancy (Jaccard Similarity)
def answer_relevancy(answer, ground_truth):
    tokens_answer = tokenize(answer)
    tokens_ground_truth = tokenize(ground_truth)
    union = tokens_answer | tokens_ground_truth
    if not union:
        return 0.0
    return len(tokens_answer & tokens_ground_truth) / len(union)

# Метрика Faithfulness
def faithfulness(answer, ground_truth):
    tokens_answer = tokenize(answer)
    tokens_ground_truth = tokenize(ground_truth)
    if not tokens_answer:
        return 0.0
    return len(tokens_answer & tokens_ground_truth) / len(tokens_answer)

# Метрика Contextual Recall
def contextual_recall(answer, ground_truth):
    tokens_answer = tokenize(answer)
    tokens_ground_truth = tokenize(ground_truth)
    if not tokens_ground_truth:
        return 0.0
    return len(tokens_answer & tokens_ground_truth) / len(tokens_ground_truth)

# Метрика Contextual Precision
def contextual_precision(answer, ground_truth):
    tokens_answer = tokenize(answer)
    tokens_ground_truth = tokenize(ground_truth)
    if not tokens_answer:
        return 0.0
    return len(tokens_answer & tokens_ground_truth) / len(tokens_answer)

# Метрика Contextual Relevancy: F1-мера от contextual precision и contextual recall
def contextual_relevancy(answer, ground_truth):
    precision = contextual_precision(answer, ground_truth)
    recall = contextual_recall(answer, ground_truth)
    if precision + recall == 0:
        return 0.0
    return 2 * precision * recall / (precision + recall)


def bleu_score(answer, ground_truth):
    reference = [ground_truth.split()]
    candidate = answer.split()
    smoothie = SmoothingFunction().method4
    return sentence_bleu(reference, candidate, smoothing_function=smoothie)

def normalize_text(text):
    return ' '.join(re.findall(r'\w+', text.lower()))


def rouge_scores(answer, ground_truth):
    scores = scorer.score(ground_truth, answer)
    return {
        "ROUGE-1": scores["rouge1"].fmeasure,
        "ROUGE-L": scores["rougeL"].fmeasure
    }


# Тестовые примеры вопросов
green_questions = green_questions
red_questions = red_questions


def test_pipeline(chain, test_examples):
    results = []
    for example in test_examples:
        query = example["query"]
        ground_truth = example["ground_truth"]

        # Получаем ответ от цепочки 
        response = chain.invoke(query)

        # Вычисляем метрики
        metrics = {
            "Answer Relevancy": answer_relevancy(response, ground_truth),
            "Faithfulness": faithfulness(response, ground_truth),
            "Contextual Recall": contextual_recall(response, ground_truth),
            "Contextual Precision": contextual_precision(response, ground_truth),
            "Contextual Relevancy": contextual_relevancy(response, ground_truth),
            "BLEU": bleu_score(response, ground_truth),
        }

        rouge = rouge_scores(response, ground_truth)
        metrics.update({
            "ROUGE-1": rouge["ROUGE-1"],
            "ROUGE-L": rouge["ROUGE-L"],
        })

        results.append({
            "query": query,
            "response": response,
            "ground_truth": ground_truth,
            "evaluation": metrics,
        })

    return results


def print_results(results, label):
    print(f"Тестирование '{label}' вопросов:")
    for result in results:
        print(f"Query: {result['query']}")
        print(f"Response: {result['response']}")
        print(f"Ground Truth: {result['ground_truth']}")
        print("Evaluation Results:")
        for metric_name, metric_value in result["evaluation"].items():
            print(f"  {metric_name}: {metric_value:.2f}")
        print("-" * 50)

# Запускаем тестирование для "зеленых" и "красных" вопросов
green_results = test_pipeline(chain, green_questions)
red_results = test_pipeline(chain, red_questions)

print_results(green_results, "зеленых")
print_results(red_results, "красных")
