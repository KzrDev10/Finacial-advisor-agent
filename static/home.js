/* ---- NAV SCROLL ---- */
const nav = document.getElementById('main-nav');
window.addEventListener('scroll', () => {
    nav.classList.toggle('scrolled', window.scrollY > 50);
}, { passive: true });

/* ---- CURSOR GLOW ---- */
const cursorGlow = document.getElementById('cursor-glow');
document.addEventListener('mousemove', (e) => {
    cursorGlow.style.left = e.clientX + 'px';
    cursorGlow.style.top = e.clientY + 'px';
}, { passive: true });

/* ---- PARTICLE CANVAS ---- */
(function () {
    const canvas = document.getElementById('particle-canvas');
    const ctx = canvas.getContext('2d');
    let W, H, particles = [];
    const mouse = { x: -9999, y: -9999 };
    const REPEL_RADIUS = 120;
    const REPEL_STRENGTH = 4;

    document.addEventListener('mousemove', (e) => {
        mouse.x = e.clientX;
        mouse.y = e.clientY;
    }, { passive: true });

    function resize() {
        W = canvas.width = window.innerWidth;
        H = canvas.height = window.innerHeight;
    }
    resize();
    window.addEventListener('resize', resize, { passive: true });

    class Particle {
        constructor() { this.reset(); }
        reset() {
            this.x = Math.random() * W;
            this.y = Math.random() * H;
            this.r  = Math.random() * 1.5 + 0.3;
            this.vx = (Math.random() - 0.5) * 0.25;
            this.vy = (Math.random() - 0.5) * 0.25;
            this.alpha = Math.random() * 0.4 + 0.05;
            this.color = Math.random() > 0.5 ? '0,212,255' : '57,255,110';
        }
        update() {
            // Cursor repulsion
            const dx = this.x - mouse.x;
            const dy = this.y - mouse.y;
            const dist = Math.sqrt(dx * dx + dy * dy);
            if (dist < REPEL_RADIUS && dist > 0) {
                const force = (REPEL_RADIUS - dist) / REPEL_RADIUS;
                this.x += (dx / dist) * force * REPEL_STRENGTH;
                this.y += (dy / dist) * force * REPEL_STRENGTH;
            }
            this.x += this.vx;
            this.y += this.vy;
            if (this.x < 0 || this.x > W || this.y < 0 || this.y > H) this.reset();
        }
        draw() {
            ctx.beginPath();
            ctx.arc(this.x, this.y, this.r, 0, Math.PI * 2);
            ctx.fillStyle = `rgba(${this.color},${this.alpha})`;
            ctx.fill();
        }
    }

    for (let i = 0; i < 280; i++) particles.push(new Particle());

    function loop() {
        ctx.clearRect(0, 0, W, H);
        particles.forEach(p => { p.update(); p.draw(); });

        // Draw connecting lines
        for (let i = 0; i < particles.length; i++) {
            for (let j = i + 1; j < particles.length; j++) {
                const dx = particles[i].x - particles[j].x;
                const dy = particles[i].y - particles[j].y;
                const dist = Math.sqrt(dx * dx + dy * dy);
                if (dist < 130) {
                    ctx.beginPath();
                    ctx.strokeStyle = `rgba(0,212,255,${0.18 * (1 - dist / 130)})`;
                    ctx.lineWidth = 0.5;
                    ctx.moveTo(particles[i].x, particles[i].y);
                    ctx.lineTo(particles[j].x, particles[j].y);
                    ctx.stroke();
                }
            }
        }
        requestAnimationFrame(loop);
    }
    loop();
})();

/* ---- TICKER ---- */
const tickers = [
    { sym: 'AAPL', price: '$198.42', change: '+1.24%', up: true },
    { sym: 'NVDA', price: '$875.10', change: '+3.82%', up: true },
    { sym: 'BTC', price: '$67,320', change: '-0.94%', up: false },
    { sym: 'TSLA', price: '$248.66', change: '+2.17%', up: true },
    { sym: 'ETH', price: '$3,480', change: '-1.31%', up: false },
    { sym: 'MSFT', price: '$415.22', change: '+0.68%', up: true },
    { sym: 'GOOGL', price: '$176.34', change: '+1.05%', up: true },
    { sym: 'AMZN', price: '$192.11', change: '-0.43%', up: false },
    { sym: 'SPY', price: '$538.90', change: '+0.82%', up: true },
    { sym: 'GLD', price: '$218.55', change: '+0.15%', up: true },
];

const track = document.getElementById('ticker-track');
// Duplicate for infinite scroll
[...tickers, ...tickers].forEach((t, i) => {
    const item = document.createElement('div');
    item.className = 'ticker-item';
    item.innerHTML = `
        <span class="ticker-symbol">${t.sym}</span>
        <span class="ticker-price">${t.price}</span>
        <span class="ticker-change ${t.up ? 'up' : 'down'}">${t.change}</span>
        ${i < [...tickers, ...tickers].length - 1 ? '<div class="ticker-divider"></div>' : ''}
      `;
    track.appendChild(item);
});

