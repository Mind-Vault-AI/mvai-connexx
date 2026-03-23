<?php /* front-page.php — Mind Vault AI */ ?>
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <meta name="description" content="Mind Vault AI — AI tools, e-books, trade tools, templates &amp; custom development. Digital products that work. 30% affiliate program. Buy, use, earn.">
  <title>Mind Vault AI — Digital Products, AI Tools &amp; E-books</title>
  <!-- GA4 — replace G-XXXXXXXXXX with your property ID -->
  <script async src="https://www.googletagmanager.com/gtag/js?id=G-XXXXXXXXXX"></script>
  <script>window.dataLayer=window.dataLayer||[];function gtag(){dataLayer.push(arguments)}gtag('js',new Date());gtag('config','G-XXXXXXXXXX');</script>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&display=swap" rel="stylesheet">
  <style>
    *, *::before, *::after { margin: 0; padding: 0; box-sizing: border-box; }

    :root {
      --bg:        #0f1520;
      --bg-card:   #12181e;
      --bg-alt:    #0b1018;
      --border:    rgba(90,175,175,0.12);
      --border-h:  rgba(90,175,175,0.35);
      --text:      #f0f2f5;
      --muted:     #7a8fa6;
      --dim:       #4a5a70;
      --connexx:   #5aafaf;
      --connexx-d: #3d8a8a;
      --apex:      #c9a962;
      --darts:     #a855f7;
      --process:   #00c96e;
      --mobile:    #f97316;
      --tr: 0.3s cubic-bezier(.4,0,.2,1);
    }

    html { scroll-behavior: smooth; }
    body { font-family: 'Inter', -apple-system, sans-serif; background: var(--bg); color: var(--text); overflow-x: hidden; line-height: 1.6; }

    /* ─── SOCIAL FLOATING BAR ───────────────────── */
    .social-float {
      position: fixed; right: 1.2rem; top: 50%; transform: translateY(-50%);
      display: flex; flex-direction: column; gap: .6rem; z-index: 900;
    }
    .social-float a {
      width: 36px; height: 36px; border-radius: 8px;
      background: var(--bg-card); border: 1px solid var(--border);
      display: flex; align-items: center; justify-content: center;
      color: var(--muted); text-decoration: none; font-size: .85rem;
      transition: all .2s; font-weight: 700;
    }
    .social-float a:hover { border-color: var(--connexx); color: var(--connexx); transform: scale(1.1); }

    /* ─── NAV ───────────────────────────────────── */
    nav {
      position: fixed; top: 0; width: 100%;
      background: rgba(5,8,15,.9); backdrop-filter: blur(20px);
      border-bottom: 1px solid var(--border); z-index: 1000;
    }
    .nav-inner {
      max-width: 1300px; margin: 0 auto; padding: .85rem 2rem;
      display: flex; align-items: center; justify-content: space-between;
    }
    .logo {
      font-size: 1.1rem; font-weight: 900; letter-spacing: -1px;
      background: linear-gradient(135deg, #5aafaf, #3d8a8a);
      -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text;
      text-decoration: none;
    }
    .nav-links { display: flex; gap: 1.5rem; list-style: none; }
    .nav-links a { color: var(--muted); text-decoration: none; font-size: .88rem; font-weight: 500; transition: color .2s; }
    .nav-links a:hover { color: var(--text); }
    .nav-actions { display: flex; gap: .6rem; align-items: center; }
    .btn {
      display: inline-flex; align-items: center; gap: .4rem;
      padding: .55rem 1.2rem; border-radius: 8px;
      font-weight: 600; font-size: .88rem; text-decoration: none;
      border: none; cursor: pointer; transition: all .25s;
    }
    .btn-ghost { color: var(--muted); background: transparent; border: 1px solid var(--border); }
    .btn-ghost:hover { color: var(--text); border-color: #3a4a5a; }
    .btn-primary { background: linear-gradient(135deg, #5aafaf, #3d8a8a); color: #fff; }
    .btn-primary:hover { transform: translateY(-1px); box-shadow: 0 8px 20px rgba(90,175,175,.3); }
    .hamburger { display: none; background: none; border: none; color: var(--text); font-size: 1.4rem; cursor: pointer; }

    /* ─── HERO ──────────────────────────────────── */
    .hero {
      min-height: 100vh; display: flex; align-items: center; justify-content: center;
      padding: 8rem 2rem 5rem; position: relative; overflow: hidden;
    }
    .hero::before {
      content: ''; position: absolute; inset: 0;
      background:
        radial-gradient(ellipse 80% 60% at 50% -10%, rgba(90,175,175,.12) 0%, transparent 60%),
        radial-gradient(ellipse 50% 40% at 85% 100%, rgba(168,85,247,.07) 0%, transparent 50%),
        radial-gradient(ellipse 40% 30% at 5% 80%, rgba(0,201,110,.05) 0%, transparent 50%);
      pointer-events: none;
    }
    .hero-inner { max-width: 860px; text-align: center; position: relative; z-index: 1; }
    .hero-badge {
      display: inline-block; padding: .4rem 1rem;
      background: rgba(90,175,175,.1); border: 1px solid rgba(90,175,175,.25);
      border-radius: 50px; color: var(--connexx);
      font-size: .78rem; font-weight: 700; letter-spacing: 1px;
      text-transform: uppercase; margin-bottom: 2rem;
    }
    .hero h1 {
      font-size: clamp(2.6rem, 7vw, 5rem); font-weight: 900;
      line-height: 1.05; letter-spacing: -3px; margin-bottom: 1.5rem;
    }
    .hero h1 .grad {
      background: linear-gradient(135deg, #5aafaf 0%, #3d8a8a 40%, #a855f7 100%);
      -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text;
    }
    .hero p { font-size: 1.15rem; color: var(--muted); max-width: 580px; margin: 0 auto 2.5rem; }
    .hero-ctas { display: flex; gap: 1rem; justify-content: center; flex-wrap: wrap; margin-bottom: 2.5rem; }
    .btn-big { padding: .9rem 2.2rem; font-size: 1rem; border-radius: 10px; }
    .trust-badges { display: flex; gap: 1.5rem; justify-content: center; flex-wrap: wrap; }
    .trust-badge {
      display: flex; align-items: center; gap: .5rem;
      color: var(--dim); font-size: .82rem; font-weight: 500;
    }
    .trust-badge span { color: var(--muted); }

    /* ─── STATS BAR ─────────────────────────────── */
    .stats-bar {
      background: var(--bg-alt); border-top: 1px solid var(--border); border-bottom: 1px solid var(--border);
      padding: 2rem;
    }
    .stats-grid { max-width: 900px; margin: 0 auto; display: grid; grid-template-columns: repeat(4, 1fr); gap: 2rem; text-align: center; }
    .stat-num { font-size: 2rem; font-weight: 900; color: var(--connexx); letter-spacing: -1px; }
    .stat-label { font-size: .82rem; color: var(--muted); margin-top: .25rem; }

    /* ─── SECTION WRAPPER ───────────────────────── */
    section { padding: 5rem 2rem; }
    .section-inner { max-width: 1200px; margin: 0 auto; }
    .section-label {
      display: inline-flex; align-items: center; gap: .5rem;
      color: var(--connexx); font-size: .8rem; font-weight: 700;
      text-transform: uppercase; letter-spacing: 1.5px; margin-bottom: 1rem;
    }
    .section-label::before { content: ''; width: 24px; height: 2px; background: var(--connexx); }
    h2 { font-size: clamp(1.8rem, 4vw, 2.8rem); font-weight: 900; letter-spacing: -1.5px; margin-bottom: 1rem; }
    .section-sub { color: var(--muted); font-size: 1.05rem; max-width: 560px; margin-bottom: 3rem; }

    /* ─── PRODUCT TILES ─────────────────────────── */
    .tiles-row {
      display: flex; gap: 1px; background: var(--border);
      border-radius: 16px; overflow: hidden;
      height: 260px;
    }
    .tile {
      flex: 1; background: var(--bg-card); padding: 2rem 1.5rem;
      display: flex; flex-direction: column; justify-content: space-between;
      cursor: pointer; transition: flex .4s var(--tr), background .3s;
      position: relative; overflow: hidden; min-width: 80px;
    }
    .tile:hover { flex: 3; }
    .tile::before {
      content: ''; position: absolute; inset: 0; opacity: 0;
      transition: opacity .4s;
    }
    .tile:hover::before { opacity: 1; }
    .tile-connexx::before { background: linear-gradient(135deg, rgba(90,175,175,.08), transparent); }
    .tile-apex::before    { background: linear-gradient(135deg, rgba(201,169,98,.08), transparent); }
    .tile-darts::before   { background: linear-gradient(135deg, rgba(168,85,247,.08), transparent); }
    .tile-process::before { background: linear-gradient(135deg, rgba(0,201,110,.08), transparent); }
    .tile-mobile::before  { background: linear-gradient(135deg, rgba(249,115,22,.08), transparent); }

    .tile-icon { font-size: 1.8rem; }
    .tile-name { font-size: 1rem; font-weight: 800; letter-spacing: -.5px; white-space: nowrap; }
    .tile-connexx .tile-name { color: var(--connexx); }
    .tile-apex .tile-name    { color: var(--apex); }
    .tile-darts .tile-name   { color: var(--darts); }
    .tile-process .tile-name { color: var(--process); }
    .tile-mobile .tile-name  { color: var(--mobile); }
    .tile-sub { font-size: .78rem; color: var(--muted); margin-top: .25rem; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
    .tile-cta {
      display: inline-flex; align-items: center; gap: .4rem;
      font-size: .8rem; font-weight: 700; text-decoration: none;
      opacity: 0; transform: translateY(8px); transition: all .3s .1s;
      padding: .4rem .8rem; border-radius: 6px;
    }
    .tile:hover .tile-cta { opacity: 1; transform: translateY(0); }
    .tile-connexx .tile-cta { color: var(--connexx); background: rgba(90,175,175,.12); }
    .tile-apex .tile-cta    { color: var(--apex); background: rgba(201,169,98,.12); }
    .tile-darts .tile-cta   { color: var(--darts); background: rgba(168,85,247,.12); }
    .tile-process .tile-cta { color: var(--process); background: rgba(0,201,110,.12); }
    .tile-mobile .tile-cta  { color: var(--mobile); background: rgba(249,115,22,.12); }

    /* ─── CONNEXX FEATURED ──────────────────────── */
    .featured-grid {
      display: grid; grid-template-columns: 1fr 380px; gap: 3rem; align-items: start;
    }
    .featured-label {
      display: inline-flex; align-items: center; gap: .6rem;
      color: var(--connexx); font-size: .85rem; font-weight: 700;
      text-transform: uppercase; letter-spacing: 1px; margin-bottom: 1.2rem;
    }
    .featured-label .dot { width: 8px; height: 8px; border-radius: 50%; background: var(--connexx); animation: pulse 2s infinite; }
    @keyframes pulse { 0%,100%{opacity:1}50%{opacity:.3} }
    .feature-list { list-style: none; display: grid; grid-template-columns: 1fr 1fr; gap: .6rem; margin: 1.5rem 0; }
    .feature-list li {
      display: flex; align-items: center; gap: .6rem;
      font-size: .88rem; color: var(--muted); padding: .5rem .75rem;
      background: var(--bg-card); border-radius: 8px; border: 1px solid var(--border);
    }
    .feature-list li::before { content: '✓'; color: var(--connexx); font-weight: 700; flex-shrink: 0; }
    .feature-list li.highlight { border-color: rgba(90,175,175,.25); color: var(--text); }
    .feature-list li.highlight::before { content: '★'; color: #c9a962; }

    /* Terminal mockup */
    .terminal {
      background: #080c12; border-radius: 12px; overflow: hidden;
      border: 1px solid var(--border); font-family: 'Courier New', monospace;
    }
    .terminal-bar {
      background: #0d1117; padding: .65rem 1rem;
      display: flex; align-items: center; gap: .5rem; border-bottom: 1px solid var(--border);
    }
    .t-dot { width: 10px; height: 10px; border-radius: 50%; }
    .t-title { font-size: .78rem; color: var(--dim); margin-left: .5rem; }
    .terminal-body { padding: 1.2rem; font-size: .8rem; line-height: 1.8; }
    .t-dim   { color: var(--dim); }
    .t-grn   { color: #00c96e; }
    .t-teal  { color: var(--connexx); }
    .t-gold  { color: #c9a962; }
    .t-purp  { color: #a855f7; }
    .t-muted { color: var(--muted); }

    /* Buy panel */
    .buy-panel {
      background: var(--bg-card); border: 1px solid var(--border);
      border-radius: 16px; padding: 1.8rem; position: sticky; top: 5rem;
    }
    .buy-panel h3 { font-size: 1rem; font-weight: 700; margin-bottom: 1.2rem; }
    .tier {
      padding: .8rem 1rem; border-radius: 10px; border: 1px solid var(--border);
      margin-bottom: .6rem; cursor: pointer; transition: all .2s;
      display: flex; align-items: center; justify-content: space-between;
    }
    .tier:hover { border-color: var(--connexx); background: rgba(90,175,175,.05); }
    .tier.popular { border-color: var(--connexx); background: rgba(90,175,175,.07); }
    .tier-name { font-size: .88rem; font-weight: 700; }
    .tier-price { font-size: .88rem; font-weight: 700; color: var(--connexx); }
    .tier-sub { font-size: .72rem; color: var(--muted); margin-top: .15rem; }
    .popular-badge {
      font-size: .68rem; font-weight: 700; color: var(--connexx);
      background: rgba(90,175,175,.15); padding: .15rem .5rem; border-radius: 20px;
      text-transform: uppercase; letter-spacing: .5px;
    }
    .buy-cta { width: 100%; margin-top: 1.2rem; justify-content: center; padding: .9rem; font-size: .95rem; border-radius: 10px; }
    .pay-methods { display: flex; gap: .5rem; justify-content: center; margin-top: 1rem; flex-wrap: wrap; }
    .pay-pill {
      font-size: .72rem; color: var(--dim); background: rgba(255,255,255,.04);
      border: 1px solid var(--border); padding: .2rem .6rem; border-radius: 20px;
    }

    /* ─── PRODUCTS GRID ─────────────────────────── */
    .products-grid { display: grid; grid-template-columns: repeat(2, 1fr); gap: 1.5rem; }
    .product-card {
      background: var(--bg-card); border: 1px solid var(--border);
      border-radius: 16px; padding: 1.8rem; transition: all .3s;
    }
    .product-card:hover { border-color: rgba(90,175,175,.3); transform: translateY(-3px); }
    .product-card-header { display: flex; align-items: center; gap: 1rem; margin-bottom: 1.2rem; }
    .product-icon { font-size: 2rem; }
    .product-title { font-size: 1.1rem; font-weight: 800; }
    .product-price { font-size: .85rem; font-weight: 600; margin-top: .15rem; }
    .product-apex .product-price    { color: var(--apex); }
    .product-darts .product-price   { color: var(--darts); }
    .product-process .product-price { color: var(--process); }
    .product-intel .product-price   { color: #a855f7; }
    .product-mobile .product-price  { color: var(--mobile); }
    .product-desc { font-size: .88rem; color: var(--muted); margin-bottom: 1.2rem; line-height: 1.6; }
    .feature-tags { display: flex; flex-wrap: wrap; gap: .4rem; margin-bottom: 1.2rem; }
    .tag {
      font-size: .72rem; font-weight: 600; padding: .2rem .65rem;
      border-radius: 20px; background: rgba(90,175,175,.08);
      border: 1px solid rgba(90,175,175,.15); color: var(--muted);
    }
    .product-actions { display: flex; gap: .6rem; }
    .btn-sm { padding: .45rem 1rem; font-size: .82rem; border-radius: 7px; }
    .btn-outline-teal { border: 1px solid rgba(90,175,175,.3); color: var(--connexx); background: transparent; }
    .btn-outline-teal:hover { background: rgba(90,175,175,.08); }
    .btn-outline-apex  { border: 1px solid rgba(201,169,98,.3); color: var(--apex); background: transparent; }
    .btn-outline-darts { border: 1px solid rgba(168,85,247,.3); color: var(--darts); background: transparent; }
    .btn-outline-green { border: 1px solid rgba(0,201,110,.3); color: var(--process); background: transparent; }
    .btn-outline-orange{ border: 1px solid rgba(249,115,22,.3); color: var(--mobile); background: transparent; }

    /* ─── LOGIN SECTION ─────────────────────────── */
    .login-section { background: var(--bg-alt); border-top: 1px solid var(--border); border-bottom: 1px solid var(--border); }
    .login-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 4rem; align-items: center; }
    .login-providers { display: flex; flex-direction: column; gap: .8rem; }
    .login-btn {
      display: flex; align-items: center; gap: 1rem; padding: .9rem 1.4rem;
      border-radius: 10px; border: 1px solid var(--border); background: var(--bg-card);
      color: var(--text); text-decoration: none; font-size: .92rem; font-weight: 600;
      transition: all .25s; cursor: pointer;
    }
    .login-btn:hover { border-color: var(--connexx); background: rgba(90,175,175,.06); transform: translateX(4px); }
    .login-btn-icon { width: 28px; height: 28px; border-radius: 6px; display: flex; align-items: center; justify-content: center; font-size: 1rem; }
    .login-or {
      text-align: center; color: var(--dim); font-size: .82rem; position: relative; margin: .4rem 0;
    }
    .login-or::before, .login-or::after {
      content: ''; position: absolute; top: 50%; width: 42%; height: 1px; background: var(--border);
    }
    .login-or::before { left: 0; } .login-or::after { right: 0; }
    .email-form { display: flex; gap: .6rem; margin-top: .4rem; }
    .email-form input {
      flex: 1; padding: .75rem 1rem; background: var(--bg-card);
      border: 1px solid var(--border); border-radius: 8px; color: var(--text);
      font-family: inherit; font-size: .9rem; outline: none; transition: border-color .2s;
    }
    .email-form input:focus { border-color: var(--connexx); }
    .email-form input::placeholder { color: var(--dim); }

    /* ─── NEWSLETTER ────────────────────────────── */
    .newsletter-wrap {
      background: linear-gradient(135deg, rgba(90,175,175,.06), rgba(168,85,247,.04));
      border: 1px solid var(--border-h); border-radius: 20px;
      padding: 3rem; text-align: center; max-width: 620px; margin: 0 auto;
    }
    .newsletter-wrap h3 { font-size: 1.6rem; font-weight: 800; letter-spacing: -1px; margin-bottom: .75rem; }
    .newsletter-wrap p { color: var(--muted); margin-bottom: 1.5rem; }
    .nl-form { display: flex; gap: .6rem; max-width: 420px; margin: 0 auto; }
    .nl-form input {
      flex: 1; padding: .8rem 1.1rem; background: var(--bg-card);
      border: 1px solid var(--border); border-radius: 9px; color: var(--text);
      font-family: inherit; font-size: .9rem; outline: none; transition: border-color .2s;
    }
    .nl-form input:focus { border-color: var(--connexx); }
    .nl-form input::placeholder { color: var(--dim); }
    .nl-gdpr { font-size: .72rem; color: var(--dim); margin-top: .8rem; }

    /* ─── CLIENTS ───────────────────────────────── */
    .clients-row { display: flex; gap: 1.5rem; flex-wrap: wrap; align-items: center; justify-content: center; }
    .client-badge {
      padding: .6rem 1.4rem; background: var(--bg-card);
      border: 1px solid var(--border); border-radius: 8px;
      font-size: .88rem; font-weight: 700; color: var(--muted);
      letter-spacing: .5px; transition: all .2s;
    }
    .client-badge:hover { color: var(--text); border-color: var(--connexx); }

    /* ─── ABOUT ─────────────────────────────────── */
    .about-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 4rem; align-items: start; }
    .about-text p { color: var(--muted); margin-bottom: 1rem; line-height: 1.8; }
    .about-stats { display: grid; grid-template-columns: 1fr 1fr; gap: 1rem; margin-top: 2rem; }
    .about-stat {
      background: var(--bg-card); border: 1px solid var(--border);
      border-radius: 12px; padding: 1.2rem;
    }
    .about-stat-num { font-size: 1.8rem; font-weight: 900; color: var(--connexx); }
    .about-stat-label { font-size: .78rem; color: var(--muted); margin-top: .2rem; }
    .expertise-tags { display: flex; flex-wrap: wrap; gap: .5rem; }
    .exp-tag {
      font-size: .78rem; font-weight: 600; padding: .3rem .8rem;
      border-radius: 6px; background: var(--bg-card);
      border: 1px solid var(--border); color: var(--muted);
    }

    /* ─── CONTACT ───────────────────────────────── */
    .contact-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 4rem; }
    .contact-info { display: flex; flex-direction: column; gap: 1rem; }
    .contact-item {
      display: flex; align-items: center; gap: 1rem; padding: 1rem 1.2rem;
      background: var(--bg-card); border: 1px solid var(--border);
      border-radius: 10px; text-decoration: none; color: var(--text);
      transition: all .2s;
    }
    .contact-item:hover { border-color: var(--connexx); }
    .contact-item-icon { font-size: 1.2rem; width: 36px; text-align: center; }
    .contact-item-label { font-size: .78rem; color: var(--dim); }
    .contact-item-val { font-size: .9rem; font-weight: 600; }
    .contact-form { display: flex; flex-direction: column; gap: .8rem; }
    .contact-form-row { display: grid; grid-template-columns: 1fr 1fr; gap: .8rem; }
    .form-group { display: flex; flex-direction: column; gap: .4rem; }
    .form-group label { font-size: .8rem; color: var(--muted); font-weight: 500; }
    .form-group input, .form-group textarea, .form-group select {
      padding: .75rem 1rem; background: var(--bg-card);
      border: 1px solid var(--border); border-radius: 9px; color: var(--text);
      font-family: inherit; font-size: .9rem; outline: none; transition: border-color .2s;
      resize: vertical;
    }
    .form-group input:focus, .form-group textarea:focus { border-color: var(--connexx); }
    .form-group input::placeholder, .form-group textarea::placeholder { color: var(--dim); }
    /* honeypot */
    .hp-field { display: none; }

    /* ─── FOOTER ────────────────────────────────── */
    footer { background: var(--bg-alt); border-top: 1px solid var(--border); padding: 4rem 2rem 2rem; }
    .footer-grid { max-width: 1200px; margin: 0 auto; display: grid; grid-template-columns: 2fr 1fr 1fr 1fr; gap: 3rem; margin-bottom: 3rem; }
    .footer-brand .logo-f {
      font-size: 1.1rem; font-weight: 900; letter-spacing: -1px;
      background: linear-gradient(135deg, #5aafaf, #3d8a8a);
      -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text;
      display: block; margin-bottom: .8rem;
    }
    .footer-brand p { font-size: .83rem; color: var(--dim); line-height: 1.7; max-width: 260px; }
    .footer-social { display: flex; flex-wrap: wrap; gap: .5rem; margin-top: 1.2rem; }
    .footer-social a {
      width: 32px; height: 32px; border-radius: 7px;
      background: var(--bg-card); border: 1px solid var(--border);
      display: flex; align-items: center; justify-content: center;
      color: var(--dim); text-decoration: none; font-size: .75rem; font-weight: 700;
      transition: all .2s;
    }
    .footer-social a:hover { color: var(--connexx); border-color: var(--connexx); }
    .footer-col h4 { font-size: .82rem; font-weight: 700; text-transform: uppercase; letter-spacing: 1px; color: var(--muted); margin-bottom: 1rem; }
    .footer-col ul { list-style: none; display: flex; flex-direction: column; gap: .6rem; }
    .footer-col ul li a { color: var(--dim); text-decoration: none; font-size: .83rem; transition: color .2s; }
    .footer-col ul li a:hover { color: var(--text); }
    .footer-bottom { max-width: 1200px; margin: 0 auto; padding-top: 2rem; border-top: 1px solid var(--border); display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 1rem; }
    .footer-bottom p { font-size: .78rem; color: var(--dim); }
    .footer-bottom a { color: var(--dim); text-decoration: none; }
    .footer-bottom a:hover { color: var(--connexx); }

    /* ─── DIGITAL PRODUCTS / EBOOKS ────────────── */
    .ebook-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(240px, 1fr)); gap: 1.2rem; }
    .ebook-card {
      background: var(--bg-card); border: 1px solid var(--border);
      border-radius: 14px; padding: 1.5rem; transition: all .3s;
      display: flex; flex-direction: column;
    }
    .ebook-card:hover { border-color: rgba(90,175,175,.35); transform: translateY(-3px); }
    .ebook-cover {
      height: 140px; border-radius: 10px; margin-bottom: 1rem;
      display: flex; align-items: center; justify-content: center;
      font-size: 3rem; position: relative; overflow: hidden;
    }
    .ebook-format {
      position: absolute; top: .5rem; right: .5rem;
      font-size: .65rem; font-weight: 700; padding: .2rem .5rem;
      border-radius: 4px; background: rgba(0,0,0,.5); color: #fff;
      text-transform: uppercase; letter-spacing: .5px;
    }
    .ebook-title { font-size: .95rem; font-weight: 800; margin-bottom: .25rem; }
    .ebook-desc { font-size: .8rem; color: var(--muted); line-height: 1.6; flex: 1; margin-bottom: .8rem; }
    .ebook-price-row {
      display: flex; align-items: center; justify-content: space-between;
      padding-top: .8rem; border-top: 1px solid var(--border);
    }
    .ebook-price { font-size: 1.1rem; font-weight: 900; color: var(--connexx); }
    .ebook-price .old { text-decoration: line-through; color: var(--dim); font-size: .8rem; font-weight: 400; margin-right: .3rem; }

    /* ─── AFFILIATE PROGRAM ────────────────────── */
    .affiliate-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 3rem; align-items: center; }
    .aff-steps { display: flex; flex-direction: column; gap: 1rem; }
    .aff-step {
      display: flex; gap: 1rem; align-items: flex-start;
      padding: 1.2rem; background: var(--bg-card);
      border: 1px solid var(--border); border-radius: 12px;
      transition: border-color .2s;
    }
    .aff-step:hover { border-color: rgba(90,175,175,.3); }
    .aff-num {
      width: 36px; height: 36px; border-radius: 50%;
      background: linear-gradient(135deg, var(--connexx), var(--connexx-d));
      color: #fff; display: flex; align-items: center; justify-content: center;
      font-weight: 900; font-size: .9rem; flex-shrink: 0;
    }
    .aff-step-title { font-weight: 700; font-size: .92rem; margin-bottom: .2rem; }
    .aff-step-desc { font-size: .82rem; color: var(--muted); line-height: 1.5; }
    .aff-highlight {
      background: linear-gradient(135deg, rgba(90,175,175,.08), rgba(168,85,247,.05));
      border: 1px solid var(--border-h); border-radius: 16px;
      padding: 2rem; text-align: center;
    }
    .aff-commission { font-size: 3.5rem; font-weight: 900; color: var(--connexx); line-height: 1; }
    .aff-commission-label { font-size: .9rem; color: var(--muted); margin-top: .5rem; }
    .aff-perks { display: grid; grid-template-columns: 1fr 1fr; gap: .6rem; margin-top: 1.5rem; text-align: left; }
    .aff-perk {
      font-size: .8rem; color: var(--muted); padding: .5rem .75rem;
      background: rgba(0,0,0,.2); border-radius: 8px;
      display: flex; align-items: center; gap: .4rem;
    }
    .aff-perk::before { content: '✓'; color: var(--connexx); font-weight: 700; }

    /* ─── DEVELOPMENT SERVICES ─────────────────── */
    .services-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(260px, 1fr)); gap: 1.2rem; }
    .service-card {
      background: var(--bg-card); border: 1px solid var(--border);
      border-radius: 14px; padding: 1.8rem; transition: all .3s;
    }
    .service-card:hover { border-color: rgba(90,175,175,.3); transform: translateY(-3px); }
    .service-icon { font-size: 2rem; margin-bottom: 1rem; }
    .service-title { font-size: 1rem; font-weight: 800; margin-bottom: .5rem; }
    .service-desc { font-size: .85rem; color: var(--muted); line-height: 1.6; margin-bottom: 1rem; }
    .service-from { font-size: .82rem; font-weight: 700; color: var(--connexx); }

    /* ─── DEMO HUB ─────────────────────────────── */
    .demo-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); gap: 1.2rem; }
    .demo-card {
      background: var(--bg-card); border: 1px solid var(--border);
      border-radius: 14px; overflow: hidden; transition: all .3s;
    }
    .demo-card:hover { border-color: rgba(90,175,175,.3); transform: translateY(-2px); }
    .demo-preview {
      height: 160px; display: flex; align-items: center; justify-content: center;
      font-size: 3.5rem; position: relative;
    }
    .demo-live-badge {
      position: absolute; top: .75rem; right: .75rem;
      font-size: .68rem; font-weight: 700; padding: .2rem .6rem;
      border-radius: 20px; background: rgba(0,201,110,.15);
      color: var(--process); border: 1px solid rgba(0,201,110,.25);
      text-transform: uppercase; letter-spacing: .5px;
    }
    .demo-info { padding: 1.2rem; }
    .demo-name { font-weight: 800; font-size: .95rem; margin-bottom: .3rem; }
    .demo-desc { font-size: .8rem; color: var(--muted); margin-bottom: .8rem; }

    /* ─── TRADE TOOLS ──────────────────────────── */
    .trade-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(240px, 1fr)); gap: 1.2rem; }
    .trade-card {
      background: var(--bg-card); border: 1px solid var(--border);
      border-radius: 14px; padding: 1.5rem; transition: all .3s;
    }
    .trade-card:hover { border-color: rgba(201,169,98,.35); transform: translateY(-3px); }
    .trade-icon { font-size: 2rem; margin-bottom: .75rem; }
    .trade-title { font-size: .95rem; font-weight: 800; margin-bottom: .3rem; color: var(--apex); }
    .trade-desc { font-size: .8rem; color: var(--muted); line-height: 1.5; margin-bottom: .8rem; }
    .trade-price { font-size: .88rem; font-weight: 700; color: var(--apex); }

    @media (max-width: 768px) {
      .affiliate-grid { grid-template-columns: 1fr; }
      .aff-perks { grid-template-columns: 1fr; }
    }

    /* ─── FADE-UP ANIMATIONS ────────────────────── */
    .fade-up { opacity: 0; transform: translateY(24px); transition: opacity .6s var(--tr), transform .6s var(--tr); }
    .fade-up.visible { opacity: 1; transform: translateY(0); }
    .delay-1 { transition-delay: .1s; }
    .delay-2 { transition-delay: .2s; }
    .delay-3 { transition-delay: .3s; }
    .delay-4 { transition-delay: .4s; }

    /* ─── RESPONSIVE ────────────────────────────── */
    @media (max-width: 1024px) {
      .featured-grid { grid-template-columns: 1fr; }
      .buy-panel { position: static; }
      .login-grid { grid-template-columns: 1fr; }
      .about-grid { grid-template-columns: 1fr; }
      .contact-grid { grid-template-columns: 1fr; }
      .footer-grid { grid-template-columns: 1fr 1fr; }
      .social-float { display: none; }
    }
    @media (max-width: 768px) {
      .nav-links { display: none; }
      .hamburger { display: block; }
      .tiles-row { flex-direction: column; height: auto; }
      .tile { flex: none; min-width: unset; }
      .tile:hover { flex: none; }
      .tile-cta { opacity: 1; transform: none; }
      .stats-grid { grid-template-columns: repeat(2, 1fr); }
      .products-grid { grid-template-columns: 1fr; }
      .feature-list { grid-template-columns: 1fr; }
      .about-stats { grid-template-columns: 1fr 1fr; }
      .contact-form-row { grid-template-columns: 1fr; }
      .footer-grid { grid-template-columns: 1fr; gap: 2rem; }
      .footer-bottom { flex-direction: column; text-align: center; }
      .email-form { flex-direction: column; }
      .nl-form { flex-direction: column; }
    }
  </style>
