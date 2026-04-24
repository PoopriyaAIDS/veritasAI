// ── CHATBOT LOGIC ──
        let chatOpen = false;

        // Knowledge base — rule based responses
        const rules = [
            {
                keys: ['what is fake news', 'define fake news', 'meaning of fake news', 'fake news means'],
                answer: `<strong>What is Fake News?</strong>
Fake news is false or misleading information presented as real news. It is designed to deceive readers, spread misinformation, or manipulate public opinion.\n\nCommon types include:\n• Fabricated stories\n• Misleading headlines\n• Conspiracy theories\n• Manipulated images or videos`
            },
            {
                keys: ['how to use', 'how do i use', 'how does this work', 'how to analyze', 'guide', 'help'],
                answer: `<strong>How to Use VeritasAI</strong>
It's simple! Choose your input type:\n\n📝 <b>Text Tab</b> — Paste any news article or headline\n🖼️ <b>Image Tab</b> — Upload a screenshot of news\n🎬 <b>Video Tab</b> — Upload a news video file\n\nThen click <b>Analyze for Authenticity</b> and get your result instantly!`
            },
            {
                keys: ['how accurate', 'accuracy', 'how reliable', 'how good', 'performance'],
                answer: `<strong>Model Accuracy</strong>
VeritasAI achieves <b>91.34% accuracy</b> trained on over 200,000 news articles.\n\nTraining datasets:\n• ISOT Dataset (2010–2017)\n• WELFake Dataset (up to 2022)\n• LIAR Dataset (up to 2022)\n\nThe model uses Logistic Regression + TF-IDF vectorization with 150,000 features.`
            },
            {
                keys: ['credibility score', 'what is credibility', 'score mean', 'what does score'],
                answer: `<strong>Credibility Score (0–100)</strong>
This measures how trustworthy the <b>news content</b> is.\n\n• 70–100 → Likely real and credible\n• 40–69  → Uncertain, verify manually\n• 0–39   → Likely fake or misleading\n\nIt is based on the probability that the content matches real news patterns learned during training.`
            },
            {
                keys: ['confidence level', 'what is confidence', 'confidence mean'],
                answer: `<strong>Confidence Level</strong>
This shows how <b>certain the model is</b> about its prediction.\n\n• HIGH   → 85%+ certainty\n• MEDIUM → 65–84% certainty\n• LOW    → Below 65% certainty\n\nNote: Credibility Score is about the news content. Confidence Level is about the model's certainty.`
            },
            {
                keys: ['categories', 'what categories', 'types of news', 'which topics', 'supports'],
                answer: `<strong>Supported News Categories</strong>
VeritasAI detects fake news across all 8 categories:\n\n🏛️ Politics & Government\n🏥 Health & Medicine\n🔭 Science & Technology\n💰 Business & Economy\n⚽ Sports\n🎬 Entertainment & Celebrity\n🌍 Environment & Climate\n🚔 Crime & Justice`
            },
            {
                keys: ['how to verify', 'verify news', 'check news', 'tips', 'fact check', 'trusted sources'],
                answer: `<strong>How to Verify News</strong>
Follow these steps to fact-check any news:\n\n1️⃣ Search on <b>Reuters, AP News, BBC</b>\n2️⃣ Check fact-checking sites like <b>Snopes, FactCheck.org, PolitiFact</b>\n3️⃣ Look for <b>named sources</b> — anonymous = suspicious\n4️⃣ Check the <b>publication date</b>\n5️⃣ Reverse image search any photos\n6️⃣ Be skeptical of ALL CAPS headlines`
            },
            {
                keys: ['red flag', 'what are red flags', 'suspicious', 'warning signs'],
                answer: `<strong>Red Flags of Fake News</strong>
VeritasAI checks for these warning signs:\n\n🚩 "Share before deleted" urgency\n🚩 Sensational words (SHOCKING, BOMBSHELL)\n🚩 Anonymous or unnamed sources\n🚩 Conspiracy theory terms\n🚩 Anti-pharma / miracle cure claims\n🚩 Excessive exclamation marks!!!\n🚩 100% guaranteed claims\n🚩 Known conspiracy topics (5G, microchips)`
            },
            {
                keys: ['image', 'upload image', 'screenshot', 'photo', 'ocr'],
                answer: `<strong>Image Analysis</strong>
Upload a screenshot of any news article and VeritasAI will:\n\n1. Extract the text using <b>OCR (Tesseract)</b>\n2. Clean and process the text\n3. Run it through the ML model\n4. Show you the verdict\n\n💡 Tip: Include at least 2–3 paragraphs in your screenshot for best accuracy!`
            },
            {
                keys: ['video', 'upload video', 'speech', 'audio'],
                answer: `<strong>Video Analysis</strong>
Upload a news video file and VeritasAI will:\n\n1. Extract the audio track\n2. Convert speech to text\n3. Analyze the first <b>60 seconds</b>\n4. Show you the verdict\n\n💡 Supported formats: MP4, AVI, MOV, MKV, WEBM\n⚠️ Requires clear English speech in the video.`
            },
            {
                keys: ['probability', 'real probability', 'fake probability', 'percentage'],
                answer: `<strong>Probability Distribution</strong>
Shows the ML model's raw probability scores:\n\n✅ <b>REAL %</b> — probability the content is genuine news\n❌ <b>FAKE %</b> — probability the content is misinformation\n\nThese two always add up to 100%. The higher score determines the final verdict.`
            },
            {
                keys: ['who made', 'who created', 'about this app', 'about veritasai', 'developer'],
                answer: `<strong>About VeritasAI</strong>
VeritasAI is an AI-based fake news detection system built using:\n\n🤖 <b>Machine Learning</b> — Logistic Regression\n📊 <b>NLP</b> — TF-IDF Vectorization\n🔍 <b>OCR</b> — Tesseract for image analysis\n🎙️ <b>Speech-to-Text</b> — for video analysis\n🌐 <b>Flask</b> — Python web framework`
            },
            {
                keys: ['hello', 'hi', 'hey', 'good morning', 'good evening', 'howdy'],
                answer: `<strong>Hello! 👋</strong>
Welcome to VeritasAI! I'm VeritasBot, your fake news detection assistant.\n\nI can help you with:\n• Using the app\n• Understanding results\n• News verification tips\n• How the AI works\n\nWhat would you like to know?`
            },
            {
                keys: ['thank', 'thanks', 'thank you', 'great', 'awesome', 'good job'],
                answer: `You're welcome! 😊\n\nRemember — always verify news from multiple trusted sources before sharing. Stay informed and stay safe! 🗞️`
            },
            {
                keys: ['bye', 'goodbye', 'see you', 'exit'],
                answer: `Goodbye! 👋\n\nStay vigilant against misinformation. Remember — when in doubt, verify before you share! 🗞️`
            },
            {
                keys: ['what is tfidf', 'tf idf', 'tf-idf', 'tfidf', 'term frequency'],
                answer: `<strong>What is TF-IDF?</strong>\nTF-IDF stands for <b>Term Frequency - Inverse Document Frequency</b>.\n\nIt converts text into numbers the ML model can understand.\n\n📌 <b>TF</b> — How often a word appears in the article\n📌 <b>IDF</b> — How rare the word is across all articles\n\nWords common in fake news (SHOCKING, EXPOSED, BOMBSHELL) get high scores — helping detect misinformation! 🎯`
            },
            {
                keys: ['what is nlp', 'natural language processing', 'nlp mean'],
                answer: `<strong>What is NLP?</strong>\nNLP stands for <b>Natural Language Processing</b> — AI that helps computers understand human language.\n\nIn VeritasAI, NLP is used to:\n📝 Read and analyze news text\n🔍 Detect suspicious writing patterns\n📊 Convert words into numbers\n🚩 Identify fake news language\n\nWithout NLP, the computer cannot understand words! 🤖`
            },
            {
                keys: ['logistic regression', 'what algorithm', 'which algorithm', 'ml algorithm'],
                answer: `<strong>Logistic Regression</strong>\nThe ML algorithm powering VeritasAI.\n\nHow it works:\n1️⃣ Reads TF-IDF features of the news\n2️⃣ Calculates probability of REAL vs FAKE\n3️⃣ Real > 50% → REAL NEWS\n4️⃣ Fake > 50% → FAKE NEWS\n\n✅ Achieves 91.34% accuracy on 200,000+ articles!`
            },
            {
                keys: ['what is ocr', 'ocr mean', 'tesseract', 'optical character'],
                answer: `<strong>What is OCR?</strong>\nOCR stands for <b>Optical Character Recognition</b> — technology that reads text from images.\n\nVeritasAI uses <b>Tesseract OCR v5.5</b> which:\n📸 Scans your uploaded image\n🔤 Extracts all readable text\n🤖 Sends text to the ML model\n✅ Returns the verdict\n\n💡 Works best with clear, high resolution screenshots!`
            },
            {
                keys: ['what is machine learning', 'machine learning', 'what is ml', 'what is ai', 'artificial intelligence'],
                answer: `<strong>What is Machine Learning?</strong>\nML is a type of AI where computers learn from data instead of being manually programmed.\n\nVeritasAI's ML model:\n📚 Trained on 200,000+ news articles\n🧠 Learned patterns of real vs fake news\n🎯 Predicts new articles with 91.34% accuracy\n\nIt learned by reading thousands of examples — just like a human! 🤖`
            },
            {
                keys: ['what is flask', 'technology used', 'how is website made', 'built with'],
                answer: `<strong>Technologies Used</strong>\n🐍 <b>Python</b> — main programming language\n🌐 <b>Flask</b> — web framework\n🤖 <b>Scikit-learn</b> — ML model\n📊 <b>TF-IDF</b> — text vectorization\n🔍 <b>Tesseract OCR</b> — image analysis\n🎙️ <b>SpeechRecognition</b> — video analysis\n🎨 <b>HTML + CSS + JS</b> — frontend`
            },
            {
                keys: ['tamil', 'hindi', 'regional', 'other language', 'language support'],
                answer: `<strong>Language Support</strong>\nCurrently VeritasAI supports <b>English only</b>.\n\nThis is because the 200,000+ training articles are in English.\n\n🔮 <b>Future upgrade possible!</b>\nWith Tamil/Hindi datasets and retraining, regional language support can be added — a great future enhancement! 🎯`
            },
            {
                keys: ['dataset', 'training data', 'how was it trained', 'isot', 'welfake', 'liar'],
                answer: `<strong>Training Datasets</strong>\nVeritasAI was trained on <b>3 combined datasets</b>:\n\n📁 <b>ISOT</b> — 117,033 articles (2010–2017)\n📁 <b>WELFake</b> — 72,134 articles (up to 2022)\n📁 <b>LIAR</b> — 12,791 articles (up to 2022)\n\nTotal: <b>200,000+ articles</b> across all 8 news categories ✅`
            },
            {
                keys: ['wrong prediction', 'incorrect', 'mistake', 'false positive', 'wrong result', 'error'],
                answer: `<strong>Wrong Predictions</strong>\nNo AI is 100% perfect. VeritasAI has <b>91.34% accuracy</b> — about 1 in 10 may be incorrect.\n\nCommon reasons:\n⚠️ Very short text (under 50 words)\n⚠️ Sarcastic or satirical news\n⚠️ Non-English content\n⚠️ Very recent events\n\n💡 Always verify important news manually! 🎯`
            },
            {
                keys: ['how to improve', 'improve accuracy', 'make better', 'enhance'],
                answer: `<strong>Tips for Best Results</strong>\n✅ Paste <b>full articles</b> not just headlines\n✅ Include at least <b>100+ words</b>\n✅ Use <b>clear screenshots</b> for images\n✅ Ensure <b>clear English speech</b> for video\n✅ Cross-check with trusted news sources\n\n🔮 Future: regional languages + deep learning!`
            },
        ];

        function getBotResponse(input) {
            const lower = input.toLowerCase().trim();
            for (const rule of rules) {
                if (rule.keys.some(k => lower.includes(k))) {
                    return rule.answer;
                }
            }
            // Default fallback
            return `I'm not sure about that specific question. Here are some things I can help with:\n\n• How to use the app\n• Understanding credibility scores\n• What red flags mean\n• How to verify news\n• Supported categories\n\nTry asking one of those! 😊`;
        }

        function toggleChat() {
            chatOpen = !chatOpen;
            const win = document.getElementById('chatWindow');
            win.classList.toggle('open', chatOpen);
            document.getElementById('chatBadge').style.display = 'none';

            if (chatOpen && document.getElementById('chatMessages').children.length === 0) {
                setTimeout(() => addBotMessage(
                    `<strong>Welcome to VeritasBot! 🗞️</strong>\nI'm your fake news detection assistant.\n\nAsk me anything about:\n• How the app works\n• Understanding results\n• News verification tips\n\nOr click a quick reply below! 👇`
                ), 400);
            }
            if (chatOpen) {
                setTimeout(() => document.getElementById('chatInput').focus(), 300);
            }
        }

        function addUserMessage(text) {
            const div = document.createElement('div');
            div.className = 'chat-msg user';
            div.textContent = text;
            document.getElementById('chatMessages').appendChild(div);
            scrollChat();
        }

        function addBotMessage(html) {
            const div = document.createElement('div');
            div.className = 'chat-msg bot';
            div.innerHTML = html.replace(/\n/g, '<br/>');
            document.getElementById('chatMessages').appendChild(div);
            scrollChat();
        }

        function scrollChat() {
            const msgs = document.getElementById('chatMessages');
            msgs.scrollTop = msgs.scrollHeight;
        }

        function showTyping() {
            document.getElementById('typingIndicator').style.display = 'flex';
            scrollChat();
        }

        function hideTyping() {
            document.getElementById('typingIndicator').style.display = 'none';
        }

        function sendQuick(text) {
            addUserMessage(text);
            showTyping();
            setTimeout(() => {
                hideTyping();
                addBotMessage(getBotResponse(text));
            }, 700);
        }

        function sendMessage() {
            const input = document.getElementById('chatInput');
            const text = input.value.trim();
            if (!text) return;
            input.value = '';

            addUserMessage(text);
            showTyping();

            setTimeout(() => {
                hideTyping();
                addBotMessage(getBotResponse(text));
            }, 800);
        }