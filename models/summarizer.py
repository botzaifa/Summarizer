from transformers import T5Tokenizer, T5ForConditionalGeneration
import torch
import yaml

# Function to load the config file
def load_config(path="config/config.yaml"):
    with open(path, "r") as f:
        return yaml.safe_load(f)

# Load the config
config = load_config()

class TextSummarizer:
    def __init__(self, model_name: str = "t5-base", device: str = None):
        self.device = device if device else ("cuda" if torch.cuda.is_available() else "cpu")
        self.tokenizer = T5Tokenizer.from_pretrained(model_name)
        self.model = T5ForConditionalGeneration.from_pretrained(model_name)
        self.model.to(self.device)

    def summarize(self, text: str) -> str:
        # Prepare text for summarization
        input_text = "summarize: " + text.strip().replace("\n", " ")

        inputs = self.tokenizer.encode(
            input_text,
            return_tensors="pt",
            max_length=1024,  # Allow full input to be considered
            truncation=True
        ).to(self.device)

        # Adjust max length and min length for longer summaries
        input_len = inputs.shape[1]
        dynamic_max = min(int(0.4 * input_len), 2000)  # Remove restriction: allow a very high max length
        dynamic_min = 100  # Set a reasonable minimum length to avoid empty summaries

        # Generate summary
        summary_ids = self.model.generate(
            inputs,
            max_length=dynamic_max,  # Set high max length
            min_length=dynamic_min,  # Ensure summary is not too short
            length_penalty=1.0,  # Set length penalty to avoid overly short summaries
            num_beams=4,         # Increase beam search for better quality
            no_repeat_ngram_size=2,  # Prevent repeating phrases
            early_stopping=True  # Stop early once a good summary is generated
        )

        return self.tokenizer.decode(summary_ids[0], skip_special_tokens=True)



# from transformers import BartTokenizer, BartForConditionalGeneration
# import torch
# import yaml

# # Function to load the config file
# def load_config(path="config/config.yaml"):
#     with open(path, "r") as f:
#         return yaml.safe_load(f)

# # Load the config
# config = load_config()

# class TextSummarizer:
#     def __init__(self, model_name: str = "facebook/bart-large-cnn", device: str = None):
#         self.device = device if device else ("cuda" if torch.cuda.is_available() else "cpu")
#         self.tokenizer = BartTokenizer.from_pretrained(model_name)
#         self.model = BartForConditionalGeneration.from_pretrained(model_name)
#         self.model.to(self.device)

#     def summarize(self, text: str) -> str:
#         # Use "long" summary settings from config
#         length_setting = config["summary_length"]["long"]
#         min_len = length_setting["min_length"]
#         max_len = length_setting["max_length"]

#         # Prepare text for summarization
#         input_text = text.strip()

#         inputs = self.tokenizer.encode(
#             input_text,
#             return_tensors="pt",
#             max_length=1024,
#             truncation=True
#         ).to(self.device)

#         # Adjust max length and min length
#         input_len = inputs.shape[1]
#         dynamic_max = min(int(0.4 * input_len), max_len)
#         dynamic_min = min(min_len, dynamic_max - 10) if dynamic_max > 20 else 10

#         # Generate summary using better settings
#         summary_ids = self.model.generate(
#             inputs,
#             max_length=dynamic_max,
#             min_length=dynamic_min,
#             length_penalty=1.0,
#             num_beams=4,
#             no_repeat_ngram_size=2,
#             early_stopping=True
#         )

#         return self.tokenizer.decode(summary_ids[0], skip_special_tokens=True)
