import requests
import matplotlib.pyplot as plt
from collections import defaultdict
from concurrent.futures import ThreadPoolExecutor

# розбиття тексту на слова
def map_function(text):
    words = text.split()
    return [(word.lower().strip('.,!?;:"()[]'), 1) for word in words if word.isalnum()]

# групування слів
def shuffle_function(mapped_values):
    shuffled = defaultdict(list)
    for key, value in mapped_values:
        shuffled[key].append(value)
    return shuffled.items()

# підрахунок частоти слів
def reduce_function(shuffled_values):
    reduced = {}
    for key, values in shuffled_values:
        reduced[key] = sum(values)
    return reduced


# MapReduce
def map_reduce(text):
    # Крок 1: Маппінг
    mapped_values = map_function(text)

    # Крок 2: Shuffle
    shuffled_values = shuffle_function(mapped_values)

    # Крок 3: Редукція
    reduced_values = reduce_function(shuffled_values)

    return reduced_values

# візуалізація
def visualize_top_words(word_counts, top_n=10):
    top_words = sorted(word_counts.items(), key=lambda x: x[1], reverse=True)[:top_n]
    words, counts = zip(*top_words)

    plt.figure(figsize=(12, 8))
    bars = plt.barh(words, counts, color='skyblue')
    plt.xlabel('Частота')
    plt.ylabel('Слова')
    plt.title('Топ 10 слів за частотою використання')
    plt.gca().invert_yaxis()  # Інвертуємо порядок осі Y

    plt.show()

# завантаження тексту за URL
def fetch_text_from_url(url):
    response = requests.get(url)
    response.raise_for_status()
    return response.text

if __name__ == '__main__':
    # Введення URL
    url = input("Введіть URL для аналізу тексту: ")
    
    try:
        text = fetch_text_from_url(url)

        with ThreadPoolExecutor() as executor:
            future = executor.submit(map_reduce, text)
            result = future.result()

        # візуалізація
        visualize_top_words(result, top_n=10)
    
    except requests.exceptions.RequestException as e:
        print(f"Помилка при завантаженні тексту: {e}")
    except Exception as e:
        print(f"Виникла помилка: {e}")
