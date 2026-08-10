document.addEventListener('DOMContentLoaded', function () {
    // -------------------------------------------------------------------------
    // 1. Dark Mode Toggle
    // -------------------------------------------------------------------------
    const themeToggleBtn = document.getElementById('theme-toggle');
    const themeIcon = document.getElementById('theme-icon');
    
    // Check local storage or system preference
    const savedTheme = localStorage.getItem('theme');
    const prefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches;
    
    if (savedTheme === 'dark' || (!savedTheme && prefersDark)) {
        document.body.classList.add('dark-theme');
        if (themeIcon) {
            themeIcon.classList.remove('bi-moon-fill');
            themeIcon.classList.add('bi-sun-fill');
        }
    } else {
        document.body.classList.remove('dark-theme');
        if (themeIcon) {
            themeIcon.classList.remove('bi-sun-fill');
            themeIcon.classList.add('bi-moon-fill');
        }
    }
    
    if (themeToggleBtn) {
        themeToggleBtn.addEventListener('click', function () {
            document.body.classList.toggle('dark-theme');
            const isDark = document.body.classList.contains('dark-theme');
            localStorage.setItem('theme', isDark ? 'dark' : 'light');
            
            if (themeIcon) {
                if (isDark) {
                    themeIcon.classList.remove('bi-moon-fill');
                    themeIcon.classList.add('bi-sun-fill');
                } else {
                    themeIcon.classList.remove('bi-sun-fill');
                    themeIcon.classList.add('bi-moon-fill');
                }
            }
            
            // Re-render charts to update colors for dark/light themes if charts exist
            renderCharts();
        });
    }

    // -------------------------------------------------------------------------
    // 2. Multi-Step Form Logic
    // -------------------------------------------------------------------------
    const formSteps = document.querySelectorAll('.form-step');
    const stepIndicators = document.querySelectorAll('.step-indicator');
    const progressLine = document.querySelector('.step-progress-line');
    const nextBtns = document.querySelectorAll('.btn-next');
    const prevBtns = document.querySelectorAll('.btn-prev');
    const healthForm = document.getElementById('predictionForm');
    
    let currentStep = 0;
    
    function updateFormSteps() {
        // Show/Hide steps
        formSteps.forEach((step, index) => {
            if (index === currentStep) {
                step.classList.add('active');
            } else {
                step.classList.remove('active');
            }
        });
        
        // Update step indicator classes
        stepIndicators.forEach((indicator, index) => {
            if (index < currentStep) {
                indicator.classList.add('completed');
                indicator.classList.remove('active');
            } else if (index === currentStep) {
                indicator.classList.add('active');
                indicator.classList.remove('completed');
            } else {
                indicator.classList.remove('active', 'completed');
            }
        });
        
        // Update progress bar line width
        if (progressLine && stepIndicators.length > 1) {
            const percentage = (currentStep / (stepIndicators.length - 1)) * 100;
            progressLine.style.width = percentage + '%';
        }
    }
    
    function validateStep(stepIndex) {
        let valid = true;
        const currentStepEl = formSteps[stepIndex];
        if (!currentStepEl) return true;
        
        const inputs = currentStepEl.querySelectorAll('input[required], select[required], textarea[required]');
        
        inputs.forEach(input => {
            // Remove existing invalid styling
            input.classList.remove('is-invalid');
            
            if (!input.value.trim()) {
                input.classList.add('is-invalid');
                valid = false;
            }
            
            // Type-specific range validation
            if (input.type === 'number') {
                const val = Number(input.value);
                const min = input.getAttribute('min') ? Number(input.getAttribute('min')) : null;
                const max = input.getAttribute('max') ? Number(input.getAttribute('max')) : null;
                
                if (min !== null && val < min) {
                    input.classList.add('is-invalid');
                    valid = false;
                }
                if (max !== null && val > max) {
                    input.classList.add('is-invalid');
                    valid = false;
                }
            }
        });
        
        // Feedback message if invalid
        if (!valid) {
            const errorBanner = document.getElementById('form-error-banner');
            if (errorBanner) {
                errorBanner.textContent = 'Please fill out all required fields with valid values before proceeding.';
                errorBanner.classList.remove('d-none');
                errorBanner.scrollIntoView({ behavior: 'smooth' });
            }
        } else {
            const errorBanner = document.getElementById('form-error-banner');
            if (errorBanner) {
                errorBanner.classList.add('d-none');
            }
        }
        
        return valid;
    }
    
    nextBtns.forEach(btn => {
        btn.addEventListener('click', () => {
            if (validateStep(currentStep)) {
                currentStep++;
                if (currentStep >= formSteps.length) {
                    currentStep = formSteps.length - 1;
                }
                updateFormSteps();
            }
        });
    });
    
    prevBtns.forEach(btn => {
        btn.addEventListener('click', () => {
            currentStep--;
            if (currentStep < 0) {
                currentStep = 0;
            }
            updateFormSteps();
        });
    });

    if (healthForm) {
        healthForm.addEventListener('submit', function (e) {
            // Validate the final step before submitting
            if (!validateStep(currentStep)) {
                e.preventDefault();
            }
        });
    }

    // -------------------------------------------------------------------------
    // 3. Live BMI Calculator
    // -------------------------------------------------------------------------
    const heightInput = document.getElementById('height');
    const weightInput = document.getElementById('weight');
    const bmiOutput = document.getElementById('bmi-output');
    const bmiPill = document.getElementById('bmi-pill');
    
    function calculateBMI() {
        const heightVal = Number(heightInput?.value || 0);
        const weightVal = Number(weightInput?.value || 0);
        
        if (heightVal > 0 && weightVal > 0) {
            const bmi = weightVal / ((heightVal / 100) * (heightVal / 100));
            const roundedBmi = bmi.toFixed(2);
            
            if (bmiOutput) {
                bmiOutput.value = roundedBmi;
            }
            
            if (bmiPill) {
                bmiPill.textContent = `BMI: ${roundedBmi} - `;
                bmiPill.className = 'bmi-pill'; // Reset classes
                
                if (bmi < 18.5) {
                    bmiPill.textContent += 'Underweight';
                    bmiPill.classList.add('bmi-underweight');
                } else if (bmi >= 18.5 && bmi < 25) {
                    bmiPill.textContent += 'Normal';
                    bmiPill.classList.add('bmi-normal');
                } else if (bmi >= 25 && bmi < 30) {
                    bmiPill.textContent += 'Overweight';
                    bmiPill.classList.add('bmi-overweight');
                } else {
                    bmiPill.textContent += 'Obese';
                    bmiPill.classList.add('bmi-obese');
                }
                bmiPill.classList.remove('d-none');
            }
        } else {
            if (bmiOutput) bmiOutput.value = '';
            if (bmiPill) {
                bmiPill.classList.add('d-none');
            }
        }
    }
    
    if (heightInput && weightInput) {
        ['input', 'change', 'keyup'].forEach(evt => {
            heightInput.addEventListener(evt, calculateBMI);
            weightInput.addEventListener(evt, calculateBMI);
        });
    }

    // -------------------------------------------------------------------------
    // 4. Chart.js Dashboard Visualization
    // -------------------------------------------------------------------------
    let riskChartInstance = null;
    let lifestyleChartInstance = null;

    function renderCharts() {
        const riskChartEl = document.getElementById('riskChart');
        const lifestyleChartEl = document.getElementById('lifestyleChart');
        
        if (!riskChartEl && !lifestyleChartEl) return;
        
        // Fetch dashboard data from api
        fetch('/api/history')
            .then(res => res.json())
            .then(data => {
                if (!data || data.length === 0) return;
                
                // Color customization based on Dark/Light mode
                const isDark = document.body.classList.contains('dark-theme');
                const labelColor = isDark ? '#94a3b8' : '#64748b';
                const gridColor = isDark ? 'rgba(255, 255, 255, 0.08)' : 'rgba(0, 0, 0, 0.05)';
                
                // Process Data for Risk Level Distribution
                const riskCounts = { 'Low': 0, 'Medium': 0, 'High': 0 };
                data.forEach(item => {
                    if (riskCounts[item.risk] !== undefined) {
                        riskCounts[item.risk]++;
                    }
                });
                
                // Process Data for BMI vs Age Distribution
                const bmiValues = data.map(item => item.bmi);
                const ageValues = data.map(item => item.age);
                const confidenceValues = data.map(item => item.confidence);
                
                // Render Risk Distribution Doughnut Chart
                if (riskChartEl) {
                    if (riskChartInstance) {
                        riskChartInstance.destroy();
                    }
                    
                    const riskCtx = riskChartEl.getContext('2d');
                    riskChartInstance = new Chart(riskCtx, {
                        type: 'doughnut',
                        data: {
                            labels: ['Low Risk', 'Medium Risk', 'High Risk'],
                            datasets: [{
                                data: [riskCounts['Low'], riskCounts['Medium'], riskCounts['High']],
                                backgroundColor: [
                                    isDark ? '#10b981' : '#198754', // Green
                                    isDark ? '#f59e0b' : '#fd7e14', // Amber/Orange
                                    isDark ? '#ef4444' : '#dc3545'  // Crimson/Red
                                ],
                                borderWidth: 0,
                                hoverOffset: 4
                            }]
                        },
                        options: {
                            responsive: true,
                            maintainAspectRatio: false,
                            plugins: {
                                legend: {
                                    position: 'bottom',
                                    labels: {
                                        color: labelColor,
                                        font: { family: 'Outfit', size: 12 }
                                    }
                                }
                            },
                            cutout: '65%'
                        }
                    });
                }
                
                // Render Trends / Correlation Bar Chart
                if (lifestyleChartEl) {
                    if (lifestyleChartInstance) {
                        lifestyleChartInstance.destroy();
                    }
                    
                    const lifestyleCtx = lifestyleChartEl.getContext('2d');
                    lifestyleChartInstance = new Chart(lifestyleCtx, {
                        type: 'bar',
                        data: {
                            labels: data.map((_, idx) => `Check ${idx + 1}`),
                            datasets: [
                                {
                                    label: 'BMI Score',
                                    data: bmiValues,
                                    backgroundColor: isDark ? 'rgba(59, 130, 246, 0.7)' : 'rgba(13, 110, 253, 0.7)',
                                    borderRadius: 6,
                                },
                                {
                                    label: 'Confidence %',
                                    data: confidenceValues,
                                    backgroundColor: isDark ? 'rgba(16, 185, 129, 0.7)' : 'rgba(25, 135, 84, 0.7)',
                                    borderRadius: 6,
                                }
                            ]
                        },
                        options: {
                            responsive: true,
                            maintainAspectRatio: false,
                            scales: {
                                x: {
                                    grid: { display: false },
                                    ticks: { color: labelColor, font: { family: 'Outfit' } }
                                },
                                y: {
                                    grid: { color: gridColor },
                                    ticks: { color: labelColor, font: { family: 'Outfit' } },
                                    suggestedMax: 100
                                }
                            },
                            plugins: {
                                legend: {
                                    position: 'bottom',
                                    labels: {
                                        color: labelColor,
                                        font: { family: 'Outfit', size: 12 }
                                    }
                                }
                            }
                        }
                    });
                }
            })
            .catch(err => console.error('Error fetching/rendering charts: ', err));
    }
    
    // Initial Render
    renderCharts();

    // Reset History Event
    const resetHistoryBtn = document.getElementById('resetHistoryBtn');
    if (resetHistoryBtn) {
        resetHistoryBtn.addEventListener('click', function () {
            if (confirm('Are you sure you want to reset your health screening history to default demo data?')) {
                fetch('/api/reset-history', { method: 'POST' })
                    .then(res => res.json())
                    .then(resData => {
                        if (resData.status === 'success') {
                            alert(resData.message);
                            renderCharts();
                            // Update total check count if element exists
                            const checkCountEl = document.getElementById('checkCountEl');
                            if (checkCountEl) checkCountEl.textContent = '5'; // Seeding has 5 items
                        }
                    });
            }
        });
    }

    // -------------------------------------------------------------------------
    // 5. PDF Export & Print Trigger
    // -------------------------------------------------------------------------
    const printReportBtn = document.getElementById('printReportBtn');
    if (printReportBtn) {
        printReportBtn.addEventListener('click', function () {
            window.print();
        });
    }
});
