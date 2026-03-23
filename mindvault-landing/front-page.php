<?php /* front-page.php — Mind Vault AI — Sell Page */ ?>
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <meta name="description" content="Mind Vault AI — AI tools, e-books, trade tools, templates & development. Buy. Use. Earn. 30% affiliate program.">
  <title>Mind Vault AI — Buy. Use. Earn.</title>
  <script async src="https://www.googletagmanager.com/gtag/js?id=G-XXXXXXXXXX"></script>
  <script>window.dataLayer=window.dataLayer||[];function gtag(){dataLayer.push(arguments)}gtag('js',new Date());gtag('config','G-XXXXXXXXXX');</script>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700;800;900&display=swap" rel="stylesheet">
  <style>
    *{margin:0;padding:0;box-sizing:border-box}
    :root{
      --bg:#0a0e17;--card:#111822;--border:rgba(90,175,175,.12);
      --text:#f0f2f5;--muted:#7a8fa6;--dim:#4a5a70;
      --teal:#5aafaf;--gold:#c9a962;--green:#00c96e;--purple:#a855f7;--orange:#f97316;
    }
    html{scroll-behavior:smooth}
    body{font-family:'Inter',sans-serif;background:var(--bg);color:var(--text);line-height:1.5}
    a{text-decoration:none;color:inherit}

    /* NAV — compact */
    nav{position:fixed;top:0;width:100%;background:rgba(5,8,15,.92);backdrop-filter:blur(16px);border-bottom:1px solid var(--border);z-index:100}
    .nav-inner{max-width:1200px;margin:0 auto;padding:.7rem 1.5rem;display:flex;align-items:center;justify-content:space-between}
    .logo{font-size:1rem;font-weight:900;background:linear-gradient(135deg,var(--teal),#3d8a8a);-webkit-background-clip:text;-webkit-text-fill-color:transparent;background-clip:text}
    .nav-r{display:flex;gap:.5rem;align-items:center}
    .nav-r a{font-size:.82rem;font-weight:600;padding:.45rem 1rem;border-radius:7px;transition:all .2s}
    .btn-g{color:var(--muted);border:1px solid var(--border)}
    .btn-g:hover{color:var(--text);border-color:#444}
    .btn-p{background:var(--teal);color:#fff}
    .btn-p:hover{transform:translateY(-1px);box-shadow:0 6px 18px rgba(90,175,175,.3)}

    /* HERO — alles above the fold */
    .hero{min-height:100vh;display:flex;flex-direction:column;justify-content:center;padding:5rem 1.5rem 2rem;max-width:1200px;margin:0 auto}
    .hero-top{text-align:center;margin-bottom:2.5rem}
    .hero-badge{display:inline-block;padding:.3rem .8rem;background:rgba(90,175,175,.1);border:1px solid rgba(90,175,175,.2);border-radius:50px;color:var(--teal);font-size:.72rem;font-weight:700;letter-spacing:1px;text-transform:uppercase;margin-bottom:1rem}
    .hero h1{font-size:clamp(2rem,5vw,3.5rem);font-weight:900;letter-spacing:-2px;line-height:1.1;margin-bottom:.75rem}
    .hero h1 em{font-style:normal;background:linear-gradient(135deg,var(--teal),var(--purple));-webkit-background-clip:text;-webkit-text-fill-color:transparent;background-clip:text}
    .hero-sub{color:var(--muted);font-size:1rem;max-width:500px;margin:0 auto}

    /* PRODUCT GRID — direct zichtbaar, geen scrollen */
    .grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(200px,1fr));gap:.75rem}
    .card{background:var(--card);border:1px solid var(--border);border-radius:12px;padding:1.2rem;transition:all .25s;display:flex;flex-direction:column;cursor:pointer}
    .card:hover{border-color:rgba(90,175,175,.35);transform:translateY(-2px)}
    .card-top{display:flex;align-items:center;justify-content:space-between;margin-bottom:.6rem}
    .card-icon{font-size:1.5rem}
    .card-badge{font-size:.6rem;font-weight:700;padding:.15rem .5rem;border-radius:20px;text-transform:uppercase;letter-spacing:.5px}
    .badge-ebook{background:rgba(90,175,175,.12);color:var(--teal)}
    .badge-tool{background:rgba(201,169,98,.12);color:var(--gold)}
    .badge-saas{background:rgba(0,201,110,.12);color:var(--green)}
    .badge-bundle{background:rgba(168,85,247,.12);color:var(--purple)}
    .badge-service{background:rgba(249,115,22,.12);color:var(--orange)}
    .badge-free{background:rgba(0,201,110,.15);color:var(--green)}
    .card-title{font-size:.88rem;font-weight:800;margin-bottom:.25rem}
    .card-desc{font-size:.75rem;color:var(--muted);flex:1;margin-bottom:.6rem;line-height:1.4}
    .card-foot{display:flex;align-items:center;justify-content:space-between;padding-top:.6rem;border-top:1px solid var(--border)}
    .card-price{font-weight:900;font-size:.95rem;color:var(--teal)}
    .card-price .old{text-decoration:line-through;color:var(--dim);font-weight:400;font-size:.75rem;margin-right:.2rem}
    .card-btn{font-size:.72rem;font-weight:700;padding:.35rem .8rem;border-radius:6px;background:var(--teal);color:#fff;border:none;cursor:pointer;transition:all .2s}
    .card-btn:hover{transform:translateY(-1px);box-shadow:0 4px 12px rgba(90,175,175,.3)}
    .card-btn.gold{background:var(--gold);color:#000}
    .card-btn.green{background:var(--green);color:#000}
    .card-btn.purple{background:var(--purple);color:#fff}
    .card-btn.ghost{background:transparent;border:1px solid var(--border);color:var(--muted)}
    .card-btn.ghost:hover{border-color:var(--teal);color:var(--teal)}

    /* SECTIONS — compact */
    .section{padding:3rem 1.5rem;max-width:1200px;margin:0 auto}
    .section-dark{background:rgba(0,0,0,.3);border-top:1px solid var(--border);border-bottom:1px solid var(--border);max-width:100%;padding:3rem 0}
    .section-dark .section-inner{max-width:1200px;margin:0 auto;padding:0 1.5rem}
    .section-tag{color:var(--teal);font-size:.72rem;font-weight:700;text-transform:uppercase;letter-spacing:1.5px;margin-bottom:.5rem}
    .section h2{font-size:1.6rem;font-weight:900;letter-spacing:-1px;margin-bottom:.4rem}
    .section-sub{color:var(--muted);font-size:.88rem;margin-bottom:1.5rem}

    /* AFFILIATE BAR — compact horizontal */
    .aff-bar{display:flex;gap:1.5rem;align-items:center;flex-wrap:wrap}
    .aff-big{font-size:3rem;font-weight:900;color:var(--teal);line-height:1}
    .aff-info{flex:1;min-width:200px}
    .aff-info h3{font-size:1.1rem;font-weight:800;margin-bottom:.25rem}
    .aff-info p{font-size:.85rem;color:var(--muted)}
    .aff-perks{display:flex;gap:.5rem;flex-wrap:wrap;margin-top:.5rem}
    .aff-perk{font-size:.7rem;padding:.25rem .6rem;background:rgba(90,175,175,.08);border:1px solid var(--border);border-radius:20px;color:var(--muted)}

    /* SERVICES — horizontal compact */
    .svc-grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(220px,1fr));gap:.75rem}
    .svc{background:var(--card);border:1px solid var(--border);border-radius:10px;padding:1.2rem;transition:border-color .2s}
    .svc:hover{border-color:rgba(90,175,175,.3)}
    .svc-icon{font-size:1.3rem;margin-bottom:.5rem}
    .svc-name{font-size:.88rem;font-weight:800;margin-bottom:.25rem}
    .svc-desc{font-size:.75rem;color:var(--muted);margin-bottom:.5rem;line-height:1.4}
    .svc-price{font-size:.78rem;font-weight:700;color:var(--teal)}

    /* TRUST + SOCIAL — one line */
    .trust-row{display:flex;gap:1rem;align-items:center;justify-content:center;flex-wrap:wrap;padding:1.5rem;text-align:center}
    .trust-item{font-size:.78rem;color:var(--dim);font-weight:600}
    .social-row{display:flex;gap:.4rem;justify-content:center;flex-wrap:wrap;margin-top:1rem}
    .social-row a{width:32px;height:32px;border-radius:7px;background:var(--card);border:1px solid var(--border);display:flex;align-items:center;justify-content:center;color:var(--dim);font-size:.7rem;font-weight:700;transition:all .2s}
    .social-row a:hover{color:var(--teal);border-color:var(--teal)}

    /* FOOTER — minimal */
    footer{border-top:1px solid var(--border);padding:2rem 1.5rem;text-align:center}
    footer p{font-size:.75rem;color:var(--dim)}
    footer a{color:var(--dim);transition:color .2s}
    footer a:hover{color:var(--teal)}
    .footer-links{display:flex;gap:1rem;justify-content:center;flex-wrap:wrap;margin-bottom:.75rem}
    .footer-links a{font-size:.78rem;color:var(--muted)}

    /* RESPONSIVE */
    @media(max-width:768px){
      .grid{grid-template-columns:1fr 1fr}
      .aff-bar{flex-direction:column;text-align:center}
      .svc-grid{grid-template-columns:1fr}
      .hero h1{font-size:2rem}
    }
    @media(max-width:480px){
      .grid{grid-template-columns:1fr}
    }
  </style>
</head>
<body>

<nav>
  <div class="nav-inner">
    <a href="#" class="logo">MIND VAULT AI</a>
    <div class="nav-r">
      <a href="https://connexx.mindvault-ai.com/login" class="btn-g">Login</a>
      <a href="#products" class="btn-p">Shop</a>
    </div>
  </div>
</nav>

<div class="hero">
  <div class="hero-top">
    <div class="hero-badge">Digital Products &bull; AI Tools &bull; E-books &bull; Trade Tools</div>
    <h1>Buy. Use. <em>Earn more.</em></h1>
    <p class="hero-sub">AI tools, e-books, trade tools, templates &amp; custom development. Built from 23 years enterprise experience.</p>
  </div>

  <!-- ALLE PRODUCTEN — direct zichtbaar -->
  <div class="grid" id="products">

    <!-- E-BOOKS -->
    <a href="https://mindvault-ai.gumroad.com/l/ai-automation-guide" target="_blank" rel="noopener" class="card">
      <div class="card-top"><span class="card-icon">&#128218;</span><span class="card-badge badge-ebook">E-book</span></div>
      <div class="card-title">AI Automation for Business</div>
      <div class="card-desc">80+ pages. ChatGPT/Claude prompts, workflow automation, ROI calculations. No fluff.</div>
      <div class="card-foot"><span class="card-price"><span class="old">$29</span>$19</span><span class="card-btn">Buy</span></div>
    </a>

    <a href="https://mindvault-ai.gumroad.com/l/lean-six-sigma-handbook" target="_blank" rel="noopener" class="card">
      <div class="card-top"><span class="card-icon">&#9881;&#65039;</span><span class="card-badge badge-ebook">E-book</span></div>
      <div class="card-title">Lean Six Sigma Handbook</div>
      <div class="card-desc">DMAIC, control charts, sigma calcs. From real Tier 1 automotive experience.</div>
      <div class="card-foot"><span class="card-price">$24</span><span class="card-btn green">Buy</span></div>
    </a>

    <a href="https://mindvault-ai.gumroad.com/l/trading-psychology" target="_blank" rel="noopener" class="card">
      <div class="card-top"><span class="card-icon">&#128200;</span><span class="card-badge badge-ebook">E-book</span></div>
      <div class="card-title">Trading Psychology &amp; Risk</div>
      <div class="card-desc">Position sizing, stop-loss strategies, emotional traps. 60+ pages.</div>
      <div class="card-foot"><span class="card-price">$14</span><span class="card-btn gold">Buy</span></div>
    </a>

    <a href="https://mindvault-ai.gumroad.com/l/business-templates" target="_blank" rel="noopener" class="card">
      <div class="card-top"><span class="card-icon">&#128230;</span><span class="card-badge badge-bundle">50+ Bundle</span></div>
      <div class="card-title">Business Templates Bundle</div>
      <div class="card-desc">Unit economics, KPI dashboards, invoices, OKRs. Notion + Excel + Sheets.</div>
      <div class="card-foot"><span class="card-price"><span class="old">$49</span>$29</span><span class="card-btn purple">Buy</span></div>
    </a>

    <!-- TRADE TOOLS -->
    <a href="https://mindvault-ai.gumroad.com/l/portfolio-tracker" target="_blank" rel="noopener" class="card">
      <div class="card-top"><span class="card-icon">&#128202;</span><span class="card-badge badge-tool">Trade Tool</span></div>
      <div class="card-title">Portfolio Tracker Pro</div>
      <div class="card-desc">Multi-exchange P&amp;L tracking. Allocation view. Tax-ready export.</div>
      <div class="card-foot"><span class="card-price">$19</span><span class="card-btn gold">Buy</span></div>
    </a>

    <a href="https://mindvault-ai.gumroad.com/l/risk-management-kit" target="_blank" rel="noopener" class="card">
      <div class="card-top"><span class="card-icon">&#9878;&#65039;</span><span class="card-badge badge-tool">Trade Tool</span></div>
      <div class="card-title">Risk Management Kit</div>
      <div class="card-desc">Position sizing calculator, R:R tool, drawdown tracker. Never overexpose.</div>
      <div class="card-foot"><span class="card-price">$14</span><span class="card-btn gold">Buy</span></div>
    </a>

    <a href="https://mindvault-ai.gumroad.com/l/trade-journal" target="_blank" rel="noopener" class="card">
      <div class="card-top"><span class="card-icon">&#128209;</span><span class="card-badge badge-tool">Trade Tool</span></div>
      <div class="card-title">Trade Journal Template</div>
      <div class="card-desc">Auto-calculated win rate, profit factor, streaks. Notion + Excel.</div>
      <div class="card-foot"><span class="card-price">$9</span><span class="card-btn gold">Buy</span></div>
    </a>

    <a href="https://mindvault-ai.gumroad.com/l/market-analysis" target="_blank" rel="noopener" class="card">
      <div class="card-top"><span class="card-icon">&#128640;</span><span class="card-badge badge-tool">Trade Tool</span></div>
      <div class="card-title">Market Analysis Templates</div>
      <div class="card-desc">TA + fundamental frameworks. Screeners, watchlists, correlation maps.</div>
      <div class="card-foot"><span class="card-price">$19</span><span class="card-btn gold">Buy</span></div>
    </a>

    <!-- SAAS / PLATFORM -->
    <a href="https://connexx.mindvault-ai.com" target="_blank" rel="noopener" class="card">
      <div class="card-top"><span class="card-icon">&#9889;</span><span class="card-badge badge-free">Free Demo</span></div>
      <div class="card-title">Connexx Platform</div>
      <div class="card-desc">AI data platform. Analytics, API, Lean Six Sigma. Multi-tenant SaaS.</div>
      <div class="card-foot"><span class="card-price">Free &mdash; $299/mo</span><span class="card-btn">Try Free</span></div>
    </a>

    <a href="https://connexx.mindvault-ai.com/demo/darts501" target="_blank" rel="noopener" class="card">
      <div class="card-top"><span class="card-icon">&#127919;</span><span class="card-badge badge-free">Live Demo</span></div>
      <div class="card-title">Darts 501 Luxury</div>
      <div class="card-desc">Premium scorekeeping. Multiplayer, stats, luxury design. Play now.</div>
      <div class="card-foot"><span class="card-price">$9.99</span><span class="card-btn purple">Play &amp; Buy</span></div>
    </a>

    <a href="https://mindvault-ai.gumroad.com/l/mvai-process-tools" target="_blank" rel="noopener" class="card">
      <div class="card-top"><span class="card-icon">&#128736;&#65039;</span><span class="card-badge badge-saas">Standalone</span></div>
      <div class="card-title">Process Tools</div>
      <div class="card-desc">Lean Six Sigma toolkit. DMAIC, control charts, 8 wastes. Or incl. in Pro.</div>
      <div class="card-foot"><span class="card-price">$29</span><span class="card-btn green">Buy</span></div>
    </a>

    <a href="https://mindvault-ai.gumroad.com/l/mvai-business-intel" target="_blank" rel="noopener" class="card">
      <div class="card-top"><span class="card-icon">&#128202;</span><span class="card-badge badge-saas">Standalone</span></div>
      <div class="card-title">Business Intelligence</div>
      <div class="card-desc">Unit economics. LTV, CAC, churn prediction, MRR tracking.</div>
      <div class="card-foot"><span class="card-price">$29</span><span class="card-btn purple">Buy</span></div>
    </a>

  </div>
</div>

<!-- AFFILIATE — compact -->
<div class="section-dark">
  <div class="section-inner">
    <div class="aff-bar">
      <div class="aff-big">30%</div>
      <div class="aff-info">
        <h3>Affiliate Program &mdash; Earn with every sale</h3>
        <p>Recurring commission on Connexx subscriptions. One-time commission on all products. Monthly payouts via PayPal or crypto.</p>
        <div class="aff-perks">
          <span class="aff-perk">90-day cookie</span>
          <span class="aff-perk">Real-time dashboard</span>
          <span class="aff-perk">No minimum payout</span>
          <span class="aff-perk">Marketing materials included</span>
        </div>
      </div>
      <a href="mailto:info@mindvault-ai.com?subject=Affiliate Program" class="card-btn" style="padding:.7rem 1.5rem;font-size:.85rem">Apply Now</a>
    </div>
  </div>
</div>

<!-- DEVELOPMENT SERVICES — compact -->
<div class="section">
  <div class="section-tag">MVAI Development</div>
  <h2>Custom AI &amp; SaaS Solutions</h2>
  <p class="section-sub">23 years enterprise + AI. From concept to production.</p>
  <div class="svc-grid">
    <div class="svc">
      <div class="svc-icon">&#129302;</div>
      <div class="svc-name">AI Integration</div>
      <div class="svc-desc">Chatbots, data pipelines, workflow automation. Multi-provider.</div>
      <div class="svc-price">From &euro;2,500</div>
    </div>
    <div class="svc">
      <div class="svc-icon">&#128187;</div>
      <div class="svc-name">SaaS Development</div>
      <div class="svc-desc">Multi-tenant platforms, payments, API design. Full-stack.</div>
      <div class="svc-price">From &euro;5,000</div>
    </div>
    <div class="svc">
      <div class="svc-icon">&#9881;&#65039;</div>
      <div class="svc-name">Process Automation</div>
      <div class="svc-desc">ERP integrations, Lean Six Sigma, workflow optimization.</div>
      <div class="svc-price">From &euro;1,500</div>
    </div>
    <div class="svc">
      <div class="svc-icon">&#127912;</div>
      <div class="svc-name">White-Label</div>
      <div class="svc-desc">Our tech, your brand. Connexx, analytics, AI — rebranded.</div>
      <div class="svc-price">From &euro;3,000</div>
    </div>
  </div>
  <div style="text-align:center;margin-top:1.5rem">
    <a href="mailto:info@mindvault-ai.com?subject=Development inquiry" class="card-btn" style="padding:.7rem 1.5rem;font-size:.85rem">Discuss Your Project</a>
    <p style="color:var(--dim);font-size:.72rem;margin-top:.5rem">Free 30-min consultation &middot; NDA on request &middot; EU based</p>
  </div>
</div>

<!-- TRUST + SOCIAL + PAY -->
<div class="section-dark">
  <div class="section-inner" style="text-align:center">
    <div class="trust-row">
      <span class="trust-item">&#128274; GDPR Compliant</span>
      <span class="trust-item">&#127466;&#127482; EU Hosted</span>
      <span class="trust-item">&#128179; Gumroad</span>
      <span class="trust-item">&#127279;&#65039; PayPal</span>
      <span class="trust-item">&#8383; Crypto</span>
      <span class="trust-item">23+ Years Enterprise</span>
    </div>
    <div class="social-row">
      <a href="https://www.tiktok.com/@mindvaultai" target="_blank" rel="noopener" title="TikTok">TT</a>
      <a href="https://www.instagram.com/mindvaultai" target="_blank" rel="noopener" title="Instagram">IG</a>
      <a href="https://www.youtube.com/@mindvaultai" target="_blank" rel="noopener" title="YouTube">YT</a>
      <a href="https://x.com/mindvaultai" target="_blank" rel="noopener" title="X">X</a>
      <a href="https://www.linkedin.com/company/mindvault-ai" target="_blank" rel="noopener" title="LinkedIn">in</a>
      <a href="https://t.me/mindvaultai" target="_blank" rel="noopener" title="Telegram">TG</a>
      <a href="https://discord.gg/mindvaultai" target="_blank" rel="noopener" title="Discord">DS</a>
      <a href="https://www.reddit.com/r/mindvaultai" target="_blank" rel="noopener" title="Reddit">Re</a>
      <a href="https://www.facebook.com/mindvaultai" target="_blank" rel="noopener" title="Facebook">Fb</a>
      <a href="https://www.pinterest.com/mindvaultai" target="_blank" rel="noopener" title="Pinterest">Pi</a>
    </div>
  </div>
</div>

<!-- FOOTER — minimal -->
<footer>
  <div class="footer-links">
    <a href="https://connexx.mindvault-ai.com/login">Login</a>
    <a href="https://connexx.mindvault-ai.com">Connexx</a>
    <a href="https://mindvault-ai.gumroad.com" target="_blank" rel="noopener">Gumroad Shop</a>
    <a href="https://www.paypal.com/paypalme/mindvaultai" target="_blank" rel="noopener">PayPal</a>
    <a href="mailto:info@mindvault-ai.com">Contact</a>
    <a href="mailto:info@mindvault-ai.com?subject=Affiliate Program">Affiliate</a>
  </div>
  <p>&copy; 2026 Mind Vault AI &middot; info@mindvault-ai.com &middot; All rights reserved</p>
</footer>

<script>
document.querySelectorAll('a[href^="#"]').forEach(a=>{
  a.addEventListener('click',e=>{
    const t=document.querySelector(a.getAttribute('href'));
    if(t){e.preventDefault();t.scrollIntoView({behavior:'smooth'})}
  });
});
</script>
</body>
</html>
