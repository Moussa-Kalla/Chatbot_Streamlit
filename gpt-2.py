
"""
@author: Moussa Kalla
"""

from transformers import AutoModelForCausalLM, AutoTokenizer
import torch

# Charger le modèle GPT-2 et son tokenizer
model_name = "gpt2"  # Vous pouvez choisir un autre modèle comme "gpt-neo", "gpt-3" selon vos besoins
model = AutoModelForCausalLM.from_pretrained(model_name)
tokenizer = AutoTokenizer.from_pretrained(model_name)

# Définir un prompt
prompt = "What is Large Language  Model ?"

# Convertir le texte en tokens (entrée du modèle)
inputs = tokenizer(prompt, return_tensors="pt")

# Générer du texte
outputs = model.generate(inputs["input_ids"], max_length=100, num_return_sequences=1, no_repeat_ngram_size=2)

# Décoder les tokens générés en texte
generated_text = tokenizer.decode(outputs[0], skip_special_tokens=True)

print(generated_text)
