import os
from dotenv import load_dotenv
from langchain.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
from langchain.agents import AgentExecutor, create_react_agent
from langchain import hub
from langchain_core.tools import Tool
import json
import streamlit as st
from crewai import Agent, Task, Crew

load_dotenv()
openai_api_key = os.getenv("OPENAI_API_KEY")

llm = ChatOpenAI(temperature=0.8, model="gpt-4")

def get_llm(temperature: float, model_name: str) -> ChatOpenAI:
    """Create a new ChatOpenAI instance with specified parameters"""
    return ChatOpenAI(temperature=temperature, model=model_name)

def generate_outline(topic: str, audience: str, llm: ChatOpenAI) -> str:
    """Generate a content outline"""
    outline_prompt = PromptTemplate(
        template="Create detailed outline for blog post about '{topic}' for audience '{audience}'. Include:\n- Main sections\n- Sub-sections\n- Key points\n- Suggested call-to-action",
        input_variables=["topic", "audience"]
    )
    chain = outline_prompt | llm
    return chain.invoke({"topic": topic, "audience": audience}).content

def generate_blog_post(topic: str, audience: str, tone: str, word_count: int, keywords: str, llm: ChatOpenAI) -> str:
    """Generate complete blog post"""
    blog_prompt = PromptTemplate(
        template="Write comprehensive blog post about {topic} for {audience} ({tone} tone, {word_count} words). Keywords: {keywords}",
        input_variables=["topic", "audience", "tone", "word_count", "keywords"]
    )
    chain = blog_prompt | llm
    return chain.invoke({
        "topic": topic,
        "audience": audience,
        "tone": tone,
        "word_count": word_count,
        "keywords": keywords
    }).content

def seo_optimizer(text: str, keywords: str, llm: ChatOpenAI) -> str:
    """Optimize content for SEO"""
    seo_prompt = PromptTemplate(
        template="Improve SEO for this content using keywords {keywords}:\n\n{text}",
        input_variables=["text", "keywords"]
    )
    chain = seo_prompt | llm
    return chain.invoke({"text": text, "keywords": keywords}).content

def clean_crewai_output(result):
    """Helper function to extract clean output from CrewAI results"""
    if isinstance(result, str):
        return result
    elif isinstance(result, dict):
        return result.get('raw', str(result))
    return str(result)

def crewai_blog_post(topic: str, audience: str, tone: str, word_count: int, keywords: str, llm: ChatOpenAI) -> str:
    """Orchestrate the blog writing process using CrewAI"""
    
    outline_agent = Agent(
        role='Content Strategist',
        goal='Create compelling content outlines',
        backstory='Expert in structuring engaging content for various audiences',
        llm=llm,
        verbose=True
    )
    
    writer_agent = Agent(
        role='Content Writer',
        goal='Write high-quality blog posts',
        backstory='Skilled writer with expertise in various industries and tones',
        llm=llm,
        verbose=True
    )
    
    seo_agent = Agent(
        role='SEO Specialist',
        goal='Optimize content for search engines',
        backstory='SEO expert with deep knowledge of keyword optimization',
        llm=llm,
        verbose=True
    )
    
  
    outline_task = Task(
        description=f"Create an outline for a blog post about {topic} targeting {audience}",
        agent=outline_agent,
        expected_output='Detailed content outline with main sections, sub-sections, and key points'
    )
    
    writing_task = Task(
        description=f"""Write a {word_count}-word blog post about {topic} for {audience} 
        with a {tone} tone. Keywords to include: {keywords}""",
        agent=writer_agent,
        expected_output='Well-written blog post with proper structure and engaging content',
        context=[outline_task]
    )
    
    seo_task = Task(
        description=f"Optimize the blog post for SEO using keywords: {keywords}",
        agent=seo_agent,
        expected_output='SEO-optimized version of the blog post with improved keyword usage',
        context=[writing_task]
    )
    
   
    crew = Crew(
        agents=[outline_agent, writer_agent, seo_agent],
        tasks=[outline_task, writing_task, seo_task],
        verbose=True
    )
    
    result = crew.kickoff()
    return clean_crewai_output(result)

def langchain_blog_post(topic: str, audience: str, tone: str, word_count: int, keywords: str, llm: ChatOpenAI) -> str:
    """Original LangChain implementation"""
    tools = [
        Tool(
            name="OutlineGenerator",
            func=lambda x: generate_outline(**json.loads(x), llm=llm),
            description="Creates content outlines. Input should be JSON with 'topic' and 'audience' keys"
        ),
        Tool(
            name="BlogWriter",
            func=lambda x: generate_blog_post(**json.loads(x), llm=llm),
            description="Writes blog posts. Input should be JSON with 'topic', 'audience', 'tone', 'word_count', 'keywords'"
        ),
        Tool(
            name="SEOOptimizer",
            func=lambda x: seo_optimizer(**json.loads(x), llm=llm),
            description="Optimizes content. Input should be JSON with 'text' and 'keywords'"
        )
    ]
    
    prompt = hub.pull("hwchase17/react")
    agent = create_react_agent(llm, tools, prompt)
    agent_executor = AgentExecutor(
        agent=agent,
        tools=tools,
        verbose=False,
        handle_parsing_errors=True
    )
    
    result = agent_executor.invoke({
        "input": f"""Write a blog post about {topic} for {audience} with {tone} tone, 
        {word_count} words, using keywords: {keywords}. Follow this process:
        1. First create an outline using OutlineGenerator
        2. Then write the full post using BlogWriter
        3. Finally optimize for SEO using SEOOptimizer"""
    })
    return result['output']

def main():
    st.title("AI Blog Post Generator")
    
    with st.sidebar:
        st.header("Settings")
        model_name = st.selectbox(
            "Model",
            ["gpt-4", "gpt-3.5-turbo"],
            index=0
        )
        temperature = st.slider(
            "Creativity (Temperature)",
            min_value=0.0,
            max_value=1.0,
            value=0.8,
            step=0.1
        )
        framework = st.radio(
            "Framework",
            ["LangChain", "CrewAI"],
            index=0
        )
    topic = st.text_input("Blog Topic", "The Future of AI in Content Creation")
    audience = st.text_input("Target Audience", "marketing professionals")
    tone = st.text_input("Tone", "insightful yet accessible")
    word_count = st.number_input("Word Count", min_value=300, max_value=5000, value=1200)
    keywords = st.text_input("Keywords (comma separated)", "AI content creation, future of marketing, automated content")
    
    if st.button("Generate Blog Post"):
        with st.spinner("Generating your blog post..."):
            try:
                # Create new LLM instance with current settings
                current_llm = get_llm(temperature, model_name)
                
                if framework == "LangChain":
                    blog_post = langchain_blog_post(topic, audience, tone, word_count, keywords, current_llm)
                else:
                    blog_post = crewai_blog_post(topic, audience, tone, word_count, keywords, current_llm)
                
                st.subheader("Generated Blog Post")
                st.write(blog_post)
               
                st.download_button(
                    label="Download Blog Post",
                    data=blog_post,
                    file_name=f"blog_post_{topic[:20]}.txt",
                    mime="text/plain"
                )
                
            except Exception as e:
                st.error(f"Error occurred: {str(e)}")

if __name__ == "__main__":
    main()