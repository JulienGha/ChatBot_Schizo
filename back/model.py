import transformers
from transformers import LlamaForCausalLM
import json
from sentence_transformers import SentenceTransformer


def model_generator(file):

    model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')

    # Load the JSON file
    with open('datasets/' + file + '.json', 'r') as f:
        text = json.load(f)
    print(text)

    # Train the model on the text
    model.train_on_dataset(text)

    # Save the model
    model.save_pretrained('models/' + file)


# model_generator('dsm5')

sentences = ["This is an example sentence", "Each sentence is converted"]

model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')
embeddings = model.encode(sentences)
print(embeddings)

