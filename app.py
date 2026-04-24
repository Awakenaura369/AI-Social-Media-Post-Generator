import streamlit as st
import requests
from bs4 import BeautifulSoup
from groq import Groq

# إعدادات الصفحة
st.set_page_config(page_title="AI Social Media Post Generator", page_icon="🚀")

# جلب مفتاح API من Secrets أو المدخلات
api_key = st.sidebar.text_input("Enter Groq API Key:", type="password")

def extract_text_from_url(url):
    try:
        response = requests.get(url, timeout=10)
        soup = BeautifulSoup(response.content, 'html.parser')
        # كنجبدو غير النص المهم (العنوان والفقرات)
        paragraphs = soup.find_all(['h1', 'p'])
        article_text = " ".join([p.get_text() for p in paragraphs])
        return article_text[:4000] # تحديد النص باش ما نفوتوش الـ Context limit
    except Exception as e:
        return f"Error: {e}"

def generate_social_posts(article_content):
    client = Groq(api_key=api_key)
    
    prompt = f"""
    Analyze the following article content and create 3 high-converting social media posts:
    1. **LinkedIn Post**: Professional tone, focused on insights and value, includes 3-5 hashtags.
    2. **Facebook Post**: Engaging, conversational, uses emojis, and a clear Call to Action (CTA).
    3. **Twitter (X) Post**: Concise, punchy, focused on the main hook.

    Article Content: {article_content}
    
    Return the results in a clean, formatted way.
    """
    
    completion = client.chat.completions.create(
        model="llama3-70b-8192",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7,
    )
    return completion.choices[0].message.content

# واجهة المستخدم
st.title("🔗 Article to Social Media Post")
st.subheader("تحويل رابط المقال إلى منشورات احترافية")

url_input = st.text_input("حط رابط المقالة هنا (URL):")

if st.button("Generate Posts ✨"):
    if not api_key:
        st.error("عافاك دخل Groq API Key أولاً!")
    elif not url_input:
        st.warning("دخل الرابط بعدا!")
    else:
        with st.spinner("جاري تحليل المقال وكتابة البوستات..."):
            # 1. استخراج النص
            text = extract_text_from_url(url_input)
            
            if "Error" in text:
                st.error("مقدرناش نقراو الرابط، تأكد واش خدام.")
            else:
                # 2. توليد البوستات
                result = generate_social_posts(text)
                
                st.divider()
                st.markdown(result)
                st.balloons()

# إضافة لمسة "Facebook Sniper" اللي كتعجبك
st.sidebar.info("هاد الأداة مصممة باش تعاونك فـ Personal Branding و Client Acquisition.")