</head>
<body>

<!-- FLOATING SOCIAL BAR -->
<div class="social-float">
  <a href="#" title="TikTok">TT</a>
  <a href="#" title="Instagram">IG</a>
  <a href="#" title="YouTube">YT</a>
  <a href="#" title="X / Twitter">X</a>
  <a href="#" title="LinkedIn">in</a>
  <a href="#" title="Telegram">TG</a>
  <a href="#" title="Discord">DS</a>
  <a href="#" title="Reddit">Re</a>
  <a href="#" title="Facebook">Fb</a>
  <a href="#" title="Pinterest">Pi</a>
</div>

<!-- NAV -->
<nav>
  <div class="nav-inner">
    <a href="#" class="logo">MIND VAULT AI</a>
    <ul class="nav-links">
      <li><a href="#products">Products</a></li>
      <li><a href="#ebooks">E-books</a></li>
      <li><a href="#trade-tools">Trade Tools</a></li>
      <li><a href="#demos">Demos</a></li>
      <li><a href="#development">Development</a></li>
      <li><a href="#affiliate">Affiliate</a></li>
    </ul>
    <div class="nav-actions">
      <a href="https://connexx.mindvault-ai.com/login" class="btn btn-ghost">Login</a>
      <a href="https://connexx.mindvault-ai.com" class="btn btn-primary">Get Started →</a>
    </div>
    <button class="hamburger" onclick="this.parentElement.parentElement.querySelector('.nav-links').style.display='flex'">☰</button>
  </div>
