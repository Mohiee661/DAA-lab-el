document.addEventListener('DOMContentLoaded', () => {
    // DOM elements
    const signaturesTextarea = document.getElementById('signatures');
    const logContentTextarea = document.getElementById('log-content');
    const loadDefaultSigs = document.getElementById('load-default-signatures');
    const loadDefaultLog = document.getElementById('load-default-log');
    const detectBtn = document.getElementById('detect-btn');
    const tabBtns = document.querySelectorAll('.tab-btn');
    const statusMessage = document.getElementById('status-message');
    
    // Performance chart
    let performanceChart = null;
    
    // Tab switching
    tabBtns.forEach(btn => {
        btn.addEventListener('click', () => {
            // Remove active class from all tabs
            tabBtns.forEach(b => b.classList.remove('active'));
            document.querySelectorAll('.tab-pane').forEach(pane => pane.classList.remove('active'));
            
            // Add active class to clicked tab
            btn.classList.add('active');
            document.getElementById(`${btn.dataset.tab}-tab`).classList.add('active');
            
            // Update chart if comparison tab is selected
            if (btn.dataset.tab === 'comparison' && performanceChart) {
                performanceChart.update();
            }
        });
    });
    
    // Load default signatures
    loadDefaultSigs.addEventListener('click', async () => {
        statusMessage.textContent = 'Loading default signatures...';
        try {
            const response = await fetch('/api/signatures');
            const data = await response.json();
            
            if (data.success) {
                signaturesTextarea.value = data.signatures.join('\n');
                statusMessage.textContent = 'Default signatures loaded';
            } else {
                throw new Error('Failed to load signatures');
            }
        } catch (error) {
            console.error('Error loading signatures:', error);
            statusMessage.textContent = `Error: ${error.message}`;
        }
    });
    
    // Load default log
    loadDefaultLog.addEventListener('click', async () => {
        statusMessage.textContent = 'Loading default log file...';
        try {
            const response = await fetch('/api/log');
            const data = await response.json();
            
            if (data.success) {
                logContentTextarea.value = data.content;
                statusMessage.textContent = 'Default log file loaded';
            } else {
                throw new Error('Failed to load log file');
            }
        } catch (error) {
            console.error('Error loading log file:', error);
            statusMessage.textContent = `Error: ${error.message}`;
        }
    });
    
    // Handle file uploads for signatures
    document.getElementById('signatures-file').addEventListener('change', (event) => {
        const file = event.target.files[0];
        if (file) {
            const reader = new FileReader();
            reader.onload = (e) => {
                signaturesTextarea.value = e.target.result;
                statusMessage.textContent = 'Signatures file loaded';
            };
            reader.onerror = () => {
                statusMessage.textContent = 'Error reading signatures file';
            };
            reader.readAsText(file);
        }
    });
    
    // Handle file uploads for log content
    document.getElementById('log-file').addEventListener('change', (event) => {
        const file = event.target.files[0];
        if (file) {
            const reader = new FileReader();
            reader.onload = (e) => {
                logContentTextarea.value = e.target.result;
                statusMessage.textContent = 'Log file loaded';
            };
            reader.onerror = () => {
                statusMessage.textContent = 'Error reading log file';
            };
            reader.readAsText(file);
        }
    });
    
    // Initialize chart
    function initPerformanceChart(kmpTime, naiveTime) {
        const ctx = document.getElementById('performance-chart').getContext('2d');
        
        if (performanceChart) {
            performanceChart.destroy();
        }
        
        performanceChart = new Chart(ctx, {
            type: 'bar',
            data: {
                labels: ['KMP Algorithm', 'Naive Algorithm'],
                datasets: [{
                    label: 'Execution Time (seconds)',
                    data: [kmpTime, naiveTime],
                    backgroundColor: [
                        'rgba(52, 152, 219, 0.7)',
                        'rgba(230, 126, 34, 0.7)'
                    ],
                    borderColor: [
                        'rgba(52, 152, 219, 1)',
                        'rgba(230, 126, 34, 1)'
                    ],
                    borderWidth: 1
                }]
            },
            options: {
                indexAxis: 'y',
                scales: {
                    x: {
                        beginAtZero: true,
                        title: {
                            display: true,
                            text: 'Time (seconds)'
                        }
                    }
                },
                plugins: {
                    title: {
                        display: true,
                        text: 'Algorithm Performance Comparison'
                    }
                },
                responsive: true,
                maintainAspectRatio: false
            }
        });
    }
    
    // Detect intrusions
    detectBtn.addEventListener('click', async () => {
        const signatures = signaturesTextarea.value.trim();
        const logContent = logContentTextarea.value.trim();
        
        if (!signatures) {
            statusMessage.textContent = 'Error: Please enter at least one signature';
            return;
        }
        
        if (!logContent) {
            statusMessage.textContent = 'Error: Please enter log content to analyze';
            return;
        }
        
        statusMessage.textContent = 'Detecting intrusions...';
        detectBtn.disabled = true;
        
        try {
            const response = await fetch('/api/detect', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    signatures: signatures.split('\n').filter(s => s.trim()),
                    log_content: logContent
                })
            });
            
            const data = await response.json();
            
            if (data.success) {
                displayResults(data);
                statusMessage.textContent = 'Detection completed';
            } else {
                throw new Error('Detection failed');
            }
        } catch (error) {
            console.error('Error detecting intrusions:', error);
            statusMessage.textContent = `Error: ${error.message}`;
        } finally {
            detectBtn.disabled = false;
        }
    });
    
    // Display detection results
    function displayResults(data) {
        // KMP results
        const kmpResultsContainer = document.getElementById('kmp-results');
        const kmpCount = document.getElementById('kmp-count');
        const kmpTime = document.getElementById('kmp-time');
        
        // Naive results
        const naiveResultsContainer = document.getElementById('naive-results');
        const naiveCount = document.getElementById('naive-count');
        const naiveTime = document.getElementById('naive-time');
        
        // Comparison tab
        const kmpTimeComp = document.getElementById('kmp-time-comp');
        const kmpMatchesComp = document.getElementById('kmp-matches-comp');
        const naiveTimeComp = document.getElementById('naive-time-comp');
        const naiveMatchesComp = document.getElementById('naive-matches-comp');
        const speedComparison = document.getElementById('speed-comparison');
        
        // Count total matches
        const kmpTotalMatches = Object.values(data.kmp_results).reduce((total, matches) => total + matches.length, 0);
        const naiveTotalMatches = Object.values(data.naive_results).reduce((total, matches) => total + matches.length, 0);
        
        // Update KMP results
        kmpResultsContainer.innerHTML = '';
        kmpCount.textContent = kmpTotalMatches;
        kmpTime.textContent = `${data.kmp_time.toFixed(6)} sec`;
        
        if (Object.keys(data.kmp_results).length === 0) {
            kmpResultsContainer.innerHTML = '<p class="no-results">No matches found</p>';
        } else {
            for (const [signature, matches] of Object.entries(data.kmp_results)) {
                const resultItem = document.createElement('div');
                resultItem.className = 'result-item';
                
                const signatureHeader = document.createElement('div');
                signatureHeader.className = 'signature-header';
                signatureHeader.textContent = `Signature: "${signature}"`;
                
                const matchPositions = document.createElement('div');
                matchPositions.className = 'match-positions';
                matchPositions.textContent = `Matches at positions: ${matches.join(', ')}`;
                
                resultItem.appendChild(signatureHeader);
                resultItem.appendChild(matchPositions);
                kmpResultsContainer.appendChild(resultItem);
            }
        }
        
        // Update Naive results
        naiveResultsContainer.innerHTML = '';
        naiveCount.textContent = naiveTotalMatches;
        naiveTime.textContent = `${data.naive_time.toFixed(6)} sec`;
        
        if (Object.keys(data.naive_results).length === 0) {
            naiveResultsContainer.innerHTML = '<p class="no-results">No matches found</p>';
        } else {
            for (const [signature, matches] of Object.entries(data.naive_results)) {
                const resultItem = document.createElement('div');
                resultItem.className = 'result-item';
                
                const signatureHeader = document.createElement('div');
                signatureHeader.className = 'signature-header';
                signatureHeader.textContent = `Signature: "${signature}"`;
                
                const matchPositions = document.createElement('div');
                matchPositions.className = 'match-positions';
                matchPositions.textContent = `Matches at positions: ${matches.join(', ')}`;
                
                resultItem.appendChild(signatureHeader);
                resultItem.appendChild(matchPositions);
                naiveResultsContainer.appendChild(resultItem);
            }
        }
        
        // Update comparison tab
        kmpTimeComp.textContent = data.kmp_time.toFixed(6);
        kmpMatchesComp.textContent = kmpTotalMatches;
        naiveTimeComp.textContent = data.naive_time.toFixed(6);
        naiveMatchesComp.textContent = naiveTotalMatches;
        
        // Calculate speed comparison
        let speedText = '';
        if (data.kmp_time < data.naive_time) {
            const speedup = (data.naive_time / data.kmp_time).toFixed(2);
            speedText = `KMP is ${speedup}x faster than Naive`;
        } else if (data.naive_time < data.kmp_time) {
            const speedup = (data.kmp_time / data.naive_time).toFixed(2);
            speedText = `Naive is ${speedup}x faster than KMP`;
        } else {
            speedText = 'Both algorithms performed equally';
        }
        
        speedComparison.textContent = speedText;
        
        // Initialize performance chart
        initPerformanceChart(data.kmp_time, data.naive_time);
    }
    
    // Load default data on page load
    loadDefaultSigs.click();
    loadDefaultLog.click();
}); 