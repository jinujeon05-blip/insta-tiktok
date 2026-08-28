<!DOCTYPE html>
<html lang="vi">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <title>JS welink - Insta Card News Maker</title>
    <!-- Tailwind CSS CDN -->
    <script src="https://cdn.tailwindcss.com"></script>
    <!-- html2canvas for card image download -->import streamlit as st

# Streamlit 페이지 설정
st.set_page_config(page_title="JS welink - Insta Card News Maker", layout="wide")

# HTML/JS 앱을 Streamlit에 임베디드하기 위한 컴포넌트
html_code = """
<!DOCTYPE html>
<html lang="vi">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <title>JS welink - Insta Card News Maker</title>
    <!-- Tailwind CSS CDN -->
    <script src="https://cdn.tailwindcss.com"></script>
    <!-- html2canvas for card image download -->
    <script src="https://cdnjs.cloudflare.com/ajax/libs/html2canvas/1.4.1/html2canvas.min.js"></script>
</head>
<body class="bg-gray-950 text-gray-100 min-h-screen flex flex-col overflow-x-hidden">

    <!-- 상단 헤더 -->
    <header class="bg-gray-900 border-b border-gray-800 px-4 sm:px-6 py-3 flex flex-wrap justify-between items-center gap-3 shrink-0">
        <h1 class="text-sm sm:text-lg font-bold flex items-center gap-2">
            <span class="w-3 h-3 bg-purple-500 rounded-full inline-block"></span>
            Insta Card News Maker
        </h1>
        <div class="flex items-center gap-2 sm:gap-3">
            <span id="activePlatformBadge" class="text-xs text-purple-300 bg-purple-950/60 border border-purple-800/50 px-2.5 py-1 rounded-full font-medium">Instagram</span>
            <!-- 언어 선택 버튼 (KO/VI) -->
            <div class="flex bg-gray-800 rounded-lg p-0.5 border border-gray-700">
                <button onclick="switchLang('ko')" id="langKo" class="px-2.5 py-1 rounded text-xs font-semibold bg-purple-600 text-white transition">KO</button>
                <button onclick="switchLang('vi')" id="langVi" class="px-2.5 py-1 rounded text-xs font-semibold text-gray-400 hover:text-white transition">VI</button>
            </div>
        </div>
    </header>

    <!-- 플랫폼 탭 네비게이션 바 -->
    <nav class="bg-gray-900/90 border-b border-gray-800 px-4 py-2.5 flex gap-2 overflow-x-auto no-scrollbar shrink-0">
        <button onclick="switchPlatform('instagram')" id="tabInstagram" class="whitespace-nowrap px-3.5 py-2 rounded-lg text-xs sm:text-sm font-semibold bg-purple-600 text-white transition flex items-center gap-2 shadow-lg shadow-purple-900/35">
            Instagram
        </button>
        <button onclick="switchPlatform('tiktok')" id="tabTiktok" class="whitespace-nowrap px-3.5 py-2 rounded-lg text-xs sm:text-sm font-semibold bg-gray-800 text-gray-400 hover:text-white transition flex items-center gap-2">
            TikTok
        </button>
        <button onclick="switchPlatform('facebook')" id="tabFacebook" class="whitespace-nowrap px-3.5 py-2 rounded-lg text-xs sm:text-sm font-semibold bg-gray-800 text-gray-400 hover:text-white transition flex items-center gap-2">
            Facebook
        </button>
    </nav>

    <!-- 메인 레이아웃 -->
    <main class="flex-1 flex flex-col lg:flex-row w-full overflow-y-auto">
        
        <!-- 좌측 패널: 설정 및 업로드 -->
        <aside class="w-full lg:w-96 bg-gray-900 border-b lg:border-b-0 lg:border-r border-gray-800 p-4 sm:p-6 flex flex-col gap-5 shrink-0">
            
            <!-- API 설정 -->
            <div class="flex flex-col gap-1.5">
                <div class="flex justify-between items-center">
                    <label class="text-xs font-semibold text-gray-400 uppercase">API</label>
                    <span class="text-[10px] text-purple-400 cursor-pointer hover:underline" onclick="toggleApiKey()">잠금/해제</span>
                </div>
                <input type="password" id="apiKey" value="" placeholder="API Key를 입력하세요" class="bg-gray-950 border border-gray-800 rounded px-3 py-2 text-sm text-gray-200 focus:outline-none focus:border-purple-500">
            </div>

            <!-- 모델 및 지침 -->
            <div class="flex flex-col gap-4">
                <div class="flex flex-col gap-1.5">
                    <label class="text-xs font-semibold text-gray-400 uppercase">모델</label>
                    <select id="aiModel" class="bg-gray-950 border border-gray-800 rounded px-3 py-2 text-sm text-gray-200 focus:outline-none focus:border-purple-500">
                        <option value="gemini-3.7-flash">3.7 Flash (신규/추천)</option>
                        <option value="gemini-3.5-flash-lite">3.5 Flash-Lite (가장 빠른 답변)</option>
                        <option value="gemini-3.1-pro">3.1 Pro (고급 추론)</option>
                    </select>
                </div>

                <div class="flex flex-col gap-1.5">
                    <label class="text-xs font-semibold text-gray-400 uppercase">지침 (분석 & 번역 공통, 선택)</label>
                    <textarea id="aiPrompt" rows="3" class="bg-gray-950 border border-gray-800 rounded px-3 py-2 text-sm text-gray-200 focus:outline-none focus:border-purple-500">20대들의 언어로 자세하게 이해하기 쉽게해줘</textarea>
                </div>
            </div>

            <hr class="border-gray-800">

            <!-- 인스타그램 원본 업로드 섹션 -->
            <div class="flex flex-col gap-3">
                <label class="text-xs font-semibold text-gray-400 uppercase">인스타그램 원본</label>
                
                <!-- 게시물 이미지 업로드 -->
                <div class="flex flex-col gap-1">
                    <span class="text-[11px] text-gray-400">게시물 이미지</span>
                    <label for="postImageInput" id="postDropZone" class="border border-dashed border-gray-700 bg-gray-950 hover:bg-gray-900 rounded-lg p-3 text-center cursor-pointer transition flex flex-col items-center justify-center gap-1 overflow-hidden relative" style="min-height: 70px;">
                        <span id="postImageLabel" class="text-xs text-gray-400">이미지 업로드</span>
                        <input type="file" id="postImageInput" accept="image/*" class="hidden" onchange="previewImage(this, 'post')">
                    </label>
                </div>

                <!-- 본문 캡처 업로드 -->
                <div class="flex flex-col gap-1">
                    <span class="text-[11px] text-gray-400">본문 캡처</span>
                    <label for="bodyImageInput" id="bodyDropZone" class="border border-dashed border-gray-700 bg-gray-950 hover:bg-gray-900 rounded-lg p-3 text-center cursor-pointer transition flex flex-col items-center justify-center gap-1 overflow-hidden relative" style="min-height: 70px;">
                        <span id="bodyImageLabel" class="text-xs text-gray-400">본문 스크린샷 업로드</span>
                        <input type="file" id="bodyImageInput" accept="image/*" class="hidden" onchange="previewImage(this, 'body')">
                    </label>
                </div>

                <!-- 분석하고 카드 생성 버튼 -->
                <button onclick="generateContent()" class="mt-2 bg-purple-600 hover:bg-purple-500 text-white font-medium py-2.5 px-4 rounded-lg text-sm transition flex items-center justify-center gap-2 shadow-md">
                    분석하고 카드 생성
                </button>
            </div>

            <hr class="border-gray-800">

            <!-- 번역 & 다운로드 섹션 -->
            <div class="flex flex-col gap-3">
                <label class="text-xs font-semibold text-gray-400 uppercase">번역 & 다운로드</label>
                
                <div class="flex flex-col gap-1.5">
                    <span class="text-[11px] text-gray-400">언어</span>
                    <select id="translateLangSelect" class="bg-gray-950 border border-gray-800 rounded px-3 py-2 text-sm text-gray-200 focus:outline-none focus:border-purple-500">
                        <option value="ko">한국어</option>
                        <option value="vi">Tiếng Việt (베트남어)</option>
                        <option value="en">English (영어)</option>
                        <option value="ja">日本語 (일본어)</option>
                    </select>
                </div>

                <div class="grid grid-cols-2 gap-2 mt-1">
                    <button onclick="executeTranslation()" class="bg-gray-800 hover:bg-gray-700 text-gray-200 font-medium py-2.5 px-4 rounded-lg text-sm transition border border-gray-700">
                        번역
                    </button>
                    <button onclick="downloadCard()" class="bg-purple-600 hover:bg-purple-500 text-white font-medium py-2.5 px-4 rounded-lg text-sm transition shadow-md">
                        다운로드
                    </button>
                </div>
            </div>

        </aside>

        <!-- 중앙: 미리보기 영역 -->
        <section class="flex-1 bg-gray-950 p-4 sm:p-6 flex flex-col items-center justify-center gap-5 shrink-0 min-h-[450px]">
            <div id="subOptionBar" class="flex flex-wrap justify-center gap-2 bg-gray-900 p-1.5 rounded-lg border border-gray-800"></div>

            <div class="relative flex items-center justify-center overflow-hidden border border-gray-800 rounded-xl shadow-2xl bg-black transition-all duration-300 max-w-full" style="width: 320px; height: 400px;" id="previewContainer">
                <div id="cardPreview" class="w-full h-full bg-gradient-to-br from-gray-900 via-gray-900 to-purple-950 p-6 sm:p-8 flex flex-col justify-between relative transition-all duration-300">
                    <div class="flex justify-between items-center text-xs text-purple-300 font-medium">
                        <span id="previewBrand">JS welink</span>
                        <span id="cardPlatformIndicator">Instagram</span>
                    </div>
                    <div class="my-auto flex flex-col gap-2.5 text-center">
                        <h2 id="cardTitle" class="text-lg sm:text-xl font-bold text-white leading-snug">플랫폼 맞춤 제목</h2>
                        <p id="cardBody" class="text-xs sm:text-sm text-gray-300 leading-relaxed">이미지를 업로드하거나 텍스트를 입력해 생성해보세요.</p>
                    </div>
                    <div class="flex justify-between items-center text-[10px] sm:text-xs text-gray-500">
                        <span id="cardFooterTag">#JSwelink #Hanoi</span>
                        <span>Swipe -></span>
                    </div>
                </div>
            </div>
        </section>

        <!-- 우측 속성 설정 패널 -->
        <aside class="w-full lg:w-80 bg-gray-900 border-t lg:border-t-0 lg:border-l border-gray-800 p-4 sm:p-6 flex flex-col gap-5 shrink-0 pb-12">
            <h3 class="text-xs font-semibold text-gray-400 uppercase tracking-wider">디자인 및 텍스트 직접 수정</h3>
            <div class="flex flex-col gap-3.5">
                <div class="flex flex-col gap-1.5">
                    <label class="text-xs text-gray-400">브랜드 / 채널명</label>
                    <input type="text" id="inputBrand" value="JS welink" oninput="updateBrand(this.value)" class="bg-gray-950 border border-gray-800 rounded px-3 py-2 text-sm text-gray-200">
                </div>
                <div class="flex flex-col gap-1.5">
                    <label class="text-xs text-gray-400">제목 수정</label>
                    <input type="text" id="inputTitle" placeholder="" oninput="updateTitle(this.value)" class="bg-gray-950 border border-gray-800 rounded px-3 py-2 text-sm text-gray-200">
                </div>
                <div class="flex flex-col gap-1.5">
                    <label class="text-xs text-gray-400">본문 내용 수정</label>
                    <textarea id="inputBodyText" rows="5" placeholder="" oninput="updateBodyText(this.value)" class="bg-gray-950 border border-gray-800 rounded px-3 py-2 text-sm text-gray-200 mt-1"></textarea>
                </div>
                <div class="flex flex-col gap-1.5">
                    <label class="text-xs text-gray-400">하단 해시태그 / 푸터</label>
                    <input type="text" id="inputFooter" value="#JSwelink #Hanoi" oninput="updateFooter(this.value)" class="bg-gray-950 border border-gray-800 rounded px-3 py-2 text-sm text-gray-200">
                </div>
            </div>
        </aside>
    </main>

    <!-- 자바스크립트 로직 -->
    <script>
        let currentLang = 'ko';
        let currentPlatform = 'instagram';
        let uploadedPostImageBase64 = null;
        let uploadedBodyImageBase64 = null;

        const i18n = {
            ko: {
                defaultTitle: '플랫폼 맞춤 제목',
                defaultBody: '이미지를 업로드하거나 내용을 입력하고 생성해보세요.',
                alertApiKey: 'Gemini API Key를 입력해주세요.',
                alertGenerating: '이미지 및 텍스트를 분석 중입니다...',
                alertTranslating: '번역을 진행 중입니다...',
                alertError: 'AI 응답 생성 중 오류가 발생했습니다. API 키를 확인해주세요.',
                prompts: {
                    instagram: '핵심 내용을 20대의 언어로 친근하고 자세하게 인스타그램 카드뉴스 문구로 요약해줘.',
                    tiktok: '시선을 확 사로잡는 훅(Hook)과 함께 틱톡 영상에서 나레이션이나 자막으로 쓸 수 있는 트렌디한 숏폼 대본 스타일로 요약해줘.',
                    facebook: '페이스북 뉴스피드 공유용으로 신뢰감 있고 정보 전달력이 높은 카드뉴스 문구로 요약해줘.'
                },
                subOpts: {
                    instagram: [
                        { id: 'feed', label: '게시물 (1080x1350)', width: '300px', height: '375px' },
                        { id: 'reels', label: '릴스 (1080x1920)', width: '225px', height: '400px' }
                    ],
                    tiktok: [
                        { id: 'vertical', label: '세로형 숏폼 (9:16)', width: '225px', height: '400px' },
                        { id: 'cover', label: '영상 커버 (1080x1440)', width: '300px', height: '400px' }
                    ],
                    facebook: [
                        { id: 'square', label: '정사각형 피드 (1:1)', width: '320px', height: '320px' },
                        { id: 'landscape', label: '와이드 링크카드', width: '360px', height: '200px' }
                    ]
                }
            },
            vi: {
                defaultTitle: 'Tiêu đề phù hợp nền tảng',
                defaultBody: 'Tải lên hình ảnh hoặc nhập nội dung để tạo.',
                alertApiKey: 'Vui lòng nhập Gemini API Key.',
                alertGenerating: 'Đang phân tích hình ảnh và văn bản...',
                alertTranslating: 'Đang dịch...',
                alertError: 'Đã xảy ra lỗi khi tạo phản hồi AI.',
                prompts: {
                    instagram: 'Tóm tắt nội dung chính thành văn bản dạng thẻ Instagram thân thiện, chi tiết và hợp xu hướng.',
                    tiktok: 'Tạo kịch bản video ngắn TikTok với câu mở đầu (Hook) thu hút.',
                    facebook: 'Tóm tắt nội dung thành dạng thẻ tin tức Facebook mang tính thông tin cao.'
                },
                subOpts: {
                    instagram: [
                        { id: 'feed', label: 'Bài đăng (1080x1350)', width: '300px', height: '375px' },
                        { id: 'reels', label: 'Reels (1080x1920)', width: '225px', height: '400px' }
                    ],
                    tiktok: [
                        { id: 'vertical', label: 'Video dọc (9:16)', width: '225px', height: '400px' },
                        { id: 'cover', label: 'Ảnh bìa (1080x1440)', width: '300px', height: '400px' }
                    ],
                    facebook: [
                        { id: 'square', label: 'Feed vuông (1:1)', width: '320px', height: '320px' },
                        { id: 'landscape', label: 'Link rộng', width: '360px', height: '200px' }
                    ]
                }
            }
        };

        const platformThemes = {
            instagram: { class: 'from-gray-900 via-gray-900 to-purple-950', indicator: 'Instagram' },
            tiktok: { class: 'from-gray-950 via-cyan-950/40 to-purple-950/40', indicator: 'TikTok' },
            facebook: { class: 'from-gray-900 via-blue-950/50 to-gray-900', indicator: 'Facebook' }
        };

        function toggleApiKey() {
            const input = document.getElementById('apiKey');
            input.type = input.type === 'password' ? 'text' : 'password';
        }

        function switchLang(lang) {
            currentLang = lang;
            document.getElementById('langKo').className = lang === 'ko' ? 'px-2.5 py-1 rounded text-xs font-semibold bg-purple-600 text-white transition' : 'px-2.5 py-1 rounded text-xs font-semibold text-gray-400 hover:text-white transition';
            document.getElementById('langVi').className = lang === 'vi' ? 'px-2.5 py-1 rounded text-xs font-semibold bg-purple-600 text-white transition' : 'px-2.5 py-1 rounded text-xs font-semibold text-gray-400 hover:text-white transition';

            if(document.getElementById('cardTitle').innerText === i18n[lang === 'ko' ? 'vi' : 'ko'].defaultTitle) {
                document.getElementById('cardTitle').innerText = i18n[lang].defaultTitle;
                document.getElementById('cardBody').innerText = i18n[lang].defaultBody;
            }
            switchPlatform(currentPlatform);
        }

        function switchPlatform(platform) {
            currentPlatform = platform;
            const dict = i18n[currentLang];
            const theme = platformThemes[platform];

            ['instagram', 'tiktok', 'facebook'].forEach(p => {
                const btn = document.getElementById('tab' + p.charAt(0).toUpperCase() + p.slice(1));
                if (p === platform) {
                    btn.className = 'whitespace-nowrap px-3.5 py-2 rounded-lg text-xs sm:text-sm font-semibold bg-purple-600 text-white transition flex items-center gap-2 shadow-lg shadow-purple-900/35';
                } else {
                    btn.className = 'whitespace-nowrap px-3.5 py-2 rounded-lg text-xs sm:text-sm font-semibold bg-gray-800 text-gray-400 hover:text-white transition flex items-center gap-2';
                }
            });

            document.getElementById('activePlatformBadge').innerText = theme.indicator;
            document.getElementById('aiPrompt').value = dict.prompts[platform];
            document.getElementById('cardPlatformIndicator').innerText = theme.indicator;
            document.getElementById('cardPreview').className = `w-full h-full bg-gradient-to-br ${theme.class} p-6 sm:p-8 flex flex-col justify-between relative transition-all duration-300`;

            renderSubOptions(dict.subOpts[platform]);
        }

        function renderSubOptions(options) {
            const bar = document.getElementById('subOptionBar');
            bar.innerHTML = '';
            options.forEach((opt, idx) => {
                const btn = document.createElement('button');
                btn.id = 'subBtn_' + opt.id;
                btn.className = idx === 0 ? 'px-3 py-1.5 rounded text-xs font-medium bg-purple-600 text-white transition whitespace-nowrap' : 'px-3 py-1.5 rounded text-xs font-medium text-gray-400 hover:text-white transition whitespace-nowrap';
                btn.innerText = opt.label;
                btn.onclick = () => setFormat(opt.id, opt.width, opt.height, options);
                bar.appendChild(btn);
            });

            if (options.length > 0) {
                const container = document.getElementById('previewContainer');
                container.style.width = options[0].width;
                container.style.height = options[0].height;
            }
        }

        function setFormat(formatId, width, height, optionsList) {
            const container = document.getElementById('previewContainer');
            container.style.width = width;
            container.style.height = height;

            const currentOptions = optionsList || i18n[currentLang].subOpts[currentPlatform];
            currentOptions.forEach(opt => {
                const btn = document.getElementById('subBtn_' + opt.id);
                if (btn) {
                    btn.className = opt.id === formatId ? 'px-3 py-1.5 rounded text-xs font-medium bg-purple-600 text-white transition whitespace-nowrap' : 'px-3 py-1.5 rounded text-xs font-medium text-gray-400 hover:text-white transition whitespace-nowrap';
                }
            });
        }

        function previewImage(input, type) {
            if (input.files && input.files[0]) {
                const reader = new FileReader();
                reader.onload = function(e) {
                    const dropZone = document.getElementById(type === 'post' ? 'postDropZone' : 'bodyDropZone');
                    if (type === 'post') {
                        uploadedPostImageBase64 = e.target.result.split(',')[1];
                    } else {
                        uploadedBodyImageBase64 = e.target.result.split(',')[1];
                    }
                    dropZone.style.backgroundImage = `url(${e.target.result})`;
                    dropZone.style.backgroundSize = 'cover';
                    dropZone.style.backgroundPosition = 'center';
                    dropZone.innerHTML = `<span class="bg-black/70 text-white text-[10px] px-2 py-0.5 rounded backdrop-blur-sm">변경하려면 클릭</span><input type="file" id="${type}ImageInput" accept="image/*" class="hidden" onchange="previewImage(this, '${type}')">`;
                }
                reader.readAsDataURL(input.files[0]);
            }
        }

        function updateBrand(val) { document.getElementById('previewBrand').innerText = val; }
        function updateTitle(val) { document.getElementById('cardTitle').innerText = val || i18n[currentLang].defaultTitle; }
        function updateBodyText(val) { document.getElementById('cardBody').innerText = val || i18n[currentLang].defaultBody; }
        function updateFooter(val) { document.getElementById('cardFooterTag').innerText = val; }

        async function callGeminiAPIWithRetry(apiKey, initialModelName, payloadParts) {
            const modelsToTry = [initialModelName, 'gemini-3.5-flash-lite', 'gemini-1.5-pro'];
            let lastError = null;

            for (const modelName of modelsToTry) {
                try {
                    const url = `https://generativelanguage.googleapis.com/v1beta/models/${modelName}:generateContent?key=${apiKey}`;
                    const response = await fetch(url, {
                        method: 'POST',
                        headers: { 'content-type': 'application/json' },
                        body: JSON.stringify({
                            contents: [{ parts: payloadParts }],
                            generationConfig: { responseMimeType: "application/json" }
                        })
                    });
                    const data = await response.json();
                    if (data.error) {
                        throw new Error(data.error.message);
                    }
                    return JSON.parse(data.candidates[0].content.parts[0].text);
                } catch (err) {
                    lastError = err;
                    console.warn(`Model ${modelName} failed, trying next...`, err);
                }
            }
            throw lastError || new Error("All models failed due to high demand.");
        }

        async function generateContent() {
            const dict = i18n[currentLang];
            const apiKey = document.getElementById('apiKey').value.trim();
            const prompt = document.getElementById('aiPrompt').value;
            const model = document.getElementById('aiModel').value;

            if (!apiKey) { alert(dict.alertApiKey); return; }

            alert(dict.alertGenerating);

            try {
                let parts = [{ text: `${prompt}\\n\\nReturn JSON format strictly containing keys "title" and "body".` }];
                
                if (uploadedPostImageBase64) {
                    parts.push({ inlineData: { mimeType: "image/jpeg", data: uploadedPostImageBase64 } });
                }
                if (uploadedBodyImageBase64) {
                    parts.push({ inlineData: { mimeType: "image/jpeg", data: uploadedBodyImageBase64 } });
                }

                const result = await callGeminiAPIWithRetry(apiKey, model, parts);

                if (result.title) {
                    document.getElementById('inputTitle').value = result.title;
                    updateTitle(result.title);
                }
                if (result.body) {
                    document.getElementById('inputBodyText').value = result.body;
                    updateBodyText(result.body);
                }
            } catch (error) {
                console.error(error);
                alert(`${dict.alertError} (${error.message || ''})`);
            }
        }

        async function executeTranslation() {
            const dict = i18n[currentLang];
            const apiKey = document.getElementById('apiKey').value.trim();
            const targetLang = document.getElementById('translateLangSelect').value;
            const currentTitle = document.getElementById('inputTitle').value || '';
            const currentBody = document.getElementById('inputBodyText').value || '';
            const model = document.getElementById('aiModel').value;

            if (!apiKey) { alert(dict.alertApiKey); return; }
            if (!currentBody && !currentTitle) { alert('번역할 텍스트가 없습니다.'); return; }

            const langNames = { ko: '한국어(Korean)', vi: 'Tiếng Việt(Vietnamese)', en: 'English(영어)', ja: '日本語(일본어)' };
            alert(`${langNames[targetLang]} (으)로 ${dict.alertTranslating}`);

            try {
                const prompt = `Translate the following title and body into natural, professional ${langNames[targetLang]}. Keep social media style.\\n\\nTitle: ${currentTitle}\\nBody: ${currentBody}\\n\\nReturn JSON format strictly containing keys "title" and "body".`;
                const result = await callGeminiAPIWithRetry(apiKey, model, [{ text: prompt }]);

                if (result.title) {
                    document.getElementById('inputTitle').value = result.title;
                    updateTitle(result.title);
                }
                if (result.body) {
                    document.getElementById('inputBodyText').value = result.body;
                    updateBodyText(result.body);
                }
            } catch (error) {
                console.error(error);
                alert(`${dict.alertError} (${error.message || ''})`);
            }
        }

        function downloadCard() {
            const cardElement = document.getElementById('cardPreview');
            html2canvas(cardElement, { scale: 3 }).then(canvas => {
                const link = document.createElement('a');
                link.download = `${currentPlatform}-content.png`;
                link.href = canvas.toDataURL('image/png');
                link.click();
            });
        }

        window.onload = () => {
            switchLang('ko');
        };
    </script>
</body>
</html>
"""

