from pathlib import Path
import json

import ollama

def process_transcript(transcript: str) -> str:
    json_transcript = json.loads(transcript)
    call_transcript = "\n".join(json_transcript.get("call_transcript", []))
    return str(call_transcript)


def transcript_summariser(transcript):
    response=ollama.chat(model="deepseek-r1:1.5b",messages=[
    {'role':'system',
     'content':"""You are an expert analyst in understanding the communication between two people. Your job is to evaluate the call transcript against below categories shown between <categories></categories> Skip the preamble and go straight to the answer.
<categories>
1. Summary: Provide the detailed summary in less than 200 words
2. Purpose of Call : Provide clear motive of call from customer to CSR
3. Sentiment of Call: Understand tone of customer and provide sentiment in Positive, Neutral and Negative
4. Resolution Provided: Details about the resolution provided by CSR to customer.
</categories>"""},
    {'role': 'user',
     'content': transcript},

])
    return response['message']['content']


def transcript_quality_analyzer(transcript):
    quality=ollama.chat(model="deepseek-r1:1.5b",messages=[
    {'role':'system',
     'content':"""Evaluate call transcript against categories shown between <categories></categories> tags and provide score as 'High', 'Medium', 'Low' for each category.
Skip the preamble and go straight to the answer.

<categories>
1. Communication Skills:
 - Clarity: How clearly and concisely does the CSR communicate information?
 - Active Listening: Does the CSR actively listen to the customer's concerns and questions?
 - Empathy: How well does the CSR demonstrate empathy and understanding towards the customer?

2. Problem Resolution:
 - Effectiveness: How well did the CSR resolve the customer's issue or answer their question?
 - Timeliness: Was the issue resolved in a reasonable amount of time?

3. Product Knowledge:
 - Familiarity: Does the CSR have a good understanding of the company's products and services?
 - Accuracy: How accurate and precise are the answers provided by the CSR?

4. Professionalism:
 - Tone and Manner: How professional is the tone and manner of the CSR throughout the call?
 - Courtesy: Does the CSR maintain a courteous and respectful attitude towards the customer?

5. Problem Escalation:
 - Recognition: Did the CSR recognize when an issue required escalation to a higher level of support?
 - Handoff: How smoothly and effectively did the CSR transfer the call if escalation was necessary?

6. Resolution Follow-Up:
 - Follow-Up: Did the CSR provide information about any follow-up actions that would be taken?
 - Customer Satisfaction: Did the CSR inquire about the customer's satisfaction with the resolution?

7. Efficiency:
 - Call Handling Time: Was the call resolved efficiently without unnecessary delays?
 - Multi-Tasking: If applicable, did the CSR effectively handle multiple tasks during the call?

8. Adherence to Policies and Procedures:
 - Compliance: Did the CSR follow company policies and procedures in addressing the customer's issue?
 - Accuracy in Information: How well did the CSR adhere to the correct processes?

9. Technical Competence:
 - System Use: Did the CSR effectively navigate and use the customer service tools and systems?
 - Troubleshooting: How adept is the CSR at troubleshooting technical issues?

10. Customer Satisfaction:
 - Overall Satisfaction: How satisfied is the customer with the service received during the call?
 - Feedback: Did the CSR encourage the customer to provide feedback on the service?

11. Language Proficiency:
 - Clarity of Language: Was the language used by the CSR easily understandable?
 - Language Appropriateness: Did the CSR use appropriate language for effective communication?

12. Conflict Resolution:
 - Handling Difficult Customers: How well did the CSR manage and resolve conflicts with upset or frustrated customers?
 - De-escalation Skills: Did the CSR employ de-escalation techniques when needed?
<categories>

"""},
    {'role': 'user',
     'content': transcript},

])
    return quality['message']['content']

