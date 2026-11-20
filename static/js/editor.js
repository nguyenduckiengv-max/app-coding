// ==================== MONACO EDITOR & DRAGON JUDGE CLIENT ====================

let monacoEditor = null;
let currentLanguage = 'python3';
const problemMetaEl = document.getElementById('problemMeta');
const problemId = problemMetaEl ? problemMetaEl.getAttribute('data-id') : '';
const initialHasSubmitted = problemMetaEl ? (problemMetaEl.getAttribute('data-has-submitted') === 'true') : false;

let isSolutionUnlocked = initialHasSubmitted;

// Doc starter code tu the json nhung
let starterTemplates = {
    python3: '',
    c: ''
};

try {
    const pyEl = document.getElementById('pythonStarterJSON');
    const cEl = document.getElementById('cStarterJSON');
    if (pyEl) starterTemplates.python3 = JSON.parse(pyEl.textContent);
    if (cEl) starterTemplates.c = JSON.parse(cEl.textContent);
} catch (e) {
    console.warn("Lỗi đọc starter template:", e);
}

// Khoi tao Monaco Editor qua requirejs
require.config({ paths: { vs: 'https://cdnjs.cloudflare.com/ajax/libs/monaco-editor/0.45.0/min/vs' } });

require(['vs/editor/editor.main'], function () {
    const isDark = document.documentElement.classList.contains('dark');
    const container = document.getElementById('monacoEditorContainer');
    const loadingEl = document.getElementById('editorLoading');

    // Su dung key prefix v2 de tranh cache nham dap an cu da luu truoc do
    const savedCodeKey = `dragon_v2_code_${problemId}_${currentLanguage}`;
    const initialCode = localStorage.getItem(savedCodeKey) || starterTemplates[currentLanguage] || '';

    monacoEditor = monaco.editor.create(container, {
        value: initialCode,
        language: currentLanguage === 'python3' ? 'python' : 'c',
        theme: isDark ? 'vs-dark' : 'vs',
        automaticLayout: true,
        fontSize: 14,
        fontFamily: '"JetBrains Mono", "Fira Code", Consolas, "Courier New", monospace',
        fontLigatures: true,
        minimap: { enabled: false },
        scrollBeyondLastLine: false,
        lineNumbers: 'on',
        tabSize: 4,
        insertSpaces: true,
        wordWrap: 'on',
        renderWhitespace: 'selection',
        scrollbar: {
            verticalScrollbarSize: 8,
            horizontalScrollbarSize: 8
        }
    });

    if (loadingEl) loadingEl.style.display = 'none';

    // Tu dong luu code nguoi dung vao localStorage khi go
    monacoEditor.onDidChangeModelContent(() => {
        const code = monacoEditor.getValue();
        localStorage.setItem(`dragon_v2_code_${problemId}_${currentLanguage}`, code);
    });

    // Phim tat: Ctrl+Enter (Run), Ctrl+Alt+Enter (Submit)
    monacoEditor.addCommand(monaco.KeyMod.CtrlCmd | monaco.KeyCode.Enter, function () {
        handleRunCode();
    });

    monacoEditor.addCommand(monaco.KeyMod.CtrlCmd | monaco.KeyMod.Alt | monaco.KeyCode.Enter, function () {
        handleSubmitCode();
    });
});

// Chuyen doi ngon ngu lap trinh (Python 3 / C)
function onLanguageChange() {
    const select = document.getElementById('langSelect');
    const newLang = select.value;
    currentLanguage = newLang;

    if (!monacoEditor) return;

    const savedCodeKey = `dragon_v2_code_${problemId}_${currentLanguage}`;
    const codeToSet = localStorage.getItem(savedCodeKey) || starterTemplates[currentLanguage] || '';

    const monacoLang = (currentLanguage === 'python3') ? 'python' : 'c';
    monaco.editor.setModelLanguage(monacoEditor.getModel(), monacoLang);
    monacoEditor.setValue(codeToSet);
}

