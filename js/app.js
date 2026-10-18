/* Browser-local presentation interactions. No inference or backend health requests. */
'use strict';
(() => {
  const isObject = x => x !== null && typeof x === 'object' && !Array.isArray(x);
  function publicWebUrl(value, allowHttp = false) {
    if (typeof value !== 'string' || !value.trim()) return null;
    try {
      const u = new URL(value);
      const host = u.hostname.toLowerCase().replace(/\.$/, '');
      if (!(u.protocol === 'https:' || (allowHttp === true && u.protocol === 'http:')) || u.username || u.password || u.hash) return null;
      if (!host.includes('.') || host.includes(':') || /(?:^|\.)(localhost|local|internal|test|invalid|example)$/.test(host)) return null;
      if (/^(?:10|127|0)\./.test(host) || /^169\.254\./.test(host) || /^192\.168\./.test(host) || /^172\.(?:1[6-9]|2\d|3[01])\./.test(host)) return null;
      if (/^100\.(?:6[4-9]|[7-9]\d|1[01]\d|12[0-7])\./.test(host) || /^(?:198\.(?:18|19)|192\.0\.0)\./.test(host)) return null;
      if (/^\d+\.\d+\.\d+\.\d+$/.test(host)) {
        const n=Number(host.split('.')[0]);
        if (n>=224 || host.startsWith('192.0.2.') || host.startsWith('198.51.100.') || host.startsWith('203.0.113.')) return null;
      }
      // Configuration links are public landing pages or media; query strings are intentionally excluded.
      if (u.search) return null;
      if (/(?:token|api[_-]?key|password|secret|signature)=/i.test(decodeURIComponent(u.pathname))) return null;
      return u.href;
    } catch (_) { return null; }
  }
  const publicHttps = value => publicWebUrl(value, false);
  const publicDemoUrl = (value, allowHttp = false) => publicWebUrl(value, allowHttp === true);
  function assetUrl(value, base) {
    if (typeof value !== 'string' || !value.trim()) return null;
    if (value.startsWith('https://')) return publicHttps(value);
    if (!/^\.\/(?:assets|docs)\//.test(value) || value.includes('\\') || /[?#]/.test(value)) return null;
    try {
      const decoded = decodeURIComponent(value);
      if (decoded.slice(2).split('/').some(x => x === '..' || x === '.')) return null;
      if (decoded.includes('\\') || decoded.includes('//')) return null;
      const u = new URL(value, base), root = new URL('./', base);
      return u.origin === root.origin && u.pathname.startsWith(root.pathname) ? u.href : null;
    } catch (_) { return null; }
  }
  function confirmedDate(value) {
    return typeof value === 'string' && /^\d{4}-\d\d-\d\dT\d\d:\d\d(?::\d\d(?:\.\d+)?)?(?:Z|[+-]\d\d:\d\d)$/.test(value) && Number.isFinite(Date.parse(value));
  }
  function configValid(c) {
    return isObject(c) && c.schemaVersion === 1 && isObject(c.demo) && typeof c.demo.enabled === 'boolean' &&
      (c.demo.url === null || typeof c.demo.url === 'string') &&
      ['lan','eci','unconfirmed'].includes(c.demo.deploymentMode) && typeof c.demo.statusText === 'string' &&
      (c.demo.lastVerifiedAt === null || confirmedDate(c.demo.lastVerifiedAt)) &&
      (c.demo.allowHttp === undefined || typeof c.demo.allowHttp === 'boolean') &&
      isObject(c.links) && ['githubRepositoryUrl','projectDocsUrl'].every(k=>c.links[k]===null || typeof c.links[k]==='string');
  }
  // Pure validation helpers can also be checked with Node, without a browser or npm packages.
  if (typeof module !== 'undefined' && module.exports) module.exports = { publicHttps, publicDemoUrl, assetUrl, confirmedDate, configValid };
  if (typeof document === 'undefined') return;
  const $ = s => document.querySelector(s);
  const all = s => [...document.querySelectorAll(s)];
  const menu = $('.menu-toggle'), nav = $('#main-nav');
  menu.addEventListener('click', () => {
    const open=menu.getAttribute('aria-expanded')!=='true';
    menu.setAttribute('aria-expanded',String(open));nav.classList.toggle('open',open);
  });
  all('#main-nav a').forEach(a=>a.addEventListener('click',()=>{
    nav.classList.remove('open');menu.setAttribute('aria-expanded','false');
  }));
  function choose(buttons, panels, selected, attribute) {
    buttons.forEach(b=>{const active=b===selected;b.classList.toggle('selected',active);b.setAttribute('aria-pressed',String(active));});
    const id=selected.getAttribute(attribute);
    panels.forEach(p=>p.classList.toggle('selected',p.id===id));
  }
  const archButtons=all('.arch-button'), archPanels=all('.arch-panel');
  archButtons.forEach(b=>b.addEventListener('click',()=>choose(archButtons,archPanels,b,'aria-controls')));
  const steps=all('.step-button'), details=all('.step-detail');
  steps.forEach(b=>b.addEventListener('click',()=>choose(steps,details,b,'aria-controls')));
  const dialog=$('#image-dialog'), expanded=$('#expanded-image'), caption=$('#image-caption');
  if (typeof dialog.showModal === 'function') {
    all('.media-open').forEach(b=>b.addEventListener('click',()=>{
      const src=assetUrl(b.dataset.src,document.baseURI);if(!src)return;
      expanded.src=src;expanded.alt=b.dataset.alt||'';caption.textContent=b.dataset.caption||'';dialog.classList.toggle('long-image',b.dataset.long==='true');dialog.showModal();dialog.scrollTop=0;
    }));
    $('.dialog-close').addEventListener('click',()=>dialog.close());
    dialog.addEventListener('click',event=>{
      const r=dialog.getBoundingClientRect();
      if(event.clientX<r.left||event.clientX>r.right||event.clientY<r.top||event.clientY>r.bottom)dialog.close();
    });
    dialog.addEventListener('close',()=>{expanded.removeAttribute('src');});
  }
  const comparisonStages=all('.comparison-stage');
  all('input[data-compare]').forEach(range=>{
    const key=range.dataset.compare;
    const stage=comparisonStages.find(el=>el.dataset.comparison===key);
    const output=$('#compare-output-'+key);
    if(!stage || !output)return;
    const update=()=>{
      const value=Math.min(100,Math.max(0,Number(range.value)||0));
      stage.style.setProperty('--split',value+'%');
      output.value=value+'%';
      range.setAttribute('aria-valuetext',`分界线在 ${value}% 位置，左侧输入，右侧掩膜叠加`);
    };
    range.addEventListener('input',update);update();
    let activePointer=null;
    const updateFromPointer=event=>{
      const rect=stage.getBoundingClientRect();if(rect.width<=0)return;
      range.value=String(Math.round(Math.min(100,Math.max(0,(event.clientX-rect.left)/rect.width*100))));
      update();
    };
    stage.addEventListener('pointerdown',event=>{
      if(event.button!==0 || activePointer!==null)return;
      activePointer=event.pointerId;stage.setPointerCapture?.(event.pointerId);updateFromPointer(event);
    });
    stage.addEventListener('pointermove',event=>{if(event.pointerId===activePointer)updateFromPointer(event);});
    const release=event=>{
      if(event.pointerId!==activePointer)return;
      if(stage.hasPointerCapture?.(event.pointerId))stage.releasePointerCapture(event.pointerId);
      activePointer=null;
    };
    stage.addEventListener('pointerup',release);stage.addEventListener('pointercancel',release);
  });
  all('.comparison-controls').forEach(el=>{el.hidden=false;});
  document.documentElement.classList.add('enhanced');
  function attachLink(id,url) {
    const el=$(id);if(!url)return;
    el.href=url;el.hidden=false;
  }
  async function configure() {
    try {
      const response=await fetch(new URL('./config/site.json',document.baseURI),{cache:'no-store',credentials:'omit'});
      if(!response.ok)throw new Error('CONFIG_UNAVAILABLE');
      const c=await response.json();if(!configValid(c))throw new Error('CONFIG_INVALID');
      const demoUrl=publicDemoUrl(c.demo.url,c.demo.allowHttp===true);
      if(c.demo.enabled===true && demoUrl && ['lan','eci'].includes(c.demo.deploymentMode)) {
        attachLink('#live-link',demoUrl);
        attachLink('#nav-live-link',demoUrl);
        $('#nav-live-link').setAttribute('target','_blank');
        $('#nav-live-link').setAttribute('rel','noopener noreferrer');
        $('#nav-live-link').setAttribute('aria-label','在新窗口打开在线工作台');
        $('#demo-status').textContent=c.demo.statusText || '实时演示入口已配置';
        $('.demo-status').classList.add('available');
        const verification=confirmedDate(c.demo.lastVerifiedAt)?`最近人工确认：${c.demo.lastVerifiedAt}`:'地址由项目本人提供';
        $('#demo-verified').textContent=`${c.demo.deploymentMode==='lan'?'LAN GPU API':'OSS + ECI'} · ${new URL(demoUrl).protocol==='http:'?'HTTP':'HTTPS'} · ${verification}`;
        $('#demo-verified').hidden=false;
      } else if(c.demo.enabled===false && c.demo.statusText) $('#demo-status').textContent=c.demo.statusText;
      attachLink('#repository-link',publicHttps(c.links.githubRepositoryUrl));
      attachLink('#nav-repository-link',publicHttps(c.links.githubRepositoryUrl));
      attachLink('#docs-link',publicHttps(c.links.projectDocsUrl));
    } catch (_) {
      // Missing/broken configuration fails closed. All generated core content remains visible.
      $('#demo-status').textContent='实时入口未配置，可继续阅读项目内容';
    }
  }
  configure();
})();
