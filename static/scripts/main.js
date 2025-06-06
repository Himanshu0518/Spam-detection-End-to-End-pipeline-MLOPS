  document.querySelectorAll('.option-card').forEach(card => {
            card.addEventListener('mouseenter', function() {
                this.style.transform = 'translateY(-5px) scale(1.02)';
            });
            
            card.addEventListener('mouseleave', function() {
                this.style.transform = 'translateY(0) scale(1)';
            });
        });

        // Add loading effect on click
        document.querySelectorAll('.option-card').forEach(card => {
            card.addEventListener('click', function(e) {
                const icon = this.querySelector('.option-icon i');
                icon.style.animation = 'spin 1s linear infinite';
                
                setTimeout(() => {
                    icon.style.animation = '';
                }, 1000);
            });
        });

        // Add CSS for spin animation
        const style = document.createElement('style');
        style.textContent = `
            @keyframes spin {
                from { transform: rotate(0deg); }
                to { transform: rotate(360deg); }
            }
        `;
        document.head.appendChild(style);