// Khoi phuc starter code ban dau (khung skeleton rỗng)
function resetStarterCode() {
    if (!monacoEditor) return;
    if (confirm("Khôi phục khung sườn mã nguồn ban đầu của bài toán? Mọi chỉnh sửa chưa lưu sẽ bị ghi đè.")) {
        const starter = starterTemplates[currentLanguage] || '';
        monacoEditor.setValue(starter);
        localStorage.setItem(`dragon_v2_code_${problemId}_${currentLanguage}`, starter);
    }
}

// Nạp code giải mẫu vào Editor
function applySolutionToEditor(lang) {
    if (!monacoEditor) return;
    if (confirm(`Bạn có muốn nạp mã nguồn giải mẫu (${lang.toUpperCase()}) vào Code Editor để chạy thử và kiểm nghiệm?`)) {
        let code = '';
        if (lang === 'python3') {
            const pyCodeEl = document.getElementById('pythonSolutionCode');
            code = pyCodeEl ? pyCodeEl.innerText : '';
            document.getElementById('langSelect').value = 'python3';
            currentLanguage = 'python3';
            monaco.editor.setModelLanguage(monacoEditor.getModel(), 'python');
        } else {
            const cCodeEl = document.getElementById('cSolutionCode');
            code = cCodeEl ? cCodeEl.innerText : '';
            document.getElementById('langSelect').value = 'c';
            currentLanguage = 'c';
            monaco.editor.setModelLanguage(monacoEditor.getModel(), 'c');
        }
        monacoEditor.setValue(code);
        localStorage.setItem(`dragon_v2_code_${problemId}_${currentLanguage}`, code);
        alert(`Đã nạp lời giải ${lang} vào Code Editor!`);
    }
}

// Sao chep code trong editor vao clipboard
function copyCode() {
    if (!monacoEditor) return;
    const text = monacoEditor.getValue();
    navigator.clipboard.writeText(text).then(() => {
        alert("Đã sao chép mã nguồn vào clipboard!");
    });
}

// Chuyen doi Tab ben cot trai (De bai / Lich su / Goi y / Solution)
function switchLeftTab(tabName) {
    document.querySelectorAll('.left-tab-btn').forEach(btn => {
        btn.classList.remove('active', 'border-dragon-500', 'text-dragon-500', 'border-emerald-500', 'text-emerald-400');
        btn.classList.add('border-transparent', 'text-gray-400');
    });

    document.getElementById('tabDescContent').classList.add('hidden');
    document.getElementById('tabSubContent').classList.add('hidden');
    document.getElementById('tabHintContent').classList.add('hidden');
    document.getElementById('tabSolutionContent').classList.add('hidden');

    if (tabName === 'desc') {
        const b = document.getElementById('tabDescBtn');
        b.classList.add('active', 'border-dragon-500', 'text-dragon-500');
        b.classList.remove('border-transparent', 'text-gray-400');
        document.getElementById('tabDescContent').classList.remove('hidden');
    } else if (tabName === 'sub') {
        const b = document.getElementById('tabSubBtn');
        b.classList.add('active', 'border-dragon-500', 'text-dragon-500');
        b.classList.remove('border-transparent', 'text-gray-400');
        document.getElementById('tabSubContent').classList.remove('hidden');
        reloadSubmissions();
    } else if (tabName === 'hint') {
        const b = document.getElementById('tabHintBtn');
        b.classList.add('active', 'border-dragon-500', 'text-dragon-500');
        b.classList.remove('border-transparent', 'text-gray-400');
        document.getElementById('tabHintContent').classList.remove('hidden');
    } else if (tabName === 'solution') {
        const b = document.getElementById('tabSolutionBtn');
        b.classList.add('active', 'border-emerald-500', 'text-emerald-400');
        b.classList.remove('border-transparent', 'text-gray-400');
        document.getElementById('tabSolutionContent').classList.remove('hidden');
        
        // Neu da submit it nhat 1 lan thi tu dong mo khoa
        if (isSolutionUnlocked) {
            unlockSolution(false);
        }
    }
    lucide.createIcons();
    if (typeof window.triggerKaTeX === 'function') {
        setTimeout(window.triggerKaTeX, 50);
    }
}