</nav>

<!-- HERO -->
<section class="hero">
  <div class="hero-inner">
    <div class="hero-badge fade-up">Mind Vault AI — Digital Products &amp; AI Tools</div>
    <h1 class="fade-up delay-1">
      Buy. Use.<br>
      <span class="grad">Earn more.</span>
    </h1>
    <p class="fade-up delay-2">
      AI tools, e-books, trade tools, templates &amp; custom development.
      Built from 23 years enterprise experience. Ready to use today.
    </p>
    <div class="hero-ctas fade-up delay-3">
      <a href="#ebooks" class="btn btn-primary btn-big">Shop Digital Products &#8595;</a>
      <a href="#demos" class="btn btn-ghost btn-big">Try Free Demos</a>
    </div>
    <div class="trust-badges fade-up delay-4">
      <span class="trust-badge">💳 <span>Gumroad</span></span>
      <span class="trust-badge">🅿️ <span>PayPal</span></span>
      <span class="trust-badge">₿ <span>Crypto</span></span>
      <span class="trust-badge">🔒 <span>GDPR Compliant</span></span>
      <span class="trust-badge">🇪🇺 <span>EU Hosted</span></span>
    </div>
  </div>
</section>

<!-- STATS BAR -->
<div class="stats-bar">
  <div class="stats-grid">
    <div class="fade-up"><div class="stat-num">10+</div><div class="stat-label">Digital Products</div></div>
    <div class="fade-up delay-1"><div class="stat-num">23+</div><div class="stat-label">Years Experience</div></div>
    <div class="fade-up delay-2"><div class="stat-num">30%</div><div class="stat-label">Affiliate Commission</div></div>
    <div class="fade-up delay-3"><div class="stat-num">EU</div><div class="stat-label">Hosted &amp; GDPR</div></div>
  </div>
