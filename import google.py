import google.generativeai as genai

genai.configure(api_key="AIzaSyCvH8kpNmTc_dqnVcuiDnuvSkIbVeLexYE")

for m in genai.list_models():
    print(m.name)