// Mo khoa Lời Giải (Solution)
function unlockSolution(manual = false) {
    if (manual) {
        if (!confirm("Bạn có chắc chắn muốn xem lời giải không? Lời khuyên là hãy tự suy nghĩ và thử nộp bài ít nhất một lần để hiểu sâu bài toán!")) {
            return;
        }
    }
    isSolutionUnlocked = true;
    const gate = document.getElementById('solutionLockGate');
    const area = document.getElementById('solutionUnlockedArea');
    if (gate) gate.classList.add('hidden');
    if (area) area.classList.remove('hidden');
    lucide.createIcons();
    if (typeof window.triggerKaTeX === 'function') {
        setTimeout(window.triggerKaTeX, 50);
    }
}

// Chuyen doi Tab trong Console Drawer duoi Editor
function switchConsoleTab(tabKey) {
    document.querySelectorAll('.console-tab-btn').forEach(btn => {
        btn.classList.remove('active', 'text-gray-200', 'bg-darkbg-700');
        btn.classList.add('text-gray-400');
    });

    document.getElementById('panelCustomInput').classList.add('hidden');
    document.getElementById('panelRunOutput').classList.add('hidden');
    document.getElementById('panelSubmitResult').classList.add('hidden');

    if (tabKey === 'custom') {
        const b = document.getElementById('tabCustomInputBtn');
        b.classList.add('active', 'text-gray-200', 'bg-darkbg-700');
        b.classList.remove('text-gray-400');
        document.getElementById('panelCustomInput').classList.remove('hidden');
    } else if (tabKey === 'run') {
        const b = document.getElementById('tabRunOutputBtn');
        b.classList.add('active', 'text-gray-200', 'bg-darkbg-700');
        b.classList.remove('text-gray-400');
        document.getElementById('panelRunOutput').classList.remove('hidden');
    } else if (tabKey === 'submit') {
        const b = document.getElementById('tabSubmitResultBtn');
        b.classList.add('active', 'text-gray-200', 'bg-darkbg-700');
        b.classList.remove('text-gray-400');
        document.getElementById('panelSubmitResult').classList.remove('hidden');
    }
    lucide.createIcons();
}

// Thu phong / An hien Console Drawer
let isConsoleCollapsed = false;
let isConsoleExpanded = false;

function toggleConsole() {
    const drawer = document.getElementById('consoleDrawer');
    if (isConsoleCollapsed) {
        drawer.style.height = '16rem';
        isConsoleCollapsed = false;
    } else {
        drawer.style.height = '2.25rem';
        isConsoleCollapsed = true;
    }
}

function toggleConsoleSize() {
    const drawer = document.getElementById('consoleDrawer');
    if (isConsoleExpanded) {
        drawer.style.height = '16rem';
        isConsoleExpanded = false;
    } else {
        drawer.style.height = '28rem';
        isConsoleExpanded = true;
    }
}

function resetCustomInput() {
    const sampleInput = problemMetaEl ? problemMetaEl.getAttribute('data-sample-input') : '';
    document.getElementById('customStdinInput').value = sampleInput;
}

function copyToClipboard(elementId) {
    const el = document.getElementById(elementId);
    if (!el) return;
    navigator.clipboard.writeText(el.innerText).then(() => {
        alert("Đã sao chép vào clipboard!");
    });
}

// ==================== RUN CODE (CHAY THU TEST MAU) ====================