</div>

<!-- PRODUCTS OVERVIEW -->
<section id="products">
  <div class="section-inner">
    <div class="section-label">Our Products</div>
    <h2 class="fade-up">Everything you need.<br>Built to last.</h2>
    <p class="section-sub fade-up delay-1">Five professional tools — from enterprise AI platforms to trading signals and process optimization.</p>

    <div class="tiles-row fade-up delay-2">
      <div class="tile tile-connexx">
        <div>
          <div class="tile-icon">⚡</div>
          <div class="tile-name">CONNEXX</div>
          <div class="tile-sub">AI Platform · €19–€299/mo</div>
        </div>
        <a href="#connexx" class="tile-cta">Explore Plans →</a>
      </div>
      <div class="tile tile-apex">
        <div>
          <div class="tile-icon">📈</div>
          <div class="tile-name">APEXFLASH</div>
          <div class="tile-sub">Trading Signals · Free</div>
        </div>
        <a href="https://apexflash.pro" class="tile-cta" target="_blank">Visit Site →</a>
      </div>
      <div class="tile tile-darts">
        <div>
          <div class="tile-icon">🎯</div>
          <div class="tile-name">DARTS 501</div>
          <div class="tile-sub">Luxury Edition · €9.99</div>
        </div>
        <a href="#darts" class="tile-cta">Live Demo →</a>
      </div>
      <div class="tile tile-process">
        <div>
          <div class="tile-icon">⚙️</div>
          <div class="tile-name">PROCESS TOOLS</div>
          <div class="tile-sub">Lean · Six Sigma · €29</div>
        </div>
        <a href="#process" class="tile-cta">Learn More →</a>
      </div>
      <div class="tile tile-mobile">
        <div>
          <div class="tile-icon">📱</div>
          <div class="tile-name">ANDROID APP</div>
          <div class="tile-sub">Google Play · Coming Soon</div>
        </div>
        <a href="#mobile" class="tile-cta">Early Access →</a>
      </div>
    </div>
  </div>
</section>

