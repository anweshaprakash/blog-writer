# 📝 AI Blog Post Generator

A Streamlit-based application that leverages **LangChain** and **CrewAI** to generate complete, SEO-optimized blog posts using OpenAI's GPT models.

## 🚀 Features

- ✍️ Automatic blog post generation from a topic and audience  
- 🧠 Supports two frameworks: **LangChain** and **CrewAI**  
- 🎯 Customizable tone, target audience, word count, and keywords  
- 🔍 Built-in SEO optimization  
- 🧩 Modular architecture for outline, writing, and SEO agents  
- 📥 Download your final blog post in `.txt` format  

## 📽️ Demo Video

👉 [Watch the demo on Loom](https://www.loom.com/share/d40d56d22004478cbfa6ae41084adaec)  


## ⚙️ Installation

```bash
git clone https://github.com/anweshaprakash/blog-writer.git
cd blog-writer
pip install -r requirements.txt
```

## 🛠️ Setup

Create a `.env` file in the root directory and add your OpenAI key:

```env
OPENAI_API_KEY=your_openai_api_key
```

## 🧪 Run the App

```bash
streamlit run blog_writer.py
```

## 🎯 Usage

1. Choose your model and creativity level  
2. Select framework: LangChain or CrewAI  
3. Enter topic, audience, tone, word count, and keywords  
4. Click **Generate Blog Post**  
5. View and download your blog content  

## 🛠️ Tech Stack

- [LangChain](https://python.langchain.com/)
- [CrewAI](https://docs.crewai.com/)
- [Streamlit](https://streamlit.io/)
- [OpenAI GPT-4 / GPT-3.5](https://platform.openai.com/)

## 🧠 Architecture Overview

```
Topic + Audience + Tone + Keywords
           │
           ▼
   ┌────────────────────┐
   │  LangChain / CrewAI│
   └────────────────────┘
           │
 ┌─────────┴─────────┐
 ▼                   ▼
[Outline Agent]   [Writer Agent]
           │
           ▼
       [SEO Agent]
           │
           ▼
    Final Blog Output
```

## 🐛 Troubleshooting

- Ensure you have a valid `.env` file with `OPENAI_API_KEY`.  
- Use Python 3.9+ for better compatibility.  
- If CrewAI errors out, check for updated versions or API rate limits.

## 📄 License

MIT License

---

Made with ❤️ by [Anwesha Prakash](https://github.com/anweshiprakash)
