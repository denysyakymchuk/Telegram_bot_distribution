import openai


def ref_data(data):
    records = []
    for item in data:
        record = f"{item[0]} - {item[1]}"
        records.append(record)

    result = ",\n".join(records)
    return result


def generate_response(question):
    response = openai.Completion.create(
        engine='text-davinci-003',
        prompt=question,
        max_tokens=50,
        n=1,
        stop=None,
        temperature=0.7
    )

    return response.choices[0].text.strip()