async function handleRunCode() {
    if (!monacoEditor) return;
    const code = monacoEditor.getValue();
    const customInput = document.getElementById('customStdinInput').value;
    const runBtn = document.getElementById('runCodeBtn');

    if (!code.trim()) {
        alert("Vui lòng viết code trước khi chạy thử!");
        return;
    }

    // Chuyen den tab ket qua chay thu va hien loading
    switchConsoleTab('run');
    runBtn.disabled = true;
    runBtn.innerHTML = `<i data-lucide="loader" class="w-3.5 h-3.5 animate-spin text-cyan-400"></i><span>Đang chạy...</span>`;
    lucide.createIcons();

    const verdictBadge = document.getElementById('runVerdictBadge');
    const timeBadge = document.getElementById('runTimeBadge');
    const stdoutArea = document.getElementById('runStdoutArea');
    const stderrBox = document.getElementById('runStderrBox');
    const stderrArea = document.getElementById('runStderrArea');

    verdictBadge.textContent = "Đang thực thi mã nguồn...";
    verdictBadge.className = "font-bold text-amber-400 font-sans";
    timeBadge.textContent = "Đang chạy...";
    stdoutArea.textContent = "";
    stderrBox.classList.add('hidden');

    try {
        const response = await fetch('/api/run', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                problem_id: problemId,
                language: currentLanguage,
                code: code,
                custom_input: customInput
            })
        });

        const data = await response.json();

        if (data.verdict === 'SUCCESS') {
            verdictBadge.textContent = "Thực thi thành công (Finished)";
            verdictBadge.className = "font-bold text-emerald-400 font-sans";
        } else if (data.verdict === 'TLE') {
            verdictBadge.textContent = "Time Limit Exceeded (Quá thời gian 1.5s)";
            verdictBadge.className = "font-bold text-amber-400 font-sans";
        } else if (data.verdict === 'CE') {
            verdictBadge.textContent = "Lỗi biên dịch (Compilation Error)";
            verdictBadge.className = "font-bold text-purple-400 font-sans";
        } else if (data.verdict === 'SECURITY_VIOLATION') {
            verdictBadge.textContent = "Cảnh báo bảo mật: Lệnh bị chặn!";
            verdictBadge.className = "font-bold text-rose-500 font-sans";
        } else {
            verdictBadge.textContent = `Lỗi thực thi (${data.verdict || 'RTE'})`;
            verdictBadge.className = "font-bold text-rose-400 font-sans";
        }

        timeBadge.textContent = `${data.duration_ms || 0} ms`;
        stdoutArea.textContent = data.stdout || '(Không có dữ liệu in ra stdout)';

        if (data.stderr && data.stderr.trim()) {
            stderrBox.classList.remove('hidden');
            stderrArea.textContent = data.stderr;
        } else {
            stderrBox.classList.add('hidden');
        }

    } catch (err) {
        verdictBadge.textContent = "Lỗi kết nối tới máy chủ!";
        verdictBadge.className = "font-bold text-red-500 font-sans";
        stdoutArea.textContent = String(err);
    } finally {
        runBtn.disabled = false;
        runBtn.innerHTML = `<i data-lucide="play" class="w-3.5 h-3.5 text-cyan-400"></i><span>Chạy thử</span>`;
        lucide.createIcons();
    }
}

// ==================== SUBMIT CODE (CHAM DIEM TOAN BO 5 TEST CASES) ====================

