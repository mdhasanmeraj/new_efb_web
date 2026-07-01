/**
 * Floating UAE Loan Calculator Interactive Javascript
 */

document.addEventListener('DOMContentLoaded', function () {
    // DOM Elements
    const floatingContainer = document.getElementById('calculatorFloatingContainer');
    const floatingBtn = document.getElementById('calculatorFloatingBtn');
    const tooltip = document.getElementById('calculatorTooltip');
    const tooltipClose = document.getElementById('tooltipClose');
    const popupCard = document.getElementById('calculatorPopupCard');
    const closeBtn = document.getElementById('calculatorCloseBtn');
    
    // Panels & Wizard Steps
    const panel1 = document.getElementById('calculatorPanel1');
    const panel2 = document.getElementById('calculatorPanel2');
    const step1Indicator = document.getElementById('stepIndicator1');
    const step2Indicator = document.getElementById('stepIndicator2');
    const toPanel2Btn = document.getElementById('toPanel2Btn');
    const backToPanel1Btn = document.getElementById('backToPanel1Btn');
    
    // Form 1 Elements
    const calcProductType = document.getElementById('calcProductType');
    const calcLoanAmount = document.getElementById('calcLoanAmount');
    const calcInterestRate = document.getElementById('calcInterestRate');
    const calcTenure = document.getElementById('calcTenure');
    const resultsBox = document.getElementById('calculatorResultsBox');
    const emiDisplay = document.getElementById('emiValueDisplay');
    const principalDisplay = document.getElementById('principalDisplay');
    const interestDisplay = document.getElementById('interestDisplay');
    
    // Form 2 Elements
    const leadForm = document.getElementById('leadGenerationForm');
    const leadName = document.getElementById('leadName');
    const leadMobile = document.getElementById('leadMobile');
    const leadEmail = document.getElementById('leadEmail');
    const submitQuoteBtn = document.getElementById('submitQuoteBtn');
    
    // Form 2 Hidden Inputs (Auto-filled)
    const hiddenProduct = document.getElementById('leadProductType');
    const hiddenAmount = document.getElementById('leadLoanAmount');
    const hiddenRate = document.getElementById('leadInterestRate');
    const hiddenTenure = document.getElementById('leadTenure');
    const hiddenEmi = document.getElementById('leadEmi');
    
    // Form 2 Summary Display Elements
    const summaryProduct = document.getElementById('summaryProduct');
    const summaryAmount = document.getElementById('summaryAmount');
    const summaryRate = document.getElementById('summaryRate');
    const summaryTenure = document.getElementById('summaryTenure');
    
    // Validation Errors
    const errorName = document.getElementById('errorName');
    const errorMobile = document.getElementById('errorMobile');
    const errorEmail = document.getElementById('errorEmail');

    // Chart variables
    let emiChart = null;
    let hasOpened = false;
    let typingTimer = null;
    const typingDelay = 1500; // Track EMI calculation after 1.5s pause

    // Get CSRF Token utility
    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }

    // Event Tracking Utility
    function trackEvent(eventType, metadata = {}) {
        const csrftoken = getCookie('csrftoken');
        fetch('/track-calculator-event/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrftoken
            },
            body: JSON.stringify({
                event_type: eventType,
                metadata: metadata
            })
        }).catch(err => console.warn('Analytics error:', err));
    }

    // 1. Tooltip Speech Bubble Logic
    // Show tooltip 3 seconds after page loads
    setTimeout(() => {
        if (!hasOpened && !localStorage.getItem('calc_tooltip_dismissed')) {
            tooltip.classList.add('visible');
        }
    }, 3000);

    // Dismiss tooltip
    tooltipClose.addEventListener('click', (e) => {
        e.stopPropagation();
        tooltip.classList.remove('visible');
        localStorage.setItem('calc_tooltip_dismissed', 'true');
    });

    // Hover events for floating button (Desktop)
    floatingBtn.addEventListener('mouseenter', () => {
        if (!popupCard.classList.contains('open')) {
            tooltip.classList.add('visible');
        }
    });

    // Close tooltip when clicking floating button or card
    floatingBtn.addEventListener('click', () => {
        tooltip.classList.remove('visible');
        const isOpen = popupCard.classList.contains('open');
        if (isOpen) {
            popupCard.classList.remove('open');
        } else {
            popupCard.classList.add('open');
            if (!hasOpened) {
                trackEvent('Calculator Opened', { url: window.location.href });
                hasOpened = true;
            }
        }
    });

    closeBtn.addEventListener('click', () => {
        popupCard.classList.remove('open');
    });

    // 2. Real Time Formatting for Loan Amount
    calcLoanAmount.addEventListener('input', function (e) {
        // Remove all non-digits
        let value = this.value.replace(/\D/g, '');
        if (value) {
            // Format number with commas
            let formattedValue = Number(value).toLocaleString('en-US');
            this.value = 'AED ' + formattedValue;
        } else {
            this.value = '';
        }
        calculateRealTimeEMI();
    });

    // Input listeners for other fields
    calcProductType.addEventListener('change', calculateRealTimeEMI);
    calcInterestRate.addEventListener('input', calculateRealTimeEMI);
    calcTenure.addEventListener('input', calculateRealTimeEMI);

    // 3. EMI Calculation & Chart Drawing
    function calculateRealTimeEMI() {
        const productType = calcProductType.value;
        const rawAmount = calcLoanAmount.value.replace(/AED\s?|,/g, '');
        const amount = parseFloat(rawAmount);
        const rate = parseFloat(calcInterestRate.value);
        const tenure = parseInt(calcTenure.value);

        // Check if all fields are filled & valid
        if (productType && !isNaN(amount) && amount > 0 && !isNaN(rate) && rate > 0 && !isNaN(tenure) && tenure > 0) {
            
            // Formula: EMI = P * r * (1+r)^n / ((1+r)^n - 1)
            const P = amount;
            const r = (rate / 12) / 100; // monthly rate
            const n = tenure;

            let emi = 0;
            if (r === 0) {
                emi = P / n;
            } else {
                emi = P * r * Math.pow(1 + r, n) / (Math.pow(1 + r, n) - 1);
            }

            const totalRepayment = emi * n;
            const totalInterest = totalRepayment - P;

            // Render output details
            emiDisplay.textContent = 'AED ' + emi.toLocaleString('en-US', { minimumFractionDigits: 2, maximumFractionDigits: 2 });
            principalDisplay.textContent = 'AED ' + P.toLocaleString('en-US', { minimumFractionDigits: 2, maximumFractionDigits: 2 });
            interestDisplay.textContent = 'AED ' + totalInterest.toLocaleString('en-US', { minimumFractionDigits: 2, maximumFractionDigits: 2 });
            
            resultsBox.style.display = 'flex';
            toPanel2Btn.removeAttribute('disabled');

            // Draw or update Chart.js Pie Chart
            updateChart(P, totalInterest);

            // Debounced Analytics Track for Calculation
            clearTimeout(typingTimer);
            typingTimer = setTimeout(() => {
                trackEvent('EMI Calculated', {
                    product_type: productType,
                    loan_amount: P,
                    interest_rate: rate,
                    tenure_months: tenure,
                    calculated_emi: Math.round(emi * 100) / 100
                });
            }, typingDelay);

        } else {
            resultsBox.style.display = 'none';
            toPanel2Btn.setAttribute('disabled', 'true');
        }
    }

    function updateChart(principal, interest) {
        if (typeof Chart === 'undefined') {
            console.warn('Chart.js is not loaded');
            return;
        }

        const ctx = document.getElementById('emiPieChart');
        if (!ctx) return;

        const data = {
            labels: ['Principal Portion', 'Interest Portion'],
            datasets: [{
                data: [principal, interest],
                backgroundColor: ['#0f4c81', '#e11d48'],
                hoverOffset: 4,
                borderWidth: 1
            }]
        };

        if (emiChart) {
            emiChart.data.datasets[0].data = [principal, interest];
            emiChart.update();
        } else {
            emiChart = new Chart(ctx, {
                type: 'pie',
                data: data,
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    plugins: {
                        legend: {
                            display: false // We use our own legend below the chart
                        },
                        tooltip: {
                            callbacks: {
                                label: function(context) {
                                    let label = context.label || '';
                                    if (label) {
                                        label += ': ';
                                    }
                                    if (context.parsed !== null) {
                                        label += 'AED ' + context.parsed.toLocaleString('en-US', { maximumFractionDigits: 0 });
                                    }
                                    return label;
                                }
                            }
                        }
                    }
                }
            });
        }
    }

    // 4. Panel Switching (Wizard Transitions)
    toPanel2Btn.addEventListener('click', () => {
        // Populate Panel 2 fields from Panel 1
        const rawAmount = calcLoanAmount.value.replace(/AED\s?|,/g, '');
        
        hiddenProduct.value = calcProductType.value;
        hiddenAmount.value = rawAmount;
        hiddenRate.value = calcInterestRate.value;
        hiddenTenure.value = calcTenure.value;
        
        const emiRaw = emiDisplay.textContent.replace(/AED\s?|,/g, '');
        hiddenEmi.value = emiRaw;

        // Visual summary cards in Step 2
        summaryProduct.textContent = calcProductType.value;
        summaryAmount.textContent = calcLoanAmount.value;
        summaryRate.textContent = calcInterestRate.value + '%';
        summaryTenure.textContent = calcTenure.value + ' Mos';

        // Animate Panel Transition
        panel1.classList.remove('active');
        panel2.classList.add('active');
        step1Indicator.classList.remove('active');
        step2Indicator.classList.add('active');
    });

    backToPanel1Btn.addEventListener('click', () => {
        // Animate back to Panel 1
        panel2.classList.remove('active');
        panel1.classList.add('active');
        step2Indicator.classList.remove('active');
        step1Indicator.classList.add('active');
    });

    // 5. Form Validation & Step 2 Submission
    function validatePanel2() {
        const name = leadName.value.trim();
        const mobile = leadMobile.value.trim();
        const email = leadEmail.value.trim();
        
        let isValid = true;

        // Name Check
        if (name.length < 2) {
            errorName.textContent = 'Name is too short.';
            isValid = false;
        } else {
            errorName.textContent = '';
        }

        // UAE Mobile Validation
        // +9715XXXXXXXX or 05XXXXXXXX
        const mobileRegex = /^(\+9715\d{8}|05\d{8})$/;
        if (!mobileRegex.test(mobile)) {
            errorMobile.textContent = 'Invalid UAE number. E.g. 05XXXXXXXX or +971XXXXXXXXX';
            isValid = false;
        } else {
            errorMobile.textContent = '';
        }

        // Email Validation
        const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        if (!emailRegex.test(email)) {
            errorEmail.textContent = 'Invalid email address.';
            isValid = false;
        } else {
            errorEmail.textContent = '';
        }

        if (isValid) {
            submitQuoteBtn.removeAttribute('disabled');
        } else {
            submitQuoteBtn.setAttribute('disabled', 'true');
        }
        
        return isValid;
    }

    // Bind real-time input validations to Panel 2 fields
    leadName.addEventListener('input', validatePanel2);
    leadMobile.addEventListener('input', validatePanel2);
    leadEmail.addEventListener('input', validatePanel2);

    // Submission handler: Let it download directly and reset calculator state
    leadForm.addEventListener('submit', function (e) {
        if (!validatePanel2()) {
            e.preventDefault();
            return;
        }
        
        // Form will submit and trigger direct file download from view.
        // Let's close the popup card after a short timeout so user sees it submitted
        setTimeout(() => {
            popupCard.classList.remove('open');
            // Reset wizard state back to panel 1
            panel2.classList.remove('active');
            panel1.classList.add('active');
            step2Indicator.classList.remove('active');
            step1Indicator.classList.add('active');
            // Clear inputs
            calcLoanAmount.value = '';
            calcInterestRate.value = '';
            calcTenure.value = '';
            calcProductType.value = '';
            resultsBox.style.display = 'none';
            toPanel2Btn.setAttribute('disabled', 'true');
            leadName.value = '';
            leadMobile.value = '';
            leadEmail.value = '';
            submitQuoteBtn.setAttribute('disabled', 'true');
        }, 1500);
    });
});
