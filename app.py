import streamlit as st
import requests
from bs4 import BeautifulSoup
from groq import Groq

# إعدادات الصفحة بتصميم عصري (Dark Mode friendly)
st.set_page_config(page_title="AI Social Media Sniper", page_icon="🎯", layout="wide")

# CSS بسيط لتحسين المظهر
st.markdown("""
    <style>
    .main { background-color: #0e1117; }
    .stButton>button { width: 100%; border-radius: 5px; height: 3em; background-color: #ff4b4b; color: white; }
    </style>
    """, unsafe_allow_html=True)

#Sidebar للإعدادات
st.sidebar.title("⚙️ Settings")
api_key = st.sidebar.text_input("Enter Groq API Key:", type="password")
model_option = st.sidebar.selectbox("Choose Model:", 
    ["llama-3.3-70b-versatile", "llama-3.1-8b-instant", "mixtral-8x7b-32768"])

def extract_content(url):
    try:
        headers = {'User-Agent': 'Mozilla/5.0'}
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # إزالة السكريبتات والستايلات لضمان نظافة النص
        for script in soup(["script", "style"]):
            script.extract()

        # جلب العنوان والفقرات
        title = soup.find('h1').get_text() if soup.find('h1') else "No Title"
        paragraphs = soup.find_all('p')
        content = " ".join([p.get_text() for p in paragraphs])
        
        full_text = f"Title: {title}\nContent: {content}"
        return full_text[:5000] # تحديد الحد لتجنب مشاكل الـ Tokens
    except Exception as e:
        return f"Error: {str(e)}"

def generate_social_posts(article_text):
    client = Groq(api_key=api_key)
    
    # الـ Prompt دابا مطور باش يخرج ليك "Facebook Sniper Style"
    prompt = f"""
    You are an expert Social Media Strategist and Copywriter. 
    Analyze this article and generate 3 professional posts.

    Article Content: {article_text}

    1. 🎯 **Facebook Sniper Hook**: 
       Start with a powerful "Open Loop" or "Pattern Interrupt" hook. 
       Use conversational language, emojis, and a clear Call to Action (CTA).
       Target audience: Entrepreneurs and Tech enthusiasts.

    2. 💼 **LinkedIn Insight**: 
       Professional, authoritative tone. Focus on 3 key takeaways or "Lessons Learned". 
       Include relevant industry hashtags.

    3. 🐦 **X (Twitter) Thread Starter**: 
       Punchy, bold, and designed to get retweets. Maximum 280 characters.

    Format the output clearly with bold headings.
    """
    
    try:
        completion = client.chat.completions.create(
            model=model_option,
            messages=[{"role": "system", "content": "You are a helpful AI that creates viral social media content."},
                      {"role": "user", "content": prompt}],
            temperature=0.75,
            max_tokens=2048
        )
        return completion.choices[0].message.content
    except Exception as e:
        return f"❌ Groq Error: {str(e)}"

# واجهة المستخدم الرئيسية
st.title("🚀 AI Social Media Sniper")
st.markdown("قم بتحويل أي مقال تقني إلى منشورات فيسبوك ولينكد إن واحترافية في ثوانٍ.")

url = st.text_input("إلصق رابط المقال هنا:", placeholder="https://example.com/article")

col1, col2 = st.columns([1, 1])

if st.button("Generate Strategy ✨"):
    if not api_key:
        st.error("المرجو إدخال API Key الخاص بـ Groq في الجانب.")
    elif not url:
        st.warning("المرجو وضع رابط صالح.")
    else:
        with st.spinner("⏳ جاري قراءة المقال وتوليد المحتوى..."):
            article_data = extract_content(url)
            
            if "Error" in article_data:
                st.error(f"حدث خطأ أثناء جلب المقال: {article_data}")
            else:
                posts = generate_social_posts(article_data)
                
                st.success("✅ تم توليد المنشورات بنجاح!")
                st.markdown("---")
                st.markdown(posts)
                
                # إمكانية نسخ النص (تحسين تجربة المستخدم)
                st.text_area("Copy Text Here:", value=posts, height=300)

st.sidebar.markdown("---")
st.sidebar.write("Developed for **Mouhcine Digital Systems**")