async function handleSubmitCode() {
    if (!monacoEditor) return;
    const code = monacoEditor.getValue();
    const submitBtn = document.getElementById('submitCodeBtn');

    if (!code.trim()) {
        alert("Vui lòng viết code trước khi nộp bài!");
        return;
    }

    // Chuyen den tab cham diem
    switchConsoleTab('submit');
    submitBtn.disabled = true;
    submitBtn.innerHTML = `<i data-lucide="loader" class="w-3.5 h-3.5 animate-spin"></i><span>Đang chấm...</span>`;
    lucide.createIcons();

    // Hien loading trong console
    const statusBadge = document.getElementById('submitStatusBadge');
    const scoreText = document.getElementById('submitScoreText');
    const detailText = document.getElementById('submitDetailText');
    const timeText = document.getElementById('submitTimeText');
    const container = document.getElementById('testCasesContainer');

    statusBadge.textContent = "JUDGING...";
    statusBadge.className = "px-3 py-1 rounded font-bold font-mono text-sm bg-amber-500/20 text-amber-400 border border-amber-500/40 animate-pulse";
    scoreText.textContent = "Hệ thống đang chấm 5/5 test cases...";
    detailText.textContent = "Biên dịch và chạy qua từng bộ test (Test cơ bản, Test biên, Stress test)...";
    timeText.textContent = "";
    container.innerHTML = `
        <div class="py-6 text-center text-gray-400 text-xs flex flex-col items-center justify-center space-y-2">
            <div class="w-7 h-7 border-2 border-emerald-500 border-t-transparent rounded-full animate-spin"></div>
            <span>Đang kiểm tra với toàn bộ bộ test cases...</span>
        </div>
    `;

    try {
        const res = await fetch('/api/submit', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                problem_id: problemId,
                language: currentLanguage,
                code: code
            })
        });

        const data = await res.json();

        // Mo khoa loi giai vi nguoi dung da submit
        isSolutionUnlocked = true;

        // 1. Cap nhat Header tong quan
        const status = data.status;
        const score = data.score;
        const passed = data.passed_count;
        const total = data.total_count;

        if (status === 'AC') {
            statusBadge.textContent = "ACCEPTED (AC)";
            statusBadge.className = "px-3 py-1 rounded font-bold font-mono text-sm bg-emerald-500/20 text-emerald-400 border border-emerald-500/40";
        } else if (status === 'WA') {
            statusBadge.textContent = "WRONG ANSWER (WA)";
            statusBadge.className = "px-3 py-1 rounded font-bold font-mono text-sm bg-rose-500/20 text-rose-400 border border-rose-500/40";
        } else if (status === 'TLE') {
            statusBadge.textContent = "TIME LIMIT EXCEEDED (TLE)";
            statusBadge.className = "px-3 py-1 rounded font-bold font-mono text-sm bg-amber-500/20 text-amber-400 border border-amber-500/40";
        } else if (status === 'CE') {
            statusBadge.textContent = "COMPILATION ERROR (CE)";
            statusBadge.className = "px-3 py-1 rounded font-bold font-mono text-sm bg-purple-500/20 text-purple-400 border border-purple-500/40";
        } else if (status === 'SECURITY_VIOLATION') {
            statusBadge.textContent = "SECURITY BLOCKED";
            statusBadge.className = "px-3 py-1 rounded font-bold font-mono text-sm bg-red-600/30 text-red-300 border border-red-500";
        } else {
            statusBadge.textContent = status || "ERROR";
            statusBadge.className = "px-3 py-1 rounded font-bold font-mono text-sm bg-rose-500/20 text-rose-400 border border-rose-500/40";
        }

        scoreText.textContent = `${score} / 100 Điểm (${passed}/${total} test cases vượt qua)`;
        detailText.textContent = data.message || "";
        timeText.textContent = `Thời gian chạy tối đa: ${data.max_time_ms || 0} ms`;

        // 2. Render danh sach chi tiet tung Test Case
        container.innerHTML = "";

        if (data.compiler_output) {
            container.innerHTML += `
                <div class="p-3 rounded-lg bg-rose-950/40 border border-rose-800 text-rose-300 text-xs">
                    <div class="font-bold mb-1">Chi tiết lỗi biên dịch:</div>
                    <pre class="overflow-x-auto whitespace-pre-wrap font-mono">${data.compiler_output}</pre>
                </div>
            `;
        }

        if (data.test_results && data.test_results.length > 0) {
            data.test_results.forEach(tc => {
                const isPassed = tc.verdict === 'AC';
                const badgeColor = isPassed
                    ? 'bg-emerald-500/10 text-emerald-400 border-emerald-500/30'
                    : (tc.verdict === 'TLE' ? 'bg-amber-500/10 text-amber-400 border-amber-500/30' : 'bg-rose-500/10 text-rose-400 border-rose-500/30');

                const cardHtml = `
                    <div class="p-3 rounded-lg bg-darkbg-900 border ${isPassed ? 'border-darkbg-700' : 'border-rose-900/60'} text-xs space-y-2">
                        <div class="flex items-center justify-between">
                            <div class="flex items-center space-x-2">
                                <span class="px-2 py-0.5 rounded font-mono font-bold border ${badgeColor}">${tc.verdict}</span>
                                <span class="font-semibold text-gray-200">Test #${tc.test_index}: ${tc.description}</span>
                            </div>
                            <span class="text-gray-500 font-mono text-[11px]">${tc.execution_time_ms} ms</span>
                        </div>

                        ${!isPassed ? `
                            <div class="grid grid-cols-1 md:grid-cols-2 gap-2 mt-2 pt-2 border-t border-darkbg-800 text-[11px]">
                                <div class="bg-darkbg-850 p-2 rounded border border-darkbg-700">
                                    <span class="text-gray-400 block mb-0.5 font-sans">Input:</span>
                                    <pre class="text-cyan-400 overflow-x-auto">${tc.input_preview}</pre>
                                </div>
                                <div class="bg-darkbg-850 p-2 rounded border border-darkbg-700">
                                    <span class="text-gray-400 block mb-0.5 font-sans">Đáp án chuẩn (Expected):</span>
                                    <pre class="text-emerald-400 overflow-x-auto">${tc.expected_preview}</pre>
                                </div>
                                <div class="bg-darkbg-850 p-2 rounded border border-darkbg-700 md:col-span-2">
                                    <span class="text-gray-400 block mb-0.5 font-sans">Kết quả chương trình của bạn (Actual):</span>
                                    <pre class="text-rose-400 overflow-x-auto">${tc.actual_preview || '(Không có output)'}</pre>
                                </div>
                            </div>
                        ` : ''}
                    </div>
                `;
                container.innerHTML += cardHtml;
            });
        }

        // 3. Tu dong lam moi (reset) code trong editor ve Starter Template va xoa cache
        const starter = starterTemplates[currentLanguage] || '';
        monacoEditor.setValue(starter);
        const savedCodeKey = `dragon_v2_code_${problemId}_${currentLanguage}`;
        localStorage.setItem(savedCodeKey, starter);

        // Hien thi toast thong bao trang thai lam moi
        showToast("Đã nộp bài thành công! Trình soạn thảo đã được tự động làm mới về khung mẫu ban đầu.", "success");

        // 4. Tu dong cap nhat lich su nop o tab ben trai
        reloadSubmissions();

    } catch (err) {
        statusBadge.textContent = "LỖI";
        statusBadge.className = "px-3 py-1 rounded font-bold font-mono text-sm bg-rose-500/20 text-rose-400";
        scoreText.textContent = "Không thể gửi bài nộp tới máy chủ!";
        detailText.textContent = String(err);
    } finally {
        submitBtn.disabled = false;
        submitBtn.innerHTML = `<i data-lucide="send" class="w-3.5 h-3.5"></i><span>Nộp bài</span>`;
        lucide.createIcons();
    }
}