# Streamlit을 통해 HTML을 화면에 렌더링
st.components.v1.html(html_code, height=900, scrolling=True)
    <script src="https://cdnjs.cloudflare.com/ajax/libs/html2canvas/1.4.1/html2canvas.min.js"></script>
</head>
<body class="bg-gray-950 text-gray-100 min-h-screen flex flex-col overflow-x-hidden">

    <!-- 상단 헤더 -->
    <header class="bg-gray-900 border-b border-gray-800 px-4 sm:px-6 py-3 flex flex-wrap justify-between items-center gap-3 shrink-0">
        <h1 class="text-sm sm:text-lg font-bold flex items-center gap-2">
            <span class="w-3 h-3 bg-purple-500 rounded-full inline-block"></span>
            Insta Card News Maker
        </h1>
        <div class="flex items-center gap-2 sm:gap-3">
            <span id="activePlatformBadge" class="text-xs text-purple-300 bg-purple-950/60 border border-purple-800/50 px-2.5 py-1 rounded-full font-medium">Instagram</span>
            <!-- 언어 선택 버튼 (KO/VI) -->
            <div class="flex bg-gray-800 rounded-lg p-0.5 border border-gray-700">
                <button onclick="switchLang('ko')" id="langKo" class="px-2.5 py-1 rounded text-xs font-semibold bg-purple-600 text-white transition">KO</button>
                <button onclick="switchLang('vi')" id="langVi" class="px-2.5 py-1 rounded text-xs font-semibold text-gray-400 hover:text-white transition">VI</button>
            </div>
        </div>
    </header>

    <!-- 플랫폼 탭 네비게이션 바 -->
    <nav class="bg-gray-900/90 border-b border-gray-800 px-4 py-2.5 flex gap-2 overflow-x-auto no-scrollbar shrink-0">
        <button onclick="switchPlatform('instagram')" id="tabInstagram" class="whitespace-nowrap px-3.5 py-2 rounded-lg text-xs sm:text-sm font-semibold bg-purple-600 text-white transition flex items-center gap-2 shadow-lg shadow-purple-900/35">
            Instagram
        </button>
        <button onclick="switchPlatform('tiktok')" id="tabTiktok" class="whitespace-nowrap px-3.5 py-2 rounded-lg text-xs sm:text-sm font-semibold bg-gray-800 text-gray-400 hover:text-white transition flex items-center gap-2">
            TikTok
        </button>
        <button onclick="switchPlatform('facebook')" id="tabFacebook" class="whitespace-nowrap px-3.5 py-2 rounded-lg text-xs sm:text-sm font-semibold bg-gray-800 text-gray-400 hover:text-white transition flex items-center gap-2">
            Facebook
        </button>
    </nav>

    <!-- 메인 레이아웃 (모바일 전체 스크롤 보장) -->
    <main class="flex-1 flex flex-col lg:flex-row w-full overflow-y-auto">
        
        <!-- 좌측 패널: 설정 및 업로드 -->
        <aside class="w-full lg:w-96 bg-gray-900 border-b lg:border-b-0 lg:border-r border-gray-800 p-4 sm:p-6 flex flex-col gap-5 shrink-0">
            
            <!-- API 설정 (보안을 위해 value는 비워둠) -->
            <div class="flex flex-col gap-1.5">
                <div class="flex justify-between items-center">
                    <label class="text-xs font-semibold text-gray-400 uppercase">API</label>
                    <span class="text-[10px] text-purple-400 cursor-pointer hover:underline" onclick="toggleApiKey()">잠금/해제</span>
                </div>
                <input type="password" id="apiKey" value="" placeholder="API Key를 입력하세요" class="bg-gray-950 border border-gray-800 rounded px-3 py-2 text-sm text-gray-200 focus:outline-none focus:border-purple-500">
            </div>

            <!-- 모델 및 지침 -->
            <div class="flex flex-col gap-4">
                <div class="flex flex-col gap-1.5">
                    <label class="text-xs font-semibold text-gray-400 uppercase">모델</label>
                    <select id="aiModel" class="bg-gray-950 border border-gray-800 rounded px-3 py-2 text-sm text-gray-200 focus:outline-none focus:border-purple-500">
                        <option value="gemini-3.7-flash">3.7 Flash (신규/추천)</option>
                        <option value="gemini-3.5-flash-lite">3.5 Flash-Lite (가장 빠른 답변)</option>
                        <option value="gemini-3.1-pro">3.1 Pro (고급 추론)</option>
                    </select>
                </div>

                <div class="flex flex-col gap-1.5">
                    <label class="text-xs font-semibold text-gray-400 uppercase">지침 (분석 & 번역 공통, 선택)</label>
                    <textarea id="aiPrompt" rows="3" class="bg-gray-950 border border-gray-800 rounded px-3 py-2 text-sm text-gray-200 focus:outline-none focus:border-purple-500">20대들의 언어로 자세하게 이해하기 쉽게해줘</textarea>
                </div>
            </div>

            <hr class="border-gray-800">

            <!-- 인스타그램 원본 업로드 섹션 -->
            <div class="flex flex-col gap-3">
                <label class="text-xs font-semibold text-gray-400 uppercase">인스타그램 원본</label>
                
                <!-- 게시물 이미지 업로드 -->
                <div class="flex flex-col gap-1">
                    <span class="text-[11px] text-gray-400">게시물 이미지</span>
                    <label for="postImageInput" id="postDropZone" class="border border-dashed border-gray-700 bg-gray-950 hover:bg-gray-900 rounded-lg p-3 text-center cursor-pointer transition flex flex-col items-center justify-center gap-1 overflow-hidden relative" style="min-height: 70px;">
                        <span id="postImageLabel" class="text-xs text-gray-400">이미지 업로드</span>
                        <input type="file" id="postImageInput" accept="image/*" class="hidden" onchange="previewImage(this, 'post')">
                    </label>
                </div>

                <!-- 본문 캡처 업로드 -->
                <div class="flex flex-col gap-1">
                    <span class="text-[11px] text-gray-400">본문 캡처</span>
                    <label for="bodyImageInput" id="bodyDropZone" class="border border-dashed border-gray-700 bg-gray-950 hover:bg-gray-900 rounded-lg p-3 text-center cursor-pointer transition flex flex-col items-center justify-center gap-1 overflow-hidden relative" style="min-height: 70px;">
                        <span id="bodyImageLabel" class="text-xs text-gray-400">본문 스크린샷 업로드</span>
                        <input type="file" id="bodyImageInput" accept="image/*" class="hidden" onchange="previewImage(this, 'body')">
                    </label>
                </div>

                <!-- 분석하고 카드 생성 버튼 -->
                <button onclick="generateContent()" class="mt-2 bg-purple-600 hover:bg-purple-500 text-white font-medium py-2.5 px-4 rounded-lg text-sm transition flex items-center justify-center gap-2 shadow-md">
                    분석하고 카드 생성
                </button>
            </div>

            <hr class="border-gray-800">

            <!-- 번역 & 다운로드 섹션 -->
            <div class="flex flex-col gap-3">
                <label class="text-xs font-semibold text-gray-400 uppercase">번역 & 다운로드</label>
                
                <div class="flex flex-col gap-1.5">
                    <span class="text-[11px] text-gray-400">언어</span>
                    <select id="translateLangSelect" class="bg-gray-950 border border-gray-800 rounded px-3 py-2 text-sm text-gray-200 focus:outline-none focus:border-purple-500">
                        <option value="ko">한국어</option>
                        <option value="vi">Tiếng Việt (베트남어)</option>
                        <option value="en">English (영어)</option>
                        <option value="ja">日本語 (일본어)</option>
                    </select>
                </div>

                <div class="grid grid-cols-2 gap-2 mt-1">
                    <button onclick="executeTranslation()" class="bg-gray-800 hover:bg-gray-700 text-gray-200 font-medium py-2.5 px-4 rounded-lg text-sm transition border border-gray-700">
                        번역
                    </button>
                    <button onclick="downloadCard()" class="bg-purple-600 hover:bg-purple-500 text-white font-medium py-2.5 px-4 rounded-lg text-sm transition shadow-md">
                        다운로드
                    </button>
                </div>
            </div>

        </aside>

        <!-- 중앙: 미리보기 영역 -->
        <section class="flex-1 bg-gray-950 p-4 sm:p-6 flex flex-col items-center justify-center gap-5 shrink-0 min-h-[450px]">
            
            <!-- 포맷/서브 옵션 전환 바 -->
            <div id="subOptionBar" class="flex flex-wrap justify-center gap-2 bg-gray-900 p-1.5 rounded-lg border border-gray-800">
                <!-- 동적 생성 -->
            </div>

            <!-- 카드 미리보기 캔버스 컨테이너 -->
            <div class="relative flex items-center justify-center overflow-hidden border border-gray-800 rounded-xl shadow-2xl bg-black transition-all duration-300 max-w-full" style="width: 320px; height: 400px;" id="previewContainer">
                <div id="cardPreview" class="w-full h-full bg-gradient-to-br from-gray-900 via-gray-900 to-purple-950 p-6 sm:p-8 flex flex-col justify-between relative transition-all duration-300">
                    
                    <!-- 상단 브랜드/로고 영역 -->
                    <div class="flex justify-between items-center text-xs text-purple-300 font-medium">
                        <span id="previewBrand">JS welink</span>
                        <span id="cardPlatformIndicator">Instagram</span>
                    </div>

                    <!-- 중앙 텍스트 영역 -->
                    <div class="my-auto flex flex-col gap-2.5 text-center">
                        <h2 id="cardTitle" class="text-lg sm:text-xl font-bold text-white leading-snug">플랫폼 맞춤 제목</h2>
                        <p id="cardBody" class="text-xs sm:text-sm text-gray-300 leading-relaxed">이미지를 업로드하거나 텍스트를 입력해 생성해보세요.</p>
                    </div>

                    <!-- 하단 푸터 -->
                    <div class="flex justify-between items-center text-[10px] sm:text-xs text-gray-500">
                        <span id="cardFooterTag">#JSwelink #Hanoi</span>
                        <span>Swipe ➔</span>
                    </div>
                </div>
            </div>

        </section>

        <!-- 우측 속성 설정 패널 -->
        <aside class="w-full lg:w-80 bg-gray-900 border-t lg:border-t-0 lg:border-l border-gray-800 p-4 sm:p-6 flex flex-col gap-5 shrink-0 pb-12">
            <h3 class="text-xs font-semibold text-gray-400 uppercase tracking-wider">디자인 및 텍스트 직접 수정</h3>
            
            <div class="flex flex-col gap-3.5">
                <div class="flex flex-col gap-1.5">
                    <label class="text-xs text-gray-400">브랜드 / 채널명</label>
                    <input type="text" id="inputBrand" value="JS welink" oninput="updateBrand(this.value)" class="bg-gray-950 border border-gray-800 rounded px-3 py-2 text-sm text-gray-200">
                </div>

                <div class="flex flex-col gap-1.5">
                    <label class="text-xs text-gray-400">제목 수정</label>
                    <input type="text" id="inputTitle" placeholder="" oninput="updateTitle(this.value)" class="bg-gray-950 border border-gray-800 rounded px-3 py-2 text-sm text-gray-200">
                </div>

                <div class="flex flex-col gap-1.5">
                    <label class="text-xs text-gray-400">본문 내용 수정</label>
                    <textarea id="inputBodyText" rows="5" placeholder="" oninput="updateBodyText(this.value)" class="bg-gray-950 border border-gray-800 rounded px-3 py-2 text-sm text-gray-200 mt-1"></textarea>
                </div>

                <div class="flex flex-col gap-1.5">
                    <label class="text-xs text-gray-400">하단 해시태그 / 푸터</label>
                    <input type="text" id="inputFooter" value="#JSwelink #Hanoi" oninput="updateFooter(this.value)" class="bg-gray-950 border border-gray-800 rounded px-3 py-2 text-sm text-gray-200">
                </div>
            </div>
        </aside>

    </main>

    <!-- 자바스크립트 로직 -->
    <script>
        let currentLang = 'ko';
        let currentPlatform = 'instagram';
        let uploadedPostImageBase64 = null;
        let uploadedBodyImageBase64 = null;

        const i18n = {
            ko: {
                defaultTitle: '플랫폼 맞춤 제목',
                defaultBody: '이미지를 업로드하거나 내용을 입력하고 생성해보세요.',
                alertApiKey: 'Gemini API Key를 입력해주세요.',
                alertGenerating: '이미지 및 텍스트를 분석 중입니다...',
                alertTranslating: '번역을 진행 중입니다...',
                alertError: 'AI 응답 생성 중 오류가 발생했습니다. API 키를 확인해주세요.',
                prompts: {
                    instagram: '핵심 내용을 20대의 언어로 친근하고 자세하게 인스타그램 카드뉴스 문구로 요약해줘.',
                    tiktok: '시선을 확 사로잡는 훅(Hook)과 함께 틱톡 영상에서 나레이션이나 자막으로 쓸 수 있는 트렌디한 숏폼 대본 스타일로 요약해줘.',
                    facebook: '페이스북 뉴스피드 공유용으로 신뢰감 있고 정보 전달력이 높은 카드뉴스 문구로 요약해줘.'
                },
                subOpts: {
                    instagram: [
                        { id: 'feed', label: '게시물 (1080x1350)', width: '300px', height: '375px' },
                        { id: 'reels', label: '릴스 (1080x1920)', width: '225px', height: '400px' }
                    ],
                    tiktok: [
                        { id: 'vertical', label: '세로형 숏폼 (9:16)', width: '225px', height: '400px' },
                        { id: 'cover', label: '영상 커버 (1080x1440)', width: '300px', height: '400px' }
                    ],
                    facebook: [
                        { id: 'square', label: '정사각형 피드 (1:1)', width: '320px', height: '320px' },
                        { id: 'landscape', label: '와이드 링크카드', width: '360px', height: '200px' }
                    ]
                }
            },
            vi: {
                defaultTitle: 'Tiêu đề phù hợp nền tảng',
                defaultBody: 'Tải lên hình ảnh hoặc nhập nội dung để tạo.',
                alertApiKey: 'Vui lòng nhập Gemini API Key.',
                alertGenerating: 'Đang phân tích hình ảnh và văn bản...',
                alertTranslating: 'Đang dịch...',
                alertError: 'Đã xảy ra lỗi khi tạo phản hồi AI.',
                prompts: {
                    instagram: 'Tóm tắt nội dung chính thành văn bản dạng thẻ Instagram thân thiện, chi tiết và hợp xu hướng.',
                    tiktok: 'Tạo kịch bản video ngắn TikTok với câu mở đầu (Hook) thu hút.',
                    facebook: 'Tóm tắt nội dung thành dạng thẻ tin tức Facebook mang tính thông tin cao.'
                },
                subOpts: {
                    instagram: [
                        { id: 'feed', label: 'Bài đăng (1080x1350)', width: '300px', height: '375px' },
                        { id: 'reels', label: 'Reels (1080x1920)', width: '225px', height: '400px' }
                    ],
                    tiktok: [
                        { id: 'vertical', label: 'Video dọc (9:16)', width: '225px', height: '400px' },
                        { id: 'cover', label: 'Ảnh bìa (1080x1440)', width: '300px', height: '400px' }
                    ],
                    facebook: [
                        { id: 'square', label: 'Feed vuông (1:1)', width: '320px', height: '320px' },
                        { id: 'landscape', label: 'Link rộng', width: '360px', height: '200px' }
                    ]
                }
            }
        };

        const platformThemes = {
            instagram: { class: 'from-gray-900 via-gray-900 to-purple-950', indicator: 'Instagram' },
            tiktok: { class: 'from-gray-950 via-cyan-950/40 to-purple-950/40', indicator: 'TikTok' },
            facebook: { class: 'from-gray-900 via-blue-950/50 to-gray-900', indicator: 'Facebook' }
        };

        function toggleApiKey() {
            const input = document.getElementById('apiKey');
            input.type = input.type === 'password' ? 'text' : 'password';
        }

        function switchLang(lang) {
            currentLang = lang;
            document.getElementById('langKo').className = lang === 'ko' ? 'px-2.5 py-1 rounded text-xs font-semibold bg-purple-600 text-white transition' : 'px-2.5 py-1 rounded text-xs font-semibold text-gray-400 hover:text-white transition';
            document.getElementById('langVi').className = lang === 'vi' ? 'px-2.5 py-1 rounded text-xs font-semibold bg-purple-600 text-white transition' : 'px-2.5 py-1 rounded text-xs font-semibold text-gray-400 hover:text-white transition';

            if(document.getElementById('cardTitle').innerText === i18n[lang === 'ko' ? 'vi' : 'ko'].defaultTitle) {
                document.getElementById('cardTitle').innerText = i18n[lang].defaultTitle;
                document.getElementById('cardBody').innerText = i18n[lang].defaultBody;
            }
            switchPlatform(currentPlatform);
        }

        function switchPlatform(platform) {
            currentPlatform = platform;
            const dict = i18n[currentLang];
            const theme = platformThemes[platform];

            ['instagram', 'tiktok', 'facebook'].forEach(p => {
                const btn = document.getElementById('tab' + p.charAt(0).toUpperCase() + p.slice(1));
                if (p === platform) {
                    btn.className = 'whitespace-nowrap px-3.5 py-2 rounded-lg text-xs sm:text-sm font-semibold bg-purple-600 text-white transition flex items-center gap-2 shadow-lg shadow-purple-900/35';
                } else {
                    btn.className = 'whitespace-nowrap px-3.5 py-2 rounded-lg text-xs sm:text-sm font-semibold bg-gray-800 text-gray-400 hover:text-white transition flex items-center gap-2';
                }
            });

            document.getElementById('activePlatformBadge').innerText = theme.indicator;
            document.getElementById('aiPrompt').value = dict.prompts[platform];
            document.getElementById('cardPlatformIndicator').innerText = theme.indicator;
            document.getElementById('cardPreview').className = `w-full h-full bg-gradient-to-br ${theme.class} p-6 sm:p-8 flex flex-col justify-between relative transition-all duration-300`;

            renderSubOptions(dict.subOpts[platform]);
        }

        function renderSubOptions(options) {
            const bar = document.getElementById('subOptionBar');
            bar.innerHTML = '';
            options.forEach((opt, idx) => {
                const btn = document.createElement('button');
                btn.id = 'subBtn_' + opt.id;
                btn.className = idx === 0 ? 'px-3 py-1.5 rounded text-xs font-medium bg-purple-600 text-white transition whitespace-nowrap' : 'px-3 py-1.5 rounded text-xs font-medium text-gray-400 hover:text-white transition whitespace-nowrap';
                btn.innerText = opt.label;
                btn.onclick = () => setFormat(opt.id, opt.width, opt.height, options);
                bar.appendChild(btn);
            });

            if (options.length > 0) {
                const container = document.getElementById('previewContainer');
                container.style.width = options[0].width;
                container.style.height = options[0].height;
            }
        }

        function setFormat(formatId, width, height, optionsList) {
            const container = document.getElementById('previewContainer');
            container.style.width = width;
            container.style.height = height;

            const currentOptions = optionsList || i18n[currentLang].subOpts[currentPlatform];
            currentOptions.forEach(opt => {
                const btn = document.getElementById('subBtn_' + opt.id);
                if (btn) {
                    btn.className = opt.id === formatId ? 'px-3 py-1.5 rounded text-xs font-medium bg-purple-600 text-white transition whitespace-nowrap' : 'px-3 py-1.5 rounded text-xs font-medium text-gray-400 hover:text-white transition whitespace-nowrap';
                }
            });
        }

        function previewImage(input, type) {
            if (input.files && input.files[0]) {
                const reader = new FileReader();
                reader.onload = function(e) {
                    const dropZone = document.getElementById(type === 'post' ? 'postDropZone' : 'bodyDropZone');
                    if (type === 'post') {
                        uploadedPostImageBase64 = e.target.result.split(',')[1];
                    } else {
                        uploadedBodyImageBase64 = e.target.result.split(',')[1];
                    }
                    dropZone.style.backgroundImage = `url(${e.target.result})`;
                    dropZone.style.backgroundSize = 'cover';
                    dropZone.style.backgroundPosition = 'center';
                    dropZone.innerHTML = `<span class="bg-black/70 text-white text-[10px] px-2 py-0.5 rounded backdrop-blur-sm">변경하려면 클릭</span><input type="file" id="${type}ImageInput" accept="image/*" class="hidden" onchange="previewImage(this, '${type}')">`;
                }
                reader.readAsDataURL(input.files[0]);
            }
        }

        function updateBrand(val) { document.getElementById('previewBrand').innerText = val; }
        function updateTitle(val) { document.getElementById('cardTitle').innerText = val || i18n[currentLang].defaultTitle; }
        function updateBodyText(val) { document.getElementById('cardBody').innerText = val || i18n[currentLang].defaultBody; }
        function updateFooter(val) { document.getElementById('cardFooterTag').innerText = val; }

        async function callGeminiAPIWithRetry(apiKey, initialModelName, payloadParts) {
            const modelsToTry = [initialModelName, 'gemini-3.5-flash-lite', 'gemini-1.5-pro'];
            let lastError = null;

            for (const modelName of modelsToTry) {
                try {
                    const url = `https://generativelanguage.googleapis.com/v1beta/models/${modelName}:generateContent?key=${apiKey}`;
                    const response = await fetch(url, {
                        method: 'POST',
                        headers: { 'content-type': 'application/json' },
                        body: JSON.stringify({
                            contents: [{ parts: payloadParts }],
                            generationConfig: { responseMimeType: "application/json" }
                        })
                    });
                    const data = await response.json();
                    if (data.error) {
                        throw new Error(data.error.message);
                    }
                    return JSON.parse(data.candidates[0].content.parts[0].text);
                } catch (err) {
                    lastError = err;
                    console.warn(`Model ${modelName} failed, trying next...`, err);
                }
            }
            throw lastError || new Error("All models failed due to high demand.");
        }

        async function generateContent() {
            const dict = i18n[currentLang];
            const apiKey = document.getElementById('apiKey').value.trim();
            const prompt = document.getElementById('aiPrompt').value;
            const model = document.getElementById('aiModel').value;

            if (!apiKey) { alert(dict.alertApiKey); return; }

            alert(dict.alertGenerating);

            try {
                let parts = [{ text: `${prompt}\n\nReturn JSON format strictly containing keys "title" and "body".` }];
                
                if (uploadedPostImageBase64) {
                    parts.push({ inlineData: { mimeType: "image/jpeg", data: uploadedPostImageBase64 } });
                }
                if (uploadedBodyImageBase64) {
                    parts.push({ inlineData: { mimeType: "image/jpeg", data: uploadedBodyImageBase64 } });
                }

                const result = await callGeminiAPIWithRetry(apiKey, model, parts);

                if (result.title) {
                    document.getElementById('inputTitle').value = result.title;
                    updateTitle(result.title);
                }
                if (result.body) {
                    document.getElementById('inputBodyText').value = result.body;
                    updateBodyText(result.body);
                }
            } catch (error) {
                console.error(error);
                alert(`${dict.alertError} (${error.message || ''})`);
            }
        }

        async function executeTranslation() {
            const dict = i18n[currentLang];
            const apiKey = document.getElementById('apiKey').value.trim();
            const targetLang = document.getElementById('translateLangSelect').value;
            const currentTitle = document.getElementById('inputTitle').value || '';
            const currentBody = document.getElementById('inputBodyText').value || '';
            const model = document.getElementById('aiModel').value;

            if (!apiKey) { alert(dict.alertApiKey); return; }
            if (!currentBody && !currentTitle) { alert('번역할 텍스트가 없습니다.'); return; }

            const langNames = { ko: '한국어(Korean)', vi: 'Tiếng Việt(Vietnamese)', en: 'English(영어)', ja: '日本語(일본어)' };
            alert(`${langNames[targetLang]} (으)로 ${dict.alertTranslating}`);

            try {
                const prompt = `Translate the following title and body into natural, professional ${langNames[targetLang]}. Keep social media style.\n\nTitle: ${currentTitle}\nBody: ${currentBody}\n\nReturn JSON format strictly containing keys "title" and "body".`;
                const result = await callGeminiAPIWithRetry(apiKey, model, [{ text: prompt }]);

                if (result.title) {
                    document.getElementById('inputTitle').value = result.title;
                    updateTitle(result.title);
                }
                if (result.body) {
                    document.getElementById('inputBodyText').value = result.body;
                    updateBodyText(result.body);
                }
            } catch (error) {
                console.error(error);
                alert(`${dict.alertError} (${error.message || ''})`);
            }
        }

        function downloadCard() {
            const cardElement = document.getElementById('cardPreview');
            html2canvas(cardElement, { scale: 3 }).then(canvas => {
                const link = document.createElement('a');
                link.download = `${currentPlatform}-content.png`;
                link.href = canvas.toDataURL('image/png');
                link.click();
            });
        }

        window.onload = () => {
            switchLang('ko');
        };
    </script>
</body>
</html>