<!-- CONNEXX FEATURED -->
<section id="connexx" style="background: var(--bg-alt); border-top: 1px solid var(--border); border-bottom: 1px solid var(--border);">
  <div class="section-inner">
    <div class="featured-grid">
      <div>
        <div class="featured-label"><span class="dot"></span> Live Platform</div>
        <h2 class="fade-up" style="color: var(--connexx)">Connexx Platform</h2>
        <p style="color: var(--muted); font-size: 1rem; max-width: 500px; margin-bottom: .5rem;">
          Multi-tenant AI platform for logistics, SME &amp; enterprise. Real-time analytics, AI assistant in English &amp; Dutch, full API access.
        </p>

        <ul class="feature-list fade-up delay-1">
          <li>AI Assistant (EN/NL)</li>
          <li>Real-time Analytics</li>
          <li>REST API + Webhooks</li>
          <li>SAP / Exact / AFAS sync</li>
          <li>CSV / PDF Export</li>
          <li>Multi-tenant isolation</li>
          <li class="highlight">Unit Economics Dashboard</li>
          <li class="highlight">LEAN Six Sigma Toolkit</li>
          <li>Marketing Intelligence</li>
          <li>GDPR + IP Whitelisting</li>
          <li>99.9% Uptime SLA</li>
          <li>Android App (Q2 2026)</li>
        </ul>

        <div class="terminal fade-up delay-2" style="margin-top: 1.5rem;">
          <div class="terminal-bar">
            <div class="t-dot" style="background:#ff5f57"></div>
            <div class="t-dot" style="background:#ffbd2e"></div>
            <div class="t-dot" style="background:#28c840"></div>
            <span class="t-title">connexx.mindvault-ai.com — live</span>
          </div>
          <div class="terminal-body">
            <div class="t-dim">$ connexx status</div>
            <div class="t-grn">✓ Platform online · Frankfurt EU</div>
            <div class="t-dim">$ ai ask "Show unit economics summary"</div>
            <div class="t-teal">→ LTV: €847 · CAC: €62 · LTV/CAC: 13.7x</div>
            <div class="t-teal">→ Payback: 1.3 months · Churn: 2.1%</div>
            <div class="t-gold">→ MRR Growth: +18% MoM ↑</div>
            <div class="t-dim">$ lean analyze --process "Order Fulfillment"</div>
            <div class="t-purp">→ 3 waste types identified · Sigma: 3.8</div>
            <div class="t-grn">→ Improvement potential: +22% throughput</div>
          </div>
        </div>
      </div>

      <div class="buy-panel fade-up delay-1">
        <h3>Choose your plan</h3>
        <div class="tier">
          <div><div class="tier-name">Demo</div><div class="tier-sub">100 logs/month</div></div>
          <div class="tier-price">Free</div>
        </div>
        <div class="tier">
          <div><div class="tier-name">Starter</div><div class="tier-sub">1,000 logs/month</div></div>
          <div class="tier-price">€29/mo</div>
        </div>
        <div class="tier popular">
          <div>
            <div style="display:flex;align-items:center;gap:.5rem">
              <div class="tier-name">MKB / SME</div>
              <span class="popular-badge">Popular</span>
            </div>
            <div class="tier-sub">5,000 logs · AI Assistant</div>
          </div>
          <div class="tier-price">€49/mo</div>
        </div>
        <div class="tier">
          <div><div class="tier-name">Professional</div><div class="tier-sub">10,000 logs · Full API · White-label</div></div>
          <div class="tier-price">€99/mo</div>
        </div>
        <div class="tier">
          <div><div class="tier-name">Enterprise</div><div class="tier-sub">100K logs · Dedicated support · SLA</div></div>
          <div class="tier-price">€299/mo</div>
        </div>
        <a href="https://connexx.mindvault-ai.com" class="btn btn-primary buy-cta">Start Free →</a>
        <div class="pay-methods">
          <span class="pay-pill">Gumroad</span>
          <span class="pay-pill">PayPal</span>
          <span class="pay-pill">iDEAL</span>
          <span class="pay-pill">Crypto</span>
        </div>
      </div>
    </div>
  </div>
</section>

<!-- OTHER PRODUCTS -->
<section id="other-products">
  <div class="section-inner">
    <div class="section-label">More Products</div>
    <h2 class="fade-up">Tools for every need.</h2>
    <p class="section-sub fade-up delay-1">Standalone products that deliver real value — no fluff, no subscriptions required unless you want them.</p>

    <div class="products-grid">
      <!-- ApexFlash -->
      <div class="product-card product-apex fade-up">
        <div class="product-card-header">
          <div class="product-icon">📈</div>
          <div>
            <div class="product-title" style="color: var(--apex)">ApexFlash</div>
            <div class="product-price" style="color:var(--apex)">Free — apexflash.pro</div>
          </div>
        </div>
        <p class="product-desc">Crypto trading signals and market intelligence. Live on Telegram. Built for traders who want an edge without the noise.</p>
        <div class="feature-tags">
          <span class="tag">Market Signals</span>
          <span class="tag">Telegram Alerts</span>
          <span class="tag">Live Feed</span>
          <span class="tag">Free to Join</span>
        </div>
        <div class="product-actions">
          <a href="https://apexflash.pro" target="_blank" class="btn btn-sm btn-outline-apex">Visit ApexFlash →</a>
        </div>
      </div>

      <!-- Darts 501 -->
      <div class="product-card product-darts fade-up delay-1" id="darts">
        <div class="product-card-header">
          <div class="product-icon">🎯</div>
          <div>
            <div class="product-title" style="color: var(--darts)">Darts 501 Luxury</div>
            <div class="product-price" style="color:var(--darts)">€9.99 — One-time</div>
          </div>
        </div>
        <p class="product-desc">Premium darts scorekeeping app. Tournament mode, statistics, luxury dark design. Works in your browser — no install, lifetime access after purchase.</p>
        <div class="feature-tags">
          <span class="tag">Tournament Mode</span>
          <span class="tag">3-dart Average</span>
          <span class="tag">Offline Ready</span>
          <span class="tag">Lifetime Access</span>
        </div>
        <div class="product-actions">
          <a href="https://connexx.mindvault-ai.com/demo/darts501" target="_blank" class="btn btn-sm btn-outline-darts">Live Demo →</a>
          <a href="#contact" class="btn btn-sm btn-ghost">Buy Now</a>
        </div>
      </div>

      <!-- Process Tools -->
      <div class="product-card product-process fade-up delay-2" id="process">
        <div class="product-card-header">
          <div class="product-icon">⚙️</div>
          <div>
            <div class="product-title" style="color: var(--process)">Process Tools</div>
            <div class="product-price" style="color:var(--process)">€29 — One-time / Incl. in Pro+</div>
          </div>
        </div>
        <p class="product-desc">Lean Six Sigma toolkit for process optimization and quality assurance. DMAIC management, control charts, sigma calculations, waste identification.</p>
        <div class="feature-tags">
          <span class="tag">DMAIC</span>
          <span class="tag">Control Charts</span>
          <span class="tag">Sigma Level</span>
          <span class="tag">8 Lean Wastes</span>
          <span class="tag">KPI Dashboard</span>
        </div>
        <div class="product-actions">
          <a href="#contact" class="btn btn-sm btn-outline-green">Get Info →</a>
        </div>
      </div>

      <!-- Business Intel -->
      <div class="product-card fade-up delay-3">
        <div class="product-card-header">
          <div class="product-icon">📊</div>
          <div>
            <div class="product-title" style="color: #a855f7">Business Intelligence</div>
            <div class="product-price" style="color:#a855f7">€29 — One-time / Incl. in Pro+</div>
          </div>
        </div>
        <p class="product-desc">Unit economics dashboard with LTV, CAC, payback period, churn prediction and MRR tracking. Know what you earn and why.</p>
        <div class="feature-tags">
          <span class="tag">Unit Economics</span>
          <span class="tag">LTV / CAC</span>
          <span class="tag">Cohort Analysis</span>
          <span class="tag">Churn Prediction</span>
          <span class="tag">MRR / ARR</span>
        </div>
        <div class="product-actions">
          <a href="#contact" class="btn btn-sm" style="border:1px solid rgba(168,85,247,.3);color:#a855f7;background:transparent">Get Info →</a>
        </div>
      </div>

      <!-- Android App -->
      <div class="product-card product-mobile fade-up delay-1" id="mobile" style="grid-column: span 2;">
        <div class="product-card-header">
          <div class="product-icon">📱</div>
          <div>
            <div class="product-title" style="color: var(--mobile)">MVAI Connexx Android App</div>
            <div class="product-price" style="color:var(--mobile)">Free with all paid Connexx plans · Q2 2026</div>
          </div>
        </div>
        <p class="product-desc">Full Connexx functionality as a native Android app. Push notifications, offline detection, pull-to-refresh. Tested on Samsung S23+. Package: com.mindvault.mvaiconnexz</p>
        <div class="feature-tags">
          <span class="tag">Native Android</span>
          <span class="tag">Push Notifications</span>
          <span class="tag">Offline Mode</span>
          <span class="tag">Google Play</span>
          <span class="tag">Free with Connexx</span>
        </div>
        <div class="product-actions" style="margin-top:.5rem">
          <a href="#newsletter" class="btn btn-sm btn-outline-orange">Register for Early Access →</a>
        </div>
      </div>
    </div>
  </div>
</section>

