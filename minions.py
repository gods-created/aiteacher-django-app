from cryptography.fernet import Fernet
from random import choice
from string import (
    ascii_letters,
    digits
)
from os import getenv
from os.path import exists

from transformers import (
    T5ForConditionalGeneration,
    T5Tokenizer,
    TrainingArguments,
    Trainer,
    DataCollatorForSeq2Seq,
)

from datasets import Dataset

def load_model_and_tokenizer(q: bool = False) -> tuple:
    model = None
    tokenizer = None
    loading_model_str = 'google-t5/t5-small'

    model_dir = getenv('MODEL_DIR', './model')
    model_exists = exists(model_dir)

    if q and not model_exists:
        return 'Model not created'
    
    if model_exists:
        loading_model_str = model_dir

    model = T5ForConditionalGeneration.from_pretrained(loading_model_str).to('cpu')
    tokenizer = T5Tokenizer.from_pretrained(loading_model_str, legacy=False)

    return (
        model,
        tokenizer,
    )

def get_answer(question: str) -> str:
    try:
        load_model_and_tokenizer_response = load_model_and_tokenizer(True)
        if not isinstance(load_model_and_tokenizer_response, tuple):
            return load_model_and_tokenizer_response
        
        model, tokenizer = load_model_and_tokenizer_response
        input_ = tokenizer(question, padding=True, return_tensors='pt').to(model.device)
        output = model.generate(input_['input_ids'], max_new_tokens=2000)
        response = tokenizer.decode(output[0], skip_special_tokens=True)
        return response

    except (Exception, ) as e:
        return f'\'get_answer\' error: \'{str(e)}\''
    
def start_training(data: list) -> str:
    try:
        model, tokenizer = load_model_and_tokenizer()
        if not data:
            return 'Model can\'t training without data'
        
        prepared_data = [
            {
                'input_id': tokenizer(item.get('question'), padding=True, return_tensors='pt').input_ids.squeeze(),
                'label': tokenizer(item.get('answer'), padding=True, return_tensors='pt').input_ids.squeeze(),
            }
            for item in data
            if isinstance(item, dict) and {'question', 'answer'}.issubset(item.keys()) and all(item.values())
        ]

        if not prepared_data:
            return 'Model can\'t training without data'
        
        dataset = Dataset.from_dict({
            'input_ids': [item.get('input_id') for item in prepared_data],
            'labels': [item.get('label') for item in prepared_data],
        })

        data_collator = DataCollatorForSeq2Seq(
            model=model,
            tokenizer=tokenizer
        )

        args = TrainingArguments(
            output_dir='./ai_settigs',
            num_train_epochs=3,
            per_device_train_batch_size=4
        )

        training = Trainer(
            model=model,
            data_collator=data_collator,
            args=args,
            train_dataset=dataset
        )

        training.train()
        model.save_pretrained('./model')
        tokenizer.save_pretrained('./model')

        return 'Training finished success'

    except (Exception, ) as e:
        return f'\'gestart_trainingt_answer\' error: \'{str(e)}\''

def generate_random_string():
    return ''.join(choice(ascii_letters + digits) for _ in range(200))

def generate_api_key():
    key = Fernet.generate_key()
    f = Fernet(key)
    random_string = generate_random_string()
    api_key = f.encrypt(random_string.encode()).decode()
    return api_key[:30]