// Luu tru danh sach bai nop hien tai de tra cuu nhanh khi xem code
let loadedSubmissionsMap = {};
let activeModalSubmission = null;

// Reload danh sach lich su nop bai
async function reloadSubmissions() {
    const listContainer = document.getElementById('submissionListContainer');
    if (!listContainer) return;

    try {
        const res = await fetch(`/api/submissions/${problemId}`);
        const data = await res.json();
        const subs = data.submissions || [];

        loadedSubmissionsMap = {};
        subs.forEach(s => {
            loadedSubmissionsMap[s.id] = s;
        });

        if (subs.length === 0) {
            listContainer.innerHTML = `
                <div class="text-center py-8 text-gray-500 text-xs">
                    Bạn chưa nộp lần nào cho bài toán này. Hãy viết code và bấm "Nộp bài"!
                </div>
            `;
            return;
        }

        listContainer.innerHTML = subs.map(sub => {
            let badgeClass = 'bg-red-500/10 text-red-400 border-red-500/30';
            if (sub.status === 'AC') badgeClass = 'bg-emerald-500/10 text-emerald-400 border-emerald-500/30';
            else if (sub.status === 'WA') badgeClass = 'bg-rose-500/10 text-rose-400 border-rose-500/30';
            else if (sub.status === 'TLE') badgeClass = 'bg-amber-500/10 text-amber-400 border-amber-500/30';
            else if (sub.status === 'CE') badgeClass = 'bg-purple-500/10 text-purple-400 border-purple-500/30';

            return `
                <div class="bg-darkbg-850 p-3 rounded-lg border border-darkbg-700 space-y-2 hover:border-darkbg-600 transition">
                    <div class="flex items-center justify-between text-xs">
                        <div class="flex items-center space-x-2.5">
                            <span class="px-2 py-0.5 rounded font-bold font-mono border ${badgeClass}">${sub.status}</span>
                            <div class="text-gray-300">
                                <span class="font-semibold text-white">${sub.score}/100 điểm</span>
                                <span class="text-gray-500 text-[11px]">(${sub.passed_count}/${sub.total_count} tests)</span>
                            </div>
                        </div>
                        <div class="text-right text-gray-400">
                            <div class="font-mono text-[11px] text-gray-300 uppercase">${sub.language} • ${sub.max_time_ms}ms</div>
                            <div class="text-[10px] text-gray-500">${sub.created_at}</div>
                        </div>
                    </div>

                    <!-- Action buttons: Xem code & Nap lai -->
                    <div class="flex items-center justify-end space-x-2 pt-1 border-t border-darkbg-800 text-[11px]">
                        <button onclick="openSubmissionModal(${sub.id})"
                            class="px-2.5 py-1 rounded bg-darkbg-800 hover:bg-darkbg-700 text-gray-300 border border-darkbg-700 hover:text-white flex items-center space-x-1 transition">
                            <i data-lucide="eye" class="w-3 h-3 text-cyan-400"></i>
                            <span>Xem code</span>
                        </button>
                        <button onclick="restoreSubmissionCode(${sub.id})"
                            class="px-2.5 py-1 rounded bg-orange-500/10 hover:bg-orange-500/20 text-orange-400 border border-orange-500/30 flex items-center space-x-1 transition">
                            <i data-lucide="rotate-ccw" class="w-3 h-3 text-orange-400"></i>
                            <span>Nạp vào Editor</span>
                        </button>
                    </div>
                </div>
            `;
        }).join('');

        lucide.createIcons();

    } catch (e) {
        console.warn("Không thể tải lịch sử nộp bài:", e);
    }
}

