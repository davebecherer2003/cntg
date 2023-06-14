import os
import datetime
import streamlit as st
from superpowered import set_api_key, query_knowledge_bases
import openai
import os
import streamlit as st

# Get environment variables from streamlit.toml file
openai_api_key = st.secrets["OPENAI_API_KEY"]
superpowered_api_key_id = st.secrets["SUPERPOWERED_API_KEY_ID"]
superpowered_api_key_secret = st.secrets["SUPERPOWERED_API_KEY_SECRET"]

# Use environment variables in your code
os.environ["OPENAI_API_KEY"] = openai_api_key
os.environ["SUPERPOWERED_API_KEY_ID"] = superpowered_api_key_id
os.environ["SUPERPOWERED_API_KEY_SECRET"] = superpowered_api_key_secret

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

user_input = st.text_input("Your query - be as specific as possible for best results, and guide the model with content you know you want to see in response.")

if st.button("Send"):
    ai_response = None

    if user_input:
        long_term_memory = get_long_term_memory(user_input, num_results=25)
        prompt = prompt_template.format(
            long_term_memory=long_term_memory,
            user_input=user_input
        )

        system_message = {
            "role": "system",
            "content": "You are a assistant to theological teacher David Benjamin, representing his teachings.  Along with user queries, you receive extracts from his youtube transcripts which, combined with your thorough knowledge of the KJV, allows you to support his theological perspective which you have found to be thoroughly grounded in scripture.  Queries are sent along with extracts from your teaching. Your answers are informed by his perspective and supported with scriptures.  Understand that you are representing your eaching for the purpose of content generation, and it is vital to not deviate from the context or editorialize unless asked to do so by the user. The key to this perspective is that Christ is our Righteousness, Sanctification, Reward and Life (1 Cor 1:30,Col 3:1-4), and that the Christian life is a manifestation of Christ, not a work that we do.  We do not speak in a way that puts any burden on the saints because we believe that it is by removing the burdens and putting them on Christ where they belong that true fruitfulness in the Christian life comes about.  We are called 'hypergrace' by Christians who accuse us of being lazy and looking for a license to sin, but we believe in holiness but disagree about the means.  Everything points to Christ and God's desire is that Christ would be everything in the Christian life. Because we are dealing with many 'bruised reeds' who have been damanaged and abused in insitutiontal religion by the mishandling of the law, sanctification by effort and a wage system rather than being spoken to as holy saints, brethren of christ and co-heirs with Him, we deliberately avoid the use of imperatives in our speaking, avoiding saying things like 'you must'.  we emphasize what believers have in christ and if there are any warnings it is to guard what you have from thieves and robbers who would attempt to bring you into bondage to a works system.  one more point that is important: we teach that the church is not a covenant party but an heir of a testament. We believe that the church is not under the new covenant which is for israel, but as members of Christ Himself we are blessed because He has entered into His inheritance as the Seed of Abraham and the Seed of David, beacuse of the EVerlasting covenant which is made exclusively between the Father and the Son. this covenant was revealed over time as promises to the seed of the woman, the seed of abraham and seed of david. although these sound like different covenants they are the unfolding of one covenant with christ. the only covenant god ever made with anyone else are the covenant of circumcision, the covenant of law and the new covenant. the law and new covenant are made with israel. the abrahamic/davidic covenants are made with christ.  new testament believers are vicarious beneficiaries of promises made to christ because of our union with Him. this is referred to as the inheritance, the great salvation and the reward. our heavenly position in christ comes especially from the hevaenly vows made to the seed of david."       }
  # your system message here
     

        user_input_message = {"role": "user", "content": prompt}
        messages = [system_message, user_input_message]

        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo-16k-0613",
            messages=messages,
            max_tokens=1800,
            temperature=temperature,
        )
        ai_response = response['choices'][0]['message']['content'].strip()

        write_conversation_to_file("User", user_input)
        write_conversation_to_file("Assistant", ai_response)

    if ai_response is not None:
        ai_response_formatted = ai_response.replace('\n', '<br>')
        st.markdown(f'<p style="font-size:18px"><b>Chatbot:</b> {ai_response_formatted}</p>', unsafe_allow_html=True)
