/**
 * GitHub Portfolio Analyzer - Main JavaScript
 */

document.addEventListener('DOMContentLoaded', function() {
    
    // Form submission with loading state
    const analyzeForm = document.getElementById('analyzeForm');
    const analyzeBtn = document.getElementById('analyzeBtn');
    const usernameInput = document.getElementById('usernameInput');
    
    if (analyzeForm) {
        analyzeForm.addEventListener('submit', function(e) {
            if (analyzeBtn) {
                analyzeBtn.disabled = true;
                analyzeBtn.innerHTML = `
                    <span class="spinner-border spinner-border-sm me-2" role="status"></span>
                    Analyzing...
                `;
            }
        });
    }
    
    // Username input validation
    if (usernameInput) {
        usernameInput.addEventListener('input', function() {
            const value = this.value.trim();
            
            // Remove any spaces
            this.value = value.replace(/\s/g, '');
            
            // Visual feedback
            if (value.length > 0) {
                this.classList.add('is-valid');
                this.classList.remove('is-invalid');
            } else {
                this.classList.remove('is-valid');
            }
        });
    }
    
    // Copy code blocks
    document.querySelectorAll('pre code').forEach(function(codeBlock) {
        const pre = codeBlock.parentElement;
        
        const copyButton = document.createElement('button');
        copyButton.className = 'btn btn-sm btn-outline-light position-absolute top-0 end-0 m-2';
        copyButton.innerHTML = '<i class="bi bi-clipboard"></i>';
        copyButton.title = 'Copy to clipboard';
        
        pre.style.position = 'relative';
        pre.appendChild(copyButton);
        
        copyButton.addEventListener('click', function() {
            navigator.clipboard.writeText(codeBlock.textContent).then(function() {
                copyButton.innerHTML = '<i class="bi bi-check"></i>';
                setTimeout(function() {
                    copyButton.innerHTML = '<i class="bi bi-clipboard"></i>';
                }, 2000);
            });
        });
    });
    
    // Smooth scroll for anchor links
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function(e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                target.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    });
    
    // Progress bar animation on results page
    document.querySelectorAll('.progress-bar').forEach(function(bar) {
        const width = bar.style.width;
        bar.style.width = '0%';
        setTimeout(function() {
            bar.style.transition = 'width 1s ease-out';
            bar.style.width = width;
        }, 200);
    });
    
    // Tooltips initialization (Bootstrap)
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map(function(tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });
    
});

/**
 * API Helper Functions
 */
const API = {
    /**
     * Analyze a GitHub profile via API
     */
    analyze: async function(username, token = null) {
        try {
            const response = await fetch('/api/analyze', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    username: username,
                    token: token
                })
            });
            
            return await response.json();
        } catch (error) {
            console.error('API Error:', error);
            throw error;
        }
    }
};

/**
 * Utility Functions
 */
const Utils = {
    /**
     * Format large numbers
     */
    formatNumber: function(num) {
        if (num >= 1000000) {
            return (num / 1000000).toFixed(1) + 'M';
        } else if (num >= 1000) {
            return (num / 1000).toFixed(1) + 'K';
        }
        return num.toString();
    },
    
    /**
     * Debounce function
     */
    debounce: function(func, wait) {
        let timeout;
        return function(...args) {
            clearTimeout(timeout);
            timeout = setTimeout(() => func.apply(this, args), wait);
        };
    }
};