// Mo Modal xem lai ma nguon da nop
function openSubmissionModal(subId) {
    const sub = loadedSubmissionsMap[subId];
    if (!sub) return;

    activeModalSubmission = sub;
    const modal = document.getElementById('viewSubmissionModal');
    const statusBadge = document.getElementById('modalSubStatus');
    const scoreText = document.getElementById('modalSubScore');
    const langText = document.getElementById('modalSubLang');
    const timeText = document.getElementById('modalSubTime');
    const codeArea = document.getElementById('modalSubCodeContent');

    let badgeClass = 'bg-red-500/20 text-red-400 border border-red-500/30';
    if (sub.status === 'AC') badgeClass = 'bg-emerald-500/20 text-emerald-400 border border-emerald-500/30';
    else if (sub.status === 'WA') badgeClass = 'bg-rose-500/20 text-rose-400 border border-rose-500/30';
    else if (sub.status === 'TLE') badgeClass = 'bg-amber-500/20 text-amber-400 border border-amber-500/30';
    else if (sub.status === 'CE') badgeClass = 'bg-purple-500/20 text-purple-400 border border-purple-500/30';

    statusBadge.textContent = sub.status;
    statusBadge.className = `px-2 py-0.5 rounded text-xs font-mono font-bold ${badgeClass}`;
    scoreText.textContent = `(${sub.score}/100 điểm, ${sub.passed_count}/${sub.total_count} tests)`;
    langText.textContent = sub.language;
    timeText.textContent = sub.created_at;
    codeArea.textContent = sub.code || '// (Không có mã nguồn)';

    modal.classList.remove('hidden');
    lucide.createIcons();
}

