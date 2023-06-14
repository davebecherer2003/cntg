import os
import datetime
import streamlit as st
from superpowered import set_api_key, query_knowledge_bases
import openai
import os
import streamlit as st

# Get environment variables from streamlit.toml
openai_api_key = st.secrets["OPENAI_API_KEY"]
superpowered_api_key_id = st.secrets["SUPERPOWERED_API_KEY_ID"]
superpowered_api_key_secret = st.secrets["SUPERPOWERED_API_KEY_SECRET"]

# Use environment variables in your code
os.environ["OPENAI_API_KEY"] = openai_api_key
os.environ["SUPERPOWERED_API_KEY_ID"] = superpowered_api_key_id
os.environ["SUPERPOWERED_API_KEY_SECRET"] = superpowered_api_key_secret

# Initialize chatbot output
chatbot_output = ""

# Rest of your code goes here
# Initialize Superpowered API
#set_api_key(SUPERPOWERED_API_KEY_ID, SUPERPOWERED_API_KEY_SECRET)

# Create the prompt template for the LLM call
prompt_template = """
{long_term_memory}

user: {user_input}

assistant:
""".strip()

temperature = 0.3

st.title("Query David Benjamin's Teachings")

@st.cache_data
def get_long_term_memory(user_input: str, num_results=18):
    knowledge_base_ids = ["6e7d0ae2-71f8-46d6-85f2-f3d22cf40064","4b177cf2-bb2e-4752-8567-1c78129216d9"]
    results = query_knowledge_bases(
        knowledge_base_ids=knowledge_base_ids,
        query=user_input,
        summarize_results=False,
        top_k=num_results
    )
    
    # Add this code to write the query results to the file
    with open('knowledge_base_exports.txt', 'a') as file:
        file.write(f"Query: {user_input}\n")
        for i, result in enumerate(results["ranked_results"]):
            file.write(f"Result {i+1}: {result['content']}\n\n")
    
    # Format the results into a string that can be used by GPT-3
    long_term_memory = "\n".join([result['content'] for result in results["ranked_results"]])
    return long_term_memory

user_input = st.text_input("Your query - be as specific as possible for best results, and guide the model with content you know you want to see in response.")

if st.button("Send"):
    if user_input:
        long_term_memory = get_long_term_memory(user_input, num_results=18)
        prompt = prompt_template.format(
            long_term_memory=long_term_memory,
            user_input=user_input
        )

        system_message = {
            "role": "system",
            "content": "[IDENTITY/ROLE] you are assistant to theological teacher David Benjamin, representing his teachings.  Along with user queries, you receive extracts from his youtube transcripts which, combined with your thorough knowledge of the KJV, allows you to support his theological perspective which you have found to be thoroughly grounded in scripture.  Queries are sent along with extracts from your teaching. Your answers are informed by his perspective and supported with scriptures.  Understand that you are representing your teaching for the purpose of content generation, and it is vital to not deviate from the context or editorialize unless asked to do so by the user. [FORMAT NOTE:] Present your answers with supporting scripture references in parenthesis throughout. [THEOLOGICAL PERSPECTIVE AND INTERPRETIVE PRINCIPLES]: The key to this perspective is that Christ is our Righteousness, Sanctification, Reward and Life (1 Cor 1:30,Col 3:1-4), and that the Christian life is a manifestation of Christ, not a work that we do.  We do not speak in a way that puts any burden on the saints because we believe that it is by removing the burdens and putting them on Christ where they belong that true fruitfulness in the Christian life comes about.  We are called 'hypergrace' by Christians who accuse us of being lazy and looking for a license to sin, but we believe in holiness but disagree about the means.  Everything points to Christ and God's desire is that Christ would be everything in the Christian life. Christ is the seed of Abraham and captain of our salvation, believers are joint heirs with Him through justification by faith (Romans 4:1-5, Galatians 3:16, Hebrews 6:13-20). Christ is our righteousness, sanctification, redemption, reward and life (1 Corinthians 1:30, Colossians 3:1-4, Galatians 2:19-22). The Bema seat judgment for the Church is a celebration (1 Corinthians 3:12-15, 2 Corinthians 5:17, Ephesians 2:10, Ephesians 5:27, Colossians 1:28-29). The reward is the inheritance of Christ Himself, the of David (Romans 1:2-4, Romans 8:16-17, Galatians 3:29, Ephesians 1:5-6, 11-14). He has made us joint heirs with Him. We are enjoying Christ’s portion, His access, His fellowship with the Father, His position, and blessing through the Spirit (Galatians 4:7, Ephesians 2:18, Ephesians 3:12). This perspective should be the interpreting principle for unlocking the meaning of every scripture, as throughout the scripture, we see Christ as the heir of all things (Hebrews 2:10).  We endeavour to teach and write consistently from this perspective. Because we are dealing with many 'bruised reeds' who have been damaged and abused in institutional religion by the mishandling of the law, sanctification by effort and a wage system rather than being spoken to as holy saints, brethren of Christ and co-heirs with Him, we deliberately avoid the use of imperatives in our speaking, avoiding saying things like 'you must'.  We emphasize what believers have in Christ and if there are any warnings it is to guard what you have from thieves and robbers who would attempt to bring you into bondage to a works system."
        }
        user_input_message = {"role": "user", "content": prompt}
        messages = [system_message, user_input_message]

        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo-16k-0613",
            messages=messages,
            max_tokens=1800,
            temperature=temperature,
        )
        chatbot_output = response['choices'][0]['message']['content'].strip()

    # Display chatbot output if available
    if chatbot_output:
        st.markdown(f'<p style="font-size:18px"><b>Chatbot:</b> {chatbot_output}</p>', unsafe_allow_html=True)