<!-- ══════════════ E-BOOKS & DIGITAL PRODUCTS ══════════════ -->
<section id="ebooks" style="background: var(--bg-alt); border-top: 1px solid var(--border); border-bottom: 1px solid var(--border);">
  <div class="section-inner">
    <div class="section-label">Digital Products</div>
    <h2 class="fade-up">E-books &amp; Templates.<br>Learn. Apply. Earn.</h2>
    <p class="section-sub fade-up delay-1">Practical guides built from real enterprise experience. No fluff — actionable knowledge you can use today.</p>

    <div class="ebook-grid">
      <div class="ebook-card fade-up">
        <div class="ebook-cover" style="background:linear-gradient(135deg,rgba(90,175,175,.15),rgba(61,138,138,.08))">
          <span class="ebook-format">PDF</span>
          &#128218;
        </div>
        <div class="ebook-title">AI Automation for Business</div>
        <div class="ebook-desc">Step-by-step guide to implementing AI in your business. From ChatGPT prompts to full workflow automation. 80+ pages of actionable strategies.</div>
        <div class="ebook-price-row">
          <div class="ebook-price"><span class="old">&euro;29</span> &euro;19</div>
          <a href="https://mindvault-ai.gumroad.com/l/ai-automation-guide" target="_blank" rel="noopener" class="btn btn-sm btn-primary">Get E-book</a>
        </div>
      </div>

      <div class="ebook-card fade-up delay-1">
        <div class="ebook-cover" style="background:linear-gradient(135deg,rgba(0,201,110,.15),rgba(0,160,80,.08))">
          <span class="ebook-format">PDF</span>
          &#9881;&#65039;
        </div>
        <div class="ebook-title">Lean Six Sigma Handbook</div>
        <div class="ebook-desc">From DMAIC to control charts — a practical handbook for process optimization. Includes templates, checklists and real-world case studies.</div>
        <div class="ebook-price-row">
          <div class="ebook-price">&euro;24</div>
          <a href="https://mindvault-ai.gumroad.com/l/lean-six-sigma-handbook" target="_blank" rel="noopener" class="btn btn-sm btn-outline-green">Get E-book</a>
        </div>
      </div>

      <div class="ebook-card fade-up delay-2">
        <div class="ebook-cover" style="background:linear-gradient(135deg,rgba(201,169,98,.15),rgba(160,130,70,.08))">
          <span class="ebook-format">PDF</span>
          &#128200;
        </div>
        <div class="ebook-title">Trading Psychology &amp; Risk</div>
        <div class="ebook-desc">Master your mind, master the market. Risk management frameworks, position sizing, and the psychology behind consistent profits.</div>
        <div class="ebook-price-row">
          <div class="ebook-price">&euro;14</div>
          <a href="https://mindvault-ai.gumroad.com/l/trading-psychology" target="_blank" rel="noopener" class="btn btn-sm btn-outline-apex">Get E-book</a>
        </div>
      </div>

      <div class="ebook-card fade-up delay-3">
        <div class="ebook-cover" style="background:linear-gradient(135deg,rgba(168,85,247,.15),rgba(120,50,200,.08))">
          <span class="ebook-format">BUNDLE</span>
          &#128230;
        </div>
        <div class="ebook-title">Business Templates Bundle</div>
        <div class="ebook-desc">50+ ready-to-use templates: unit economics calculators, KPI dashboards, project trackers, invoice templates. Notion + Excel + Google Sheets.</div>
        <div class="ebook-price-row">
          <div class="ebook-price"><span class="old">&euro;49</span> &euro;29</div>
          <a href="https://mindvault-ai.gumroad.com/l/business-templates" target="_blank" rel="noopener" class="btn btn-sm" style="border:1px solid rgba(168,85,247,.3);color:#a855f7;background:transparent">Get Bundle</a>
        </div>
      </div>
    </div>
  </div>
</section>

<!-- ══════════════ TRADE TOOLS ══════════════ -->
<section id="trade-tools">
  <div class="section-inner">
    <div class="section-label">Trade Tools</div>
    <h2 class="fade-up">Smarter trading.<br>Better decisions.</h2>
    <p class="section-sub fade-up delay-1">Professional-grade tools for traders who take their craft seriously. Built by traders, for traders.</p>

    <div class="trade-grid">
      <div class="trade-card fade-up">
        <div class="trade-icon">&#128202;</div>
        <div class="trade-title">Portfolio Tracker Pro</div>
        <div class="trade-desc">Track all your positions across exchanges. P&amp;L calculations, allocation view, performance history. Excel + Google Sheets.</div>
        <div class="trade-price">&euro;19 — one-time</div>
        <a href="https://mindvault-ai.gumroad.com/l/portfolio-tracker" target="_blank" rel="noopener" class="btn btn-sm btn-outline-apex" style="margin-top:.8rem">Get Tool</a>
      </div>

      <div class="trade-card fade-up delay-1">
        <div class="trade-icon">&#9878;&#65039;</div>
        <div class="trade-title">Risk Management Kit</div>
        <div class="trade-desc">Position sizing calculator, risk/reward ratio tool, stop-loss optimizer. Never risk more than you should.</div>
        <div class="trade-price">&euro;14 — one-time</div>
        <a href="https://mindvault-ai.gumroad.com/l/risk-management-kit" target="_blank" rel="noopener" class="btn btn-sm btn-outline-apex" style="margin-top:.8rem">Get Tool</a>
      </div>

      <div class="trade-card fade-up delay-2">
        <div class="trade-icon">&#128209;</div>
        <div class="trade-title">Trade Journal Template</div>
        <div class="trade-desc">Professional trade journal with auto-calculated stats. Track entries, exits, emotions, and patterns. Notion + Spreadsheet versions.</div>
        <div class="trade-price">&euro;9 — one-time</div>
        <a href="https://mindvault-ai.gumroad.com/l/trade-journal" target="_blank" rel="noopener" class="btn btn-sm btn-outline-apex" style="margin-top:.8rem">Get Tool</a>
      </div>

      <div class="trade-card fade-up delay-3">
        <div class="trade-icon">&#128640;</div>
        <div class="trade-title">Market Analysis Templates</div>
        <div class="trade-desc">Technical &amp; fundamental analysis frameworks. Pre-built charts, indicator checklists, and market screening templates.</div>
        <div class="trade-price">&euro;19 — one-time</div>
        <a href="https://mindvault-ai.gumroad.com/l/market-analysis" target="_blank" rel="noopener" class="btn btn-sm btn-outline-apex" style="margin-top:.8rem">Get Tool</a>
      </div>
    </div>
  </div>
</section>

<!-- ══════════════ DEMO HUB ══════════════ -->
<section id="demos" style="background: var(--bg-alt); border-top: 1px solid var(--border); border-bottom: 1px solid var(--border);">
  <div class="section-inner">
    <div class="section-label">Try Before You Buy</div>
    <h2 class="fade-up">Live demos.<br>No signup required.</h2>
    <p class="section-sub fade-up delay-1">Experience our products first-hand. Click, explore, decide.</p>

    <div class="demo-grid">
      <a href="https://connexx.mindvault-ai.com" target="_blank" rel="noopener" class="demo-card fade-up" style="text-decoration:none;color:inherit">
        <div class="demo-preview" style="background:linear-gradient(135deg,rgba(90,175,175,.1),rgba(61,138,138,.05))">
          <div class="demo-live-badge">Live</div>
          &#9889;
        </div>
        <div class="demo-info">
          <div class="demo-name">Connexx Platform</div>
          <div class="demo-desc">Full AI platform demo — 100 free logs, analytics dashboard, AI assistant.</div>
          <span class="btn btn-sm btn-primary" style="width:100%;justify-content:center">Try Free Demo &#8594;</span>
        </div>
      </a>

      <a href="https://connexx.mindvault-ai.com/demo/darts501" target="_blank" rel="noopener" class="demo-card fade-up delay-1" style="text-decoration:none;color:inherit">
        <div class="demo-preview" style="background:linear-gradient(135deg,rgba(168,85,247,.1),rgba(120,50,200,.05))">
          <div class="demo-live-badge">Live</div>
          &#127919;
        </div>
        <div class="demo-info">
          <div class="demo-name">Darts 501 Luxury</div>
          <div class="demo-desc">Full game experience — multiplayer, statistics, luxury design. Play now!</div>
          <span class="btn btn-sm btn-outline-darts" style="width:100%;justify-content:center">Play Demo &#8594;</span>
        </div>
      </a>

      <div class="demo-card fade-up delay-2">
        <div class="demo-preview" style="background:linear-gradient(135deg,rgba(0,201,110,.1),rgba(0,160,80,.05))">
          &#128736;&#65039;
        </div>
        <div class="demo-info">
          <div class="demo-name">Process Tools Preview</div>
          <div class="demo-desc">DMAIC workflow, control charts, sigma calculations. Available via Connexx Professional.</div>
          <a href="https://connexx.mindvault-ai.com" target="_blank" rel="noopener" class="btn btn-sm btn-outline-green" style="width:100%;justify-content:center">Access via Connexx &#8594;</a>
        </div>
      </div>
    </div>
  </div>
</section>

