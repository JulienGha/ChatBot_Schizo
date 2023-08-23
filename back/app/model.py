import transformers
from transformers import LlamaForCausalLM

import json


def model_generator(file):
    # Load the Llama 2 model and tokenizer
    model = LlamaForCausalLM.from_pretrained("./Llama-2-13b-chat-hf")

    # Load the JSON file
    with open('datasets/' + file + '.json', 'r') as f:
        text = json.load(f)

    # Train the model on the text
    model.train_on_dataset(text)

    # Save the model
    model.save_pretrained('models/' + file)


model_generator('dsm5')
