let currentTab = 'text';
        let selectedFiles = { image: null, video: null };

        // Status check
        window.addEventListener('load', async () => {
            try {
                const res = await fetch('/status');
                const data = await res.json();
                document.getElementById('mlDot').className = 'dot ' + (data.ml_model ? 'on' : 'off');
                document.getElementById('mlLabel').textContent = 'ML Engine: ' + (data.ml_model ? 'Online ●' : 'Offline ✕');
                document.getElementById('ocrDot').className = 'dot ' + (data.ocr ? 'on' : 'off');
                document.getElementById('ocrLabel').textContent = 'OCR: ' + (data.ocr ? 'Online ●' : 'Offline ✕');
            } catch (e) { }
        });

        function switchTab(tab, btn) {
            currentTab = tab;
            document.querySelectorAll('.tab-btn').forEach(b => b.classList.remove('active'));
            btn.classList.add('active');
            document.getElementById('text-section').style.display = tab === 'text' ? 'block' : 'none';
            document.getElementById('image-section').style.display = tab === 'image' ? 'block' : 'none';
            document.getElementById('video-section').style.display = tab === 'video' ? 'block' : 'none';
            hideError();
        }

        function updateCount() {
            document.getElementById('charCount').textContent = document.getElementById('newsText').value.length + ' chars';
        }

        function dragOver(e, zoneId) {
            e.preventDefault();
            document.getElementById(zoneId).classList.add('dragover');
        }

        function dragLeave(zoneId) {
            document.getElementById(zoneId).classList.remove('dragover');
        }

        function dropFile(e, type) {
            e.preventDefault();
            const zoneId = type + 'Zone';
            document.getElementById(zoneId).classList.remove('dragover');
            const file = e.dataTransfer.files[0];
            if (file) {
                const input = document.getElementById(type + 'File');
                const dt = new DataTransfer();
                dt.items.add(file);
                input.files = dt.files;
                fileSelected(type);
            }
        }

        function fileSelected(type) {
            const input = document.getElementById(type + 'File');
            const file = input.files[0];
            if (!file) return;

            selectedFiles[type] = file;
            const size = (file.size / 1024 / 1024).toFixed(2) + ' MB';

            document.getElementById(type + 'Name').textContent = file.name;
            document.getElementById(type + 'Size').textContent = size;
            document.getElementById(type + 'Preview').classList.add('show');

            if (type === 'image') {
                const reader = new FileReader();
                reader.onload = e => {
                    const img = document.getElementById('imgPreview');
                    img.src = e.target.result;
                    img.classList.add('show');
                };
                reader.readAsDataURL(file);
            }
        }

        function removeFile(type) {
            selectedFiles[type] = null;
            document.getElementById(type + 'File').value = '';
            document.getElementById(type + 'Preview').classList.remove('show');
            if (type === 'image') {
                const img = document.getElementById('imgPreview');
                img.src = ''; img.classList.remove('show');
            }
        }

        function showError(msg) {
            const b = document.getElementById('errorBox');
            b.textContent = '⚠ ERROR: ' + msg;
            b.style.display = 'block';
        }
        function hideError() { document.getElementById('errorBox').style.display = 'none'; }

        async function analyze() {
            hideError();
            document.getElementById('extractedBox').style.display = 'none';
            const btn = document.getElementById('analyzeBtn');
            const loading = document.getElementById('loading');

            // Validate input
            if (currentTab === 'text') {
                const content = document.getElementById('newsText').value.trim();
                if (!content || content.length < 20) { showError('Please provide at least 20 characters.'); return; }
            } else if (currentTab === 'image') {
                if (!selectedFiles.image) { showError('Please select an image file.'); return; }
            } else if (currentTab === 'video') {
                if (!selectedFiles.video) { showError('Please select a video file.'); return; }
            }

            btn.disabled = true;
            document.getElementById('results').style.display = 'none';
            loading.style.display = 'block';

            // Loading messages by type
            if (currentTab === 'image') {
                document.getElementById('loadingTitle').textContent = 'Extracting Text from Image';
                document.getElementById('loadingMsg').textContent = 'Running OCR analysis...';
            } else if (currentTab === 'video') {
                document.getElementById('loadingTitle').textContent = 'Processing Video';
                document.getElementById('loadingMsg').textContent = 'Extracting speech from audio...';
                setTimeout(() => { document.getElementById('loadingMsg').textContent = 'Converting speech to text...'; }, 3000);
                setTimeout(() => { document.getElementById('loadingMsg').textContent = 'Running ML analysis...'; }, 7000);
            } else {
                document.getElementById('loadingTitle').textContent = 'Verifying Content';
                document.getElementById('loadingMsg').textContent = 'Running ML model analysis...';
            }

            try {
                const formData = new FormData();
                formData.append('type', currentTab);

                if (currentTab === 'text') {
                    formData.append('content', document.getElementById('newsText').value.trim());
                } else if (currentTab === 'image') {
                    formData.append('file', selectedFiles.image);
                } else if (currentTab === 'video') {
                    formData.append('file', selectedFiles.video);
                }

                const res = await fetch('/analyze', { method: 'POST', body: formData });
                const data = await res.json();

                loading.style.display = 'none';
                btn.disabled = false;

                if (!data.success) { showError(data.error || 'Analysis failed.'); return; }

                // Show extracted text if from image/video
                if (data.result.extracted_text) {
                    document.getElementById('extractedBox').style.display = 'block';
                    document.getElementById('extractedText').textContent =
                        (data.result.extracted_from || 'Extracted text') + ':\n\n"' + data.result.extracted_text + '"';
                }

                showResults(data.result);

            } catch (e) {
                loading.style.display = 'none';
                btn.disabled = false;
                showError('Cannot connect to server. Ensure app.py is running.');
            }
        }

        function showResults(r) {
            const results = document.getElementById('results');
            results.style.display = 'block';

            const banner = document.getElementById('verdictBanner');
            const flag = document.getElementById('verdictFlag');
            banner.className = 'verdict-banner';

            if (r.verdict === 'FAKE NEWS') {
                banner.classList.add('fake'); flag.className = 'verdict-flag fake';
                document.getElementById('vIcon').textContent = '✕';
                document.getElementById('vHeadline').textContent = 'FAKE NEWS DETECTED';
                document.getElementById('vSub').textContent = 'Confidence: ' + r.confidence + ' — This content contains indicators of misinformation.';
            } else if (r.verdict === 'REAL NEWS') {
                banner.classList.add('real'); flag.className = 'verdict-flag real';
                document.getElementById('vIcon').textContent = '✓';
                document.getElementById('vHeadline').textContent = 'CREDIBLE NEWS';
                document.getElementById('vSub').textContent = 'Confidence: ' + r.confidence + ' — This content appears to be factual and credible.';
            } else {
                banner.classList.add('unsure'); flag.className = 'verdict-flag unsure';
                document.getElementById('vIcon').textContent = '?';
                document.getElementById('vHeadline').textContent = 'UNCERTAIN';
                document.getElementById('vSub').textContent = 'Confidence: ' + r.confidence + ' — Manual verification recommended.';
            }



            setScore('finalScore', 'finalFill', r.credibility_score);
            setScore('mlConf', 'mlConfFill', r.ml_confidence_pct || r.confidence_pct || 0);

            setTimeout(() => {
                document.getElementById('realBar').style.width = r.real_probability + '%';
                document.getElementById('realPct').textContent = r.real_probability + '%';
                document.getElementById('fakeBar').style.width = r.fake_probability + '%';
                document.getElementById('fakePct').textContent = r.fake_probability + '%';
            }, 120);

            document.getElementById('reasoning').textContent = r.reasoning || '—';
            document.getElementById('tipText').textContent = r.tips || '—';

            const list = document.getElementById('redFlags');
            list.innerHTML = '';
            if (r.red_flags && r.red_flags.length > 0) {
                r.red_flags.forEach(f => {
                    const li = document.createElement('li');
                    li.innerHTML = '<span class="flag-bullet">▸</span>' + f;
                    list.appendChild(li);
                });
            } else {
                list.innerHTML = '<p class="no-flags">No significant red flags detected.</p>';
            }

            results.scrollIntoView({ behavior: 'smooth', block: 'start' });
        }

        function setScore(numId, fillId, score) {
            document.getElementById(numId).textContent = score + (score > 1 ? '/100' : '%');
            setTimeout(() => {
                const fill = document.getElementById(fillId);
                const val = score > 1 ? score : score * 100;
                fill.style.width = val + '%';
                fill.style.background = val >= 65 ? 'var(--real)' : val >= 40 ? 'var(--unsure)' : 'var(--fake)';
            }, 120);
        }

        function resetForm() {
            document.getElementById('results').style.display = 'none';
            document.getElementById('extractedBox').style.display = 'none';
            document.getElementById('newsText').value = '';
            document.getElementById('charCount').textContent = '0 chars';
            removeFile('image');
            removeFile('video');
            hideError();
            window.scrollTo({ top: 0, behavior: 'smooth' });
        }