<!-- ══════════════ MVAI DEVELOPMENT SERVICES ══════════════ -->
<section id="development">
  <div class="section-inner">
    <div class="section-label">MVAI Development</div>
    <h2 class="fade-up">Custom AI solutions.<br>Built for your business.</h2>
    <p class="section-sub fade-up delay-1">23 years enterprise experience + AI expertise = solutions that actually work. From concept to production.</p>

    <div class="services-grid">
      <div class="service-card fade-up">
        <div class="service-icon">&#129302;</div>
        <div class="service-title">Custom AI Integration</div>
        <div class="service-desc">AI assistants, chatbots, data analysis pipelines — tailored to your workflow. Multi-provider (OpenAI, Anthropic, local models).</div>
        <div class="service-from">From &euro;2,500</div>
      </div>

      <div class="service-card fade-up delay-1">
        <div class="service-icon">&#128187;</div>
        <div class="service-title">SaaS Development</div>
        <div class="service-desc">Full-stack SaaS platforms with multi-tenant architecture, payment integration, API design. Python/Flask or Node.js.</div>
        <div class="service-from">From &euro;5,000</div>
      </div>

      <div class="service-card fade-up delay-2">
        <div class="service-icon">&#9881;&#65039;</div>
        <div class="service-title">Process Automation</div>
        <div class="service-desc">Eliminate manual work. ERP integrations (SAP, Exact, AFAS), workflow automation, Lean Six Sigma optimization.</div>
        <div class="service-from">From &euro;1,500</div>
      </div>

      <div class="service-card fade-up delay-3">
        <div class="service-icon">&#127912;</div>
        <div class="service-title">White-Label Solutions</div>
        <div class="service-desc">Rebrand our tools as your own. Connexx platform, analytics dashboards, AI assistants — your brand, our tech.</div>
        <div class="service-from">From &euro;3,000</div>
      </div>
    </div>

    <div style="text-align:center;margin-top:2.5rem" class="fade-up delay-3">
      <a href="#contact" class="btn btn-primary btn-big">Discuss Your Project &#8594;</a>
      <p style="color:var(--dim);font-size:.82rem;margin-top:.8rem">Free 30-minute consultation &middot; NDA on request &middot; EU based</p>
    </div>
  </div>
</section>

<!-- ══════════════ AFFILIATE PROGRAM ══════════════ -->
<section id="affiliate" style="background: var(--bg-alt); border-top: 1px solid var(--border); border-bottom: 1px solid var(--border);">
  <div class="section-inner">
    <div class="section-label">Partner Program</div>
    <h2 class="fade-up">Earn with MVAI.<br>30% recurring commission.</h2>
    <p class="section-sub fade-up delay-1">Promote our tools, earn on every sale. Recurring commissions on subscriptions. Real products, real payouts.</p>

    <div class="affiliate-grid">
      <div class="aff-steps fade-up delay-1">
        <div class="aff-step">
          <div class="aff-num">1</div>
          <div>
            <div class="aff-step-title">Sign up as partner</div>
            <div class="aff-step-desc">Quick application — get your unique referral link and marketing materials within 24 hours.</div>
          </div>
        </div>
        <div class="aff-step">
          <div class="aff-num">2</div>
          <div>
            <div class="aff-step-title">Share &amp; promote</div>
            <div class="aff-step-desc">Share on your blog, social media, YouTube, newsletter. We provide banners, copy, and landing pages.</div>
          </div>
        </div>
        <div class="aff-step">
          <div class="aff-num">3</div>
          <div>
            <div class="aff-step-title">Earn recurring revenue</div>
            <div class="aff-step-desc">30% commission on every sale. Recurring for subscription products. Paid monthly via PayPal or crypto.</div>
          </div>
        </div>
      </div>

      <div class="aff-highlight fade-up delay-2">
        <div class="aff-commission">30%</div>
        <div class="aff-commission-label">Recurring Commission</div>
        <div style="font-size:.82rem;color:var(--dim);margin-top:.3rem">on all Connexx subscriptions &amp; product sales</div>
        <div class="aff-perks">
          <div class="aff-perk">Real-time dashboard</div>
          <div class="aff-perk">90-day cookie</div>
          <div class="aff-perk">Monthly payouts</div>
          <div class="aff-perk">Marketing materials</div>
          <div class="aff-perk">Dedicated support</div>
          <div class="aff-perk">No minimum payout</div>
        </div>
        <a href="mailto:info@mindvault-ai.com?subject=Affiliate Program Application" class="btn btn-primary" style="margin-top:1.5rem;width:100%;justify-content:center">Apply as Partner &#8594;</a>
      </div>
    </div>
  </div>
</section>

<!-- LOGIN SECTION -->
<section class="login-section">
  <div class="section-inner">
    <div class="login-grid">
      <div>
        <div class="section-label">Access</div>
        <h2 class="fade-up">Sign in to your<br>MVAI account.</h2>
        <p style="color:var(--muted); margin-top:.5rem; margin-bottom:2rem;">
          One login for all MVAI products. Manage your subscriptions, access tools, and track your usage.
        </p>
        <div class="login-providers fade-up delay-1">
          <a href="https://connexx.mindvault-ai.com/login?provider=google" class="login-btn">
            <div class="login-btn-icon" style="background:#fff">🇬</div>
            Continue with Google
          </a>
          <a href="https://connexx.mindvault-ai.com/login?provider=apple" class="login-btn">
            <div class="login-btn-icon" style="background:#000; color:#fff">🍎</div>
            Continue with Apple
          </a>
          <a href="https://connexx.mindvault-ai.com/login?provider=microsoft" class="login-btn">
            <div class="login-btn-icon" style="background:#0078d4; color:#fff">⊞</div>
            Continue with Microsoft
          </a>
          <div class="login-or">or</div>
          <form class="email-form" onsubmit="return false">
            <input type="email" placeholder="your@email.com" autocomplete="email">
            <button type="submit" class="btn btn-primary">Sign in →</button>
          </form>
        </div>
      </div>
      <div class="fade-up delay-2" style="text-align:center;">
        <div style="background:var(--bg-card); border:1px solid var(--border); border-radius:20px; padding:3rem 2rem;">
          <div style="font-size:3rem; margin-bottom:1rem">🔐</div>
          <h3 style="font-size:1.2rem; font-weight:800; margin-bottom:.75rem">Secure &amp; Private</h3>
          <p style="color:var(--muted); font-size:.88rem; line-height:1.7;">
            Multi-tenant isolation. Your data is yours only.
            EU-hosted (Frankfurt), GDPR compliant.
            No data sharing, ever.
          </p>
          <div style="margin-top:1.5rem; display:flex; gap:.5rem; justify-content:center; flex-wrap:wrap;">
            <span class="pay-pill">GDPR</span>
            <span class="pay-pill">EU Hosted</span>
            <span class="pay-pill">Encrypted</span>
            <span class="pay-pill">No 3rd party</span>
          </div>
        </div>
      </div>
    </div>
  </div>
</section>

<!-- NEWSLETTER -->
<section id="newsletter">
  <div class="section-inner">
    <div class="newsletter-wrap fade-up">
      <div style="font-size:2rem; margin-bottom:1rem">📬</div>
      <h3>Stay ahead of the market.</h3>
      <p>New products, tools, demos, and insights — straight to your inbox. No spam, unsubscribe anytime.</p>
      <form class="nl-form" id="nlForm" onsubmit="handleNewsletter(event)">
        <!-- honeypot — bots fill this, humans don't see it -->
        <input class="hp-field" type="text" name="website" tabindex="-1" autocomplete="off">
        <input type="email" id="nlEmail" placeholder="your@email.com" required>
        <button type="submit" class="btn btn-primary">Subscribe →</button>
      </form>
      <p class="nl-gdpr">By subscribing you agree to our <a href="#" style="color:var(--connexx)">Privacy Policy</a>. EU GDPR compliant. No spam.</p>
      <div id="nlMsg" style="margin-top:.8rem; font-size:.85rem; color:var(--connexx); display:none"></div>
    </div>
  </div>
</section>

<!-- CLIENTS -->
<section style="background: var(--bg-alt); border-top: 1px solid var(--border); border-bottom: 1px solid var(--border); padding: 3rem 2rem;">
  <div class="section-inner" style="text-align:center">
    <div class="section-label" style="justify-content:center; margin-bottom:1.5rem">Track Record</div>
    <h2 class="fade-up" style="font-size:1.4rem; margin-bottom:1rem">23 years serving industry leaders</h2>
    <div class="clients-row fade-up delay-1">
      <div class="client-badge">Goodyear</div>
      <div class="client-badge">Michelin</div>
      <div class="client-badge">Nokian</div>
      <div class="client-badge">Yantai</div>
      <div class="client-badge">InforLN</div>
      <div class="client-badge">BAAN ERP</div>
    </div>
    <p style="color:var(--dim);font-size:.82rem;margin-top:1.5rem">Former supervisor / key-user ERP · Supply Chain · Lean Auditor</p>
  </div>
</section>

