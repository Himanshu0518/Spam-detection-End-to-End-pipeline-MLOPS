      // Form submission handling
        document.getElementById('fetchForm').addEventListener('submit', function(e) {
            const submitBtn = document.getElementById('submitBtn');
            const submitIcon = document.getElementById('submitIcon');
            const submitText = document.getElementById('submitText');
            
            // Disable button and show loading state
            submitBtn.disabled = true;
            submitIcon.classList.add('rotating');
            submitText.textContent = 'Fetching Emails...';
        });

        // Copy to clipboard function
        function copyToClipboard(text) {
            navigator.clipboard.writeText(text).then(function() {
                // Show feedback
                const button = event.target.closest('.action-btn');
                const originalText = button.innerHTML;
                button.innerHTML = '<i class="fas fa-check"></i> Copied!';
                button.style.background = '#4CAF50';
                
                setTimeout(() => {
                    button.innerHTML = originalText;
                    button.style.background = '#2196F3';
                }, 2000);
            });
        }

        // Toggle expand function
        function toggleExpand(button) {
            const emailContent = button.closest('.email-item').querySelector('.email-content');
            const icon = button.querySelector('i');
            
            if (emailContent.style.maxHeight === 'none') {
                emailContent.style.maxHeight = '150px';
                icon.classList.remove('fa-compress');
                icon.classList.add('fa-expand');
                button.querySelector('span') ? button.querySelector('span').textContent = ' Expand' : null;
            } else {
                emailContent.style.maxHeight = 'none';
                icon.classList.remove('fa-expand');
                icon.classList.add('fa-compress');
                button.querySelector('span') ? button.querySelector('span').textContent = ' Collapse' : null;
            }
        }