// Dong Modal xem code
function closeSubmissionModal() {
    const modal = document.getElementById('viewSubmissionModal');
    if (modal) modal.classList.add('hidden');
    activeModalSubmission = null;
}

// Sao chep ma trong modal
function copyModalCode() {
    if (!activeModalSubmission || !activeModalSubmission.code) return;
    navigator.clipboard.writeText(activeModalSubmission.code).then(() => {
        showToast("Đã sao chép mã nguồn vào clipboard!", "info");
    });
}

// Nap code tu Modal vao Editor
function restoreFromModal() {
    if (!activeModalSubmission) return;
    restoreSubmissionCode(activeModalSubmission.id);
    closeSubmissionModal();
}

// Nap truc tiep code cua mot submission vao Monaco Editor
function restoreSubmissionCode(subId) {
    const sub = loadedSubmissionsMap[subId];
    if (!sub || !monacoEditor) return;

    if (confirm(`Bạn có muốn nạp lại mã nguồn lần nộp này (${sub.language.toUpperCase()}, ${sub.status} - ${sub.score}đ) vào Editor không? Code hiện tại chưa lưu sẽ bị thay thế.`)) {
        // Chuyen ngon ngu neu khac
        const targetLang = sub.language.toLowerCase().includes('c') ? 'c' : 'python3';
        if (targetLang !== currentLanguage) {
            const select = document.getElementById('langSelect');
            if (select) {
                select.value = targetLang;
                currentLanguage = targetLang;
                const monacoLang = (targetLang === 'python3') ? 'python' : 'c';
                monaco.editor.setModelLanguage(monacoEditor.getModel(), monacoLang);
            }
        }

        monacoEditor.setValue(sub.code);
        const savedCodeKey = `dragon_v2_code_${problemId}_${currentLanguage}`;
        localStorage.setItem(savedCodeKey, sub.code);

        showToast(`Đã khôi phục mã nguồn lần nộp (${sub.status} - ${sub.score} điểm) vào Editor!`, "success");
    }
}

// Toast notification helper
function showToast(message, type = 'info') {
    const container = document.getElementById('toastContainer');
    if (!container) return;

    const toast = document.createElement('div');
    const bgClass = type === 'success' ? 'bg-emerald-900/90 border-emerald-500 text-emerald-200' :
                   (type === 'error' ? 'bg-rose-900/90 border-rose-500 text-rose-200' : 'bg-darkbg-800/95 border-darkbg-600 text-gray-200');

    toast.className = `p-3.5 rounded-xl border shadow-2xl text-xs font-medium flex items-center space-x-2.5 transition-all duration-300 opacity-0 translate-y-2 pointer-events-auto ${bgClass}`;
    toast.innerHTML = `
        <i data-lucide="${type === 'success' ? 'check-circle' : 'info'}" class="w-4 h-4 flex-shrink-0"></i>
        <span>${message}</span>
    `;

    container.appendChild(toast);
    lucide.createIcons();

    // Trigger animation
    requestAnimationFrame(() => {
        toast.classList.remove('opacity-0', 'translate-y-2');
        toast.classList.add('opacity-100', 'translate-y-0');
    });

    // Auto remove after 4.5s
    setTimeout(() => {
        toast.classList.remove('opacity-100', 'translate-y-0');
        toast.classList.add('opacity-0', 'translate-y-2');
        setTimeout(() => toast.remove(), 350);
    }, 4500);
}