<!-- ABOUT -->
<section id="about">
  <div class="section-inner">
    <div class="about-grid">
      <div class="about-text">
        <div class="section-label">About</div>
        <h2 class="fade-up">Enterprise expertise,<br>AI acceleration.</h2>
        <p class="fade-up delay-1">
          Mind Vault AI was built from 23 years of hands-on enterprise experience — implementing and auditing ERP systems (BAAN, InforLN) for Tier 1 automotive manufacturers across Europe and Asia.
        </p>
        <p class="fade-up delay-2">
          That foundation means our tools are built the way enterprise software should be: structured, reliable, and actually useful. No hype, no bloat — just tools that solve real problems.
        </p>
        <p class="fade-up delay-3">
          From on-site training at Yantai (China) to supply chain optimization for Goodyear and Michelin — now channeled into AI-driven platforms available to everyone.
        </p>

        <div class="about-stats fade-up delay-2">
          <div class="about-stat"><div class="about-stat-num">23+</div><div class="about-stat-label">Years ERP / SCM</div></div>
          <div class="about-stat"><div class="about-stat-num">Tier 1</div><div class="about-stat-label">Automotive verified</div></div>
          <div class="about-stat"><div class="about-stat-num">EU</div><div class="about-stat-label">Frankfurt hosted</div></div>
          <div class="about-stat"><div class="about-stat-num">5</div><div class="about-stat-label">Active products</div></div>
        </div>
      </div>
      <div class="fade-up delay-1">
        <div style="background:var(--bg-card);border:1px solid var(--border);border-radius:16px;padding:2rem;margin-bottom:1.5rem">
          <h4 style="font-size:.9rem;font-weight:700;margin-bottom:1rem;color:var(--muted);text-transform:uppercase;letter-spacing:1px">Expertise</h4>
          <div class="expertise-tags">
            <span class="exp-tag">InforLN</span>
            <span class="exp-tag">BAAN ERP</span>
            <span class="exp-tag">Supply Chain</span>
            <span class="exp-tag">Lean Six Sigma</span>
            <span class="exp-tag">DMAIC</span>
            <span class="exp-tag">Unit Economics</span>
            <span class="exp-tag">Multi-tenant SaaS</span>
            <span class="exp-tag">AI Automation</span>
            <span class="exp-tag">Process Audit</span>
            <span class="exp-tag">Training</span>
            <span class="exp-tag">Flask / Python</span>
            <span class="exp-tag">Android Dev</span>
          </div>
        </div>
        <div style="background:var(--bg-card);border:1px solid rgba(90,175,175,.25);border-radius:16px;padding:2rem">
          <h4 style="font-size:.9rem;font-weight:700;margin-bottom:.75rem;color:var(--connexx)">MVAI Philosophy</h4>
          <p style="font-size:.88rem;color:var(--muted);line-height:1.8;font-style:italic">
            "You can only improve by accepting feedback from the market and your customers, embracing issues, and fixing them fast. That's how you build credibility — and a business that lasts."
          </p>
        </div>
      </div>
    </div>
  </div>
</section>

<!-- CONTACT -->
<section id="contact" style="background:var(--bg-alt);border-top:1px solid var(--border)">
  <div class="section-inner">
    <div class="section-label">Contact</div>
    <h2 class="fade-up">Let's build something.</h2>
    <p class="section-sub fade-up delay-1">Questions, demos, custom integrations or enterprise pricing — reach out directly.</p>
    <div class="contact-grid">
      <div>
        <div class="contact-info fade-up delay-1">
          <a href="mailto:info@mindvault-ai.com" class="contact-item">
            <div class="contact-item-icon">✉️</div>
            <div><div class="contact-item-label">Email</div><div class="contact-item-val">info@mindvault-ai.com</div></div>
          </a>
          <a href="https://www.linkedin.com/company/mindvault-ai" target="_blank" class="contact-item">
            <div class="contact-item-icon">in</div>
            <div><div class="contact-item-label">LinkedIn</div><div class="contact-item-val">linkedin.com/company/mindvault-ai</div></div>
          </a>
          <a href="https://apexflash.pro" target="_blank" class="contact-item">
            <div class="contact-item-icon">📈</div>
            <div><div class="contact-item-label">Trading Signals</div><div class="contact-item-val">apexflash.pro</div></div>
          </a>
          <a href="https://connexx.mindvault-ai.com" target="_blank" class="contact-item">
            <div class="contact-item-icon">⚡</div>
            <div><div class="contact-item-label">Platform</div><div class="contact-item-val">connexx.mindvault-ai.com</div></div>
          </a>
        </div>
      </div>
      <div class="fade-up delay-2">
        <form class="contact-form" id="contactForm" onsubmit="handleContact(event)">
          <!-- honeypot -->
          <input class="hp-field" type="text" name="url" tabindex="-1" autocomplete="off">
          <div class="contact-form-row">
            <div class="form-group"><label>Name</label><input type="text" placeholder="Your name" required></div>
            <div class="form-group"><label>Email</label><input type="email" placeholder="your@email.com" required></div>
          </div>
          <div class="form-group">
            <label>Subject</label>
            <select>
              <option>Connexx Platform</option>
              <option>Enterprise / Custom</option>
              <option>Trading Tools</option>
              <option>Process Consulting</option>
              <option>Training &amp; Auditing</option>
              <option>Partnership</option>
              <option>Other</option>
            </select>
          </div>
          <div class="form-group"><label>Message</label><textarea rows="4" placeholder="Tell us what you need..."></textarea></div>
          <button type="submit" class="btn btn-primary" style="width:100%;justify-content:center;padding:.9rem">Send Message →</button>
          <div id="contactMsg" style="font-size:.82rem;color:var(--connexx);margin-top:.5rem;display:none"></div>
        </form>
      </div>
    </div>
  </div>
</section>

<!-- FOOTER -->
<footer>
  <div class="footer-grid">
    <div class="footer-brand">
      <span class="logo-f">MIND VAULT AI</span>
      <p>Enterprise AI tools built from real-world experience. For traders, businesses &amp; teams worldwide.</p>
      <p style="margin-top:.5rem; font-size:.78rem; color: var(--dim)">info@mindvault-ai.com · EU Hosted · GDPR Compliant</p>
      <div class="footer-social">
        <a href="#" title="TikTok">TT</a>
        <a href="#" title="Instagram">IG</a>
        <a href="#" title="YouTube">YT</a>
        <a href="#" title="X">X</a>
        <a href="https://www.linkedin.com/company/mindvault-ai" title="LinkedIn">in</a>
        <a href="#" title="Telegram">TG</a>
        <a href="#" title="Discord">DS</a>
        <a href="#" title="Reddit">Re</a>
        <a href="#" title="Facebook">Fb</a>
        <a href="#" title="Pinterest">Pi</a>
      </div>
    </div>
    <div class="footer-col">
      <h4>Products</h4>
      <ul>
        <li><a href="#connexx">Connexx Platform</a></li>
        <li><a href="#ebooks">E-books &amp; Templates</a></li>
        <li><a href="#trade-tools">Trade Tools</a></li>
        <li><a href="#darts">Darts 501 Luxury</a></li>
        <li><a href="#process">Process Tools</a></li>
      </ul>
    </div>
    <div class="footer-col">
      <h4>Platform</h4>
      <ul>
        <li><a href="https://connexx.mindvault-ai.com">Login / Demo</a></li>
        <li><a href="#demos">Live Demos</a></li>
        <li><a href="#development">MVAI Development</a></li>
        <li><a href="#affiliate">Affiliate Program</a></li>
        <li><a href="#newsletter">Newsletter</a></li>
      </ul>
    </div>
    <div class="footer-col">
      <h4>Pay &amp; Buy</h4>
      <ul>
        <li><a href="https://mindvault-ai.gumroad.com" target="_blank" rel="noopener">Gumroad Shop</a></li>
        <li><a href="https://www.paypal.com/paypalme/mindvaultai" target="_blank" rel="noopener">PayPal</a></li>
        <li><a href="mailto:info@mindvault-ai.com?subject=Crypto payment">Crypto</a></li>
        <li><a href="#contact">Enterprise Invoice</a></li>
      </ul>
    </div>
  </div>
  <div class="footer-bottom">
    <p>© 2026 Mind Vault AI. All rights reserved.</p>
    <p>Built with focus on what matters: <strong style="color:var(--connexx)">your results.</strong></p>
    <p><a href="#">Privacy</a> · <a href="#">Terms</a> · <a href="#">GDPR</a></p>
  </div>
</footer>

<script>
  // Scroll animations
  const obs = new IntersectionObserver(entries => {
    entries.forEach(e => { if (e.isIntersecting) { e.target.classList.add('visible'); obs.unobserve(e.target); } });
  }, { threshold: 0.08 });
  document.querySelectorAll('.fade-up').forEach(el => obs.observe(el));

  // Newsletter submit
  function handleNewsletter(e) {
    e.preventDefault();
    const hp = e.target.querySelector('[name="website"]');
    if (hp && hp.value) return; // honeypot triggered
    const email = document.getElementById('nlEmail').value;
    if (!email) return;
    // POST to Connexx backend (Fase 2)
    fetch('https://connexx.mindvault-ai.com/api/newsletter/subscribe', {
      method: 'POST', headers: {'Content-Type':'application/json'},
      body: JSON.stringify({ email, source: 'mindvault-ai.com', language: 'en' })
    }).then(r => {
      const msg = document.getElementById('nlMsg');
      msg.style.display = 'block';
      if (r.ok) { msg.textContent = '✓ Subscribed! Welcome to the MVAI family.'; document.getElementById('nlEmail').value = ''; }
      else { msg.textContent = '⚠ Something went wrong. Please email info@mindvault-ai.com'; msg.style.color = '#f97316'; }
    }).catch(() => {
      const msg = document.getElementById('nlMsg');
      msg.style.display = 'block';
      msg.textContent = '✓ Got it! We\'ll be in touch at ' + email;
    });
  }

  // Contact submit
  function handleContact(e) {
    e.preventDefault();
    const hp = e.target.querySelector('[name="url"]');
    if (hp && hp.value) return;
    const msg = document.getElementById('contactMsg');
    msg.style.display = 'block';
    msg.textContent = '✓ Message sent! We\'ll respond within 24 hours.';
    e.target.reset();
  }

  // Smooth scroll for anchor links
  document.querySelectorAll('a[href^="#"]').forEach(a => {
    a.addEventListener('click', e => {
      const target = document.querySelector(a.getAttribute('href'));
      if (target) { e.preventDefault(); target.scrollIntoView({ behavior: 'smooth', block: 'start' }); }
    });
  });
</script>
</body>
</html>
