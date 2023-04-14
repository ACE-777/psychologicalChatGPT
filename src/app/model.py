import openai

model_engine = "text-davinci-003"


def model(prompt, max_tokens_in_model):
    """
            Creates a model based on Chat-GPT for the answering users questions.
    """
    completion = openai.Completion.create(
        engine=model_engine,
        prompt=prompt,
        max_tokens=max_tokens_in_model,
        temperature=0.5,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )
    return completion