/* ---- SCROLL REVEAL ---- */
const reveals = document.querySelectorAll('.reveal');
const observer = new IntersectionObserver((entries) => {
    entries.forEach(e => {
        if (e.isIntersecting) {
            e.target.classList.add('is-visible');
            observer.unobserve(e.target);
        }
    });
}, { threshold: 0.12 });
reveals.forEach(el => observer.observe(el));

/* ---- COUNTER ANIMATION ---- */
function animateCounter(el, target, prefix = '', suffix = '') {
    const duration = 1800;
    const start = performance.now();
    const isFloat = !Number.isInteger(target);
    function update(now) {
        const elapsed = now - start;
        const progress = Math.min(elapsed / duration, 1);
        const ease = 1 - Math.pow(1 - progress, 3);
        const val = target * ease;
        el.textContent = prefix + (isFloat ? val.toFixed(1) : Math.floor(val)) + suffix;
        if (progress < 1) requestAnimationFrame(update);
    }
    requestAnimationFrame(update);
}

const counterObserver = new IntersectionObserver((entries) => {
    entries.forEach(e => {
        if (e.isIntersecting) {
            const target = parseFloat(e.target.dataset.target);
            const id = e.target.id;
            if (id === 'stat-aum') animateCounter(e.target, target, '$', 'B+');
            if (id === 'stat-users') animateCounter(e.target, target, '', 'K+');
            if (id === 'stat-return') animateCounter(e.target, target, '', '%');
            if (id === 'stat-uptime') animateCounter(e.target, target, '', '%');
            counterObserver.unobserve(e.target);
        }
    });
}, { threshold: 0.5 });
document.querySelectorAll('[data-target]').forEach(el => counterObserver.observe(el));

/* ---- ANIMATE CHART LINE ---- */
(function () {
    const path = document.querySelector('.chart-line-path');
    if (!path) return;
    const len = path.getTotalLength();
    path.style.strokeDasharray = len;
    path.style.strokeDashoffset = len;
    path.style.transition = 'stroke-dashoffset 2s cubic-bezier(0.16,1,0.3,1) 0.5s';

    const chartObs = new IntersectionObserver((entries) => {
        entries.forEach(e => {
            if (e.isIntersecting) {
                path.style.strokeDashoffset = 0;
                chartObs.unobserve(e.target);
            }
        });
    }, { threshold: 0.3 });
    chartObs.observe(path);
})();

/* ---- FEATURE WIDE VISUAL (animated bars) ---- */
(function () {
    const vis = document.getElementById('feature-wide-visual');
    if (!vis) return;
    const bars = ['NYSE', 'NASDAQ', 'LSE', 'TSE', 'SSE', 'BSE', 'ASX', 'FSE'];
    vis.style.display = 'flex';
    vis.style.alignItems = 'flex-end';
    vis.style.gap = '6px';
    vis.style.padding = '1rem';
    bars.forEach((label, i) => {
        const heights = [55, 80, 40, 70, 90, 60, 75, 45];
        const colors = ['#00d4ff', '#39ff6e', '#7c3aed', '#fbbf24', '#00d4ff', '#39ff6e', '#f87171', '#7c3aed'];
        const wrap = document.createElement('div');
        wrap.style.cssText = `flex:1;display:flex;flex-direction:column;align-items:center;gap:4px;`;
        const bar = document.createElement('div');
        bar.style.cssText = `
          width:100%;height:${heights[i]}%;border-radius:4px 4px 0 0;
          background:${colors[i]};opacity:0.5;
          transition:height 0.5s cubic-bezier(0.16,1,0.3,1) ${i * 0.06}s, opacity 0.3s;
        `;
        const lbl = document.createElement('span');
        lbl.textContent = label;
        lbl.style.cssText = 'font-size:0.6rem;color:rgba(255,255,255,0.4);letter-spacing:0.05em;';
        bar.addEventListener('mouseenter', () => { bar.style.opacity = '0.9'; });
        bar.addEventListener('mouseleave', () => { bar.style.opacity = '0.5'; });
        wrap.appendChild(bar);
        wrap.appendChild(lbl);
        vis.appendChild(wrap);
    });
})();

/* ---- CTA EMAIL SUBMIT ---- */
document.getElementById('cta-submit-btn').addEventListener('click', function () {
    const input = document.getElementById('cta-email-input');
    if (input.value && input.value.includes('@')) {
        this.textContent = '🎉 Welcome aboard!';
        this.style.background = '#39ff6e';
        this.style.cursor = 'default';
        input.value = '';
        input.placeholder = "You're on the list!";
        setTimeout(() => {
            this.textContent = 'Get started';
            input.placeholder = 'Enter your email address';
        }, 4000);
    } else {
        input.style.borderColor = '#ff5f5f';
        setTimeout(() => { input.style.borderColor = ''; }, 2000);
    }
});

/* ---- SMOOTH SCROLL FOR ANCHOR LINKS ---- */
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
        const target = document.querySelector(this.getAttribute('href'));
        if (target) {
            e.preventDefault();
            target.scrollIntoView({ behavior: 'smooth', block: 'start' });
        }
    });
});