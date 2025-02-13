from pathlib import Path
import json
import ollama

from fastapi import FastAPI

app = FastAPI()



def process_transcript(transcript: str) -> str:
    json_transcript = json.loads(transcript)
    call_transcript = "\n".join(json_transcript.get("call_transcript", []))
    return str(call_transcript)

@app.route('/call_summarize', methods=['GET', 'POST'])
def summarize(summ):
    call_transcript=process_transcript(summ["call_transcript"])
    response = ollama.chat(model="deepseek-r1:1.5b", messages=[
        {'role': 'system',
         'content': """You are an expert analyst in understanding the communication between two people. Your job is to evaluate the call transcript against below categories shown between <categories></categories> Skip the preamble and go straight to the answer.
    <categories>
    1. Summary: Provide the detailed summary in less than 200 words
    2. Purpose of Call : Provide clear motive of call from customer to CSR
    3. Sentiment of Call: Understand tone of customer and provide sentiment in Positive, Neutral and Negative
    4. Resolution Provided: Details about the resolution provided by CSR to customer.
    </categories>"""},
        {'role': 'user',
         'content': call_transcript},

    ])
    print(response['message']['content'])


# driver function
if __name__ == '__main__':
    app.run(debug=True)