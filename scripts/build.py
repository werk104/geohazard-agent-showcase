#!/usr/bin/env python3
"""Render content.json into a complete, buildless GitHub Pages homepage. Stdlib only."""
import argparse
import html
import json
from pathlib import Path
from urllib.parse import urlsplit
ROOT = Path(__file__).resolve().parents[1]

def e(value):
    return html.escape(str(value), quote=True)

def media_path(value):
    if not isinstance(value, str) or not value.startswith('./assets/') or '?' in value or '#' in value:
        raise ValueError('Media paths must begin with ./assets/ and have no query or fragment')
    path = (ROOT / value[2:]).resolve()
    if not path.is_relative_to(ROOT / 'assets') or not path.is_file():
        raise ValueError('Missing or invalid media path: ' + value)
    return value

def render(c):
    page=c['page']; hero=c['hero']; bg=c['background']; ar=c['architecture']; wf=c['workflow']; rs=c['results']; eng=c['engineering']; dm=c['demo']
    def figure(key, hero=False):
        m=c['media'][key]; path=media_path(m['src']); full=media_path(m.get('fullSrc',m['src'])); badge='<span class="media-badge">素材待补充</span>' if m['placeholder'] else '<span class="media-badge ready">案例图像</span>'
        return f'''<figure class="media-figure"><button type="button" class="media-open" data-src="{e(full)}" data-long="{str(m.get('scrollFull',False)).lower()}" data-alt="{e(m['alt'])}" data-caption="{e(m['caption'])}" aria-label="放大查看：{e(m['caption'])}">{badge}<img src="{e(path)}" alt="{e(m['alt'])}" width="{int(m.get('width',1200))}" height="{int(m.get('height',760))}" {'fetchpriority="high"' if hero else 'loading="lazy"'}><span class="expand" aria-hidden="true">↗</span></button><figcaption>{e(m['caption'])}</figcaption></figure>'''
    def heading(num, en, title, text=''):
        return f'<div class="section-head"><p class="eyebrow">{e(num)} / {e(en)}</p><h2>{e(title)}</h2>{f"<p class=section-intro>{e(text)}</p>" if text else ""}</div>'
    def icon(name):
        paths={
          'route':'<circle cx="5" cy="5" r="2"/><circle cx="19" cy="19" r="2"/><path d="M7 5h8a4 4 0 0 1 0 8H9a4 4 0 0 0 0 8h8"/>',
          'nodes':'<rect x="9" y="2" width="6" height="6" rx="1"/><rect x="2" y="16" width="6" height="6" rx="1"/><rect x="16" y="16" width="6" height="6" rx="1"/><path d="M12 8v4H5v4m7-4h7v4"/>',
          'layers':'<path d="m12 2 10 5-10 5L2 7l10-5Zm-10 10 10 5 10-5M2 17l10 5 10-5"/>',
          'chip':'<rect x="5" y="5" width="14" height="14" rx="2"/><path d="M9 1v4m6-4v4M9 19v4m6-4v4M1 9h4m-4 6h4m14-6h4m-4 6h4"/><path d="M9 9h6v6H9z"/>',
          'check':'<path d="m12 2 9 4v6c0 5-9 10-9 10S3 17 3 12V6l9-4Z"/><path d="m8 12 3 3 5-6"/>',
          'map':'<path d="m2 5 7-3 6 3 7-3v17l-7 3-6-3-7 3V5Zm7-3v17m6-14v17"/>'}
        return f'<svg viewBox="0 0 24 24" aria-hidden="true" fill="none" stroke="currentColor" stroke-width="1.4" stroke-linecap="round" stroke-linejoin="round">{paths[name]}</svg>'
    cards=''.join(f'<article class="feature"><span class="feature-icon">{icon(f["icon"])}</span><div><h3>{e(f["title"])}</h3><p>{e(f["text"])}</p><span class="micro">{e(f["detail"])}</span></div></article>' for f in c['features'])
    step_buttons=''.join(f'<button type="button" id="step-button-{i}" class="step-button {"selected" if i==0 else ""}" aria-controls="step-{i}" aria-pressed="{str(i==0).lower()}" data-step="{i}"><span class="step-no">{i+1:02}</span><span><strong>{e(s["title"])}</strong><small>{e(s["short"])}</small></span><span class="step-arrow" aria-hidden="true">↗</span></button>' for i,s in enumerate(wf['steps']))
    step_details=''.join(f'<article class="step-detail {"selected" if i==0 else ""}" id="step-{i}" aria-labelledby="step-title-{i}"><p class="eyebrow">STEP {i+1:02} / {len(wf["steps"]):02}</p><h3 id="step-title-{i}">{e(s["title"])}</h3><dl><dt>输入</dt><dd>{e(s["input"])}</dd><dt>处理</dt><dd>{e(s["action"])}</dd><dt>输出</dt><dd>{e(s["output"])}</dd></dl><p class="tool-name">{e(s["tool"])}</p><p class="flow-label">流程示意 · 无后台任务执行</p></article>' for i,s in enumerate(wf['steps']))
    def comparison(key):
        v=c.get('comparisons',{}).get(key,{})
        if v.get('enabled') is not True:
            return figure(key)
        inp=media_path(v['input']);ov=media_path(v['overlay']);mask=media_path(v['mask'])
        w,h=int(v['width']),int(v['height'])
        if w<=0 or h<=0:raise ValueError('Invalid comparison dimensions')
        return f'''<figure class="comparison-figure"><div class="comparison-stage" data-comparison="{e(key)}" style="--split:50%"><img src="{e(inp)}" alt="{e(v['inputLabel'])}，与右侧叠加图空间对齐" width="{w}" height="{h}" loading="lazy"><div class="comparison-result"><img src="{e(ov)}" alt="{e(v['resultLabel'])}，红色为提供的预测前景" width="{w}" height="{h}" loading="lazy"></div><div class="comparison-line" aria-hidden="true"><span>↔</span></div><span class="comparison-label label-left">{e(v['inputLabel'])}</span><span class="comparison-label label-right">{e(v['resultLabel'])}</span></div><div class="comparison-controls" hidden><label for="compare-{e(key)}">拖动分界线对比</label><input type="range" id="compare-{e(key)}" data-compare="{e(key)}" min="0" max="100" value="50" aria-valuetext="分界线在 50% 位置，左侧输入，右侧掩膜叠加"><output for="compare-{e(key)}" id="compare-output-{e(key)}">50%</output></div><figcaption>{e(c['media'][key]['caption'])}</figcaption><button type="button" class="media-open comparison-open" data-src="{e(ov)}" data-alt="{e(c['media'][key]['alt'])}" data-caption="{e(c['media'][key]['caption'])}">放大查看叠加成果 ↗</button></figure>'''
    results=''
    for k in ['landslide','crack']:
        v=c.get('comparisons',{}).get(k,{})
        extra=''
        if v.get('enabled') is True:
            extra=f'''<p class="processing-note">{e(v['note'])}</p><details class="mask-details"><summary>查看二值预测掩膜</summary><img src="{e(media_path(v['mask']))}" width="{int(v['width'])}" height="{int(v['height'])}" alt="白色为预测像素 1，黑色为背景的二值掩膜" loading="lazy"><p>白色：原始预测值 1；黑色：背景 0。此处为显示图，不是人工标注真值。</p></details>'''
        results+=f'''<article class="result-case">{comparison(k)}<div class="case-copy"><p class="eyebrow">{e(rs[k]['tag'])}</p><h3>{e(rs[k]['title'])}</h3><p>{e(rs[k]['text'])}</p><ul class="fact-list">'''+''.join(f'<li>{e(t)}</li>' for t in rs[k]['facts'])+'</ul>'+extra+'</div></article>'
    channel_section=''
    contract=c.get('inputContract')
    if contract:
        groups=''.join(f'<div><span>{e(g["label"])}</span><strong>{e(g["count"])}</strong><small>{e(g["detail"])}</small></div>' for g in contract['groups'])
        rows=''.join(f'<tr><td>{e(r["channels"])}</td><td>{e(r["name"])}</td><td>{e(r["order"])}</td></tr>' for r in contract['rows'])
        channel_section=f'''<div class="input-contract"><div class="contract-title"><p class="eyebrow">26 CHANNELS / INPUT CONTRACT</p><h3>{e(contract['title'])}</h3><p>{e(contract['intro'])}</p></div><div class="contract-groups">{groups}</div><details class="channel-table"><summary>查看全部 26 通道顺序</summary><div class="table-scroll" tabindex="0" aria-label="26 通道顺序表，小屏可横向滚动"><table><thead><tr><th scope="col">通道编号</th><th scope="col">分组</th><th scope="col">内容与顺序</th></tr></thead><tbody>{rows}</tbody></table></div><p>{e(contract['rgbNote'])}</p></details></div>'''
    session_evidence=''
    if c.get('ui',{}).get('evidence'):
        ev=c['ui']['evidence']
        rows=''.join(f'<tr><td>{e(r["step"])}</td><td><code>{e(r["tool"])}</code></td><td><span class="historical-success">{e(r["status"])}</span></td><td>{e(r["result"])}</td></tr>' for r in ev['rows'])
        session_evidence=f'''<details class="session-evidence"><summary>{e(ev['title'])}</summary><p>{e(ev['intro'])}</p><div class="evidence-scroll" tabindex="0" aria-label="历史会话执行摘要，小屏可横向滚动"><table><thead><tr><th scope="col">步骤</th><th scope="col">工具</th><th scope="col">记录状态</th><th scope="col">结果摘要</th></tr></thead><tbody>{rows}</tbody></table></div><p>{e(ev['note'])}</p></details>'''
    ui_section='' 
    if c.get('ui'):
        u=c['ui']
        ui_section=f'''<section class="section interface-section" id="interface"><div class="wrap">{heading('INTERFACE','REAL WORKBENCH',u['title'],u['intro'])}<div class="ui-grid"><article class="ui-card ui-overview"><h3>{e(u['overviewTitle'])}</h3>{figure('workbench')}<p class="ui-note">{e(u['overviewNote'])}</p></article><article class="ui-card ui-map"><h3>{e(u['mapTitle'])}</h3>{figure('mapPreview')}<p class="ui-note">{e(u['mapNote'])}</p><div class="ui-detail-tags"><span>会话控制</span><span>OSS 文件管理</span><span>图层开关</span><span>透明度</span></div></article></div>{session_evidence}</div></section>'''
    contributions=''
    if c['contribution']['enabled'] is True:
        co=c['contribution']
        if not co['items']: raise ValueError('Enabled contribution section needs confirmed items')
        contributions=f'<section class="section contribution" id="contribution"><div class="wrap">{heading("07","MY ROLE",co["title"],co["intro"])}<ul class="contribution-list">'+''.join(f'<li>{e(t)}</li>' for t in co['items'])+'</ul></div></section>'
    faq=''.join(f'<details><summary>{e(f["question"])}</summary><p>{e(f["answer"])}</p></details>' for f in c['faq'])
    return f'''<!doctype html>
<!-- Generated by scripts/build.py from content.json. Edit content.json, then rebuild. -->
<html lang="zh-CN">
<head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{e(page['title'])}</title><meta name="description" content="{e(page['description'])}">
<meta name="theme-color" content="#102b3b"><meta property="og:title" content="{e(page['title'])}"><meta property="og:description" content="{e(page['description'])}"><meta property="og:type" content="website">
<link rel="icon" type="image/svg+xml" href="./assets/diagrams/mark.svg"><link rel="stylesheet" href="./css/styles.css"><script src="./js/app.js" defer></script>
</head>
<body>
<a class="skip-link" href="#main">跳至正文</a>
<header class="site-header"><div class="wrap header-inner"><a href="#top" class="brand"><img src="./assets/diagrams/mark.svg" alt="" width="36" height="36"><span>{e(page['brand'])}<small>REMOTE SENSING WORKBENCH</small></span></a><button class="menu-toggle" type="button" aria-expanded="false" aria-controls="main-nav">导航 <span aria-hidden="true">☰</span></button><nav id="main-nav" aria-label="主导航"><a href="#overview">项目概览</a><a href="#interface">工作台界面</a><a href="#architecture">系统架构</a><a href="#workflow">工作流程</a><a href="#results">案例成果</a><a class="nav-demo" id="nav-live-link" href="#demo">在线体验 <span aria-hidden="true">↗</span></a></nav></div></header>
<main id="main">
<section class="hero" id="top"><div class="wrap hero-grid"><div class="hero-copy"><p class="eyebrow"><span class="dot"></span>{e(hero['eyebrow'])}</p><p class="project-subtitle">{e(page['subtitle'])}</p><h1>{e(hero['headline'][0])}<br><span>{e(hero['headline'][1])}</span></h1><p class="hero-lead">{e(hero['lead'])}</p><div class="hero-actions"><a class="button primary" href="#workflow">了解工作流程 <span aria-hidden="true">↗</span></a><a class="text-link" href="#results">查看案例展示 <span aria-hidden="true">→</span></a></div><p class="hero-note">{e(hero['note'])}</p></div><div class="hero-visual"><div class="visual-top"><span>{e(hero.get("visualEyebrow","WORKBENCH / OVERVIEW"))}</span><span class="outline-label">{e(hero.get("visualBadge","展示素材预留"))}</span></div>{figure('hero' if 'hero' in c['media'] else 'workbench',True)}<div class="visual-bottom"><span>{e(hero.get("visualSteps",["任务组织","工具执行","成果预览"])[0])}</span><i aria-hidden="true">→</i><span>{e(hero.get("visualSteps",["任务组织","工具执行","成果预览"])[1])}</span><i aria-hidden="true">→</i><span>{e(hero.get("visualSteps",["任务组织","工具执行","成果预览"])[2])}</span></div></div></div><div class="wrap tech-row"><span class="tech-label">BUILT WITH</span>{''.join(f'<span>{e(t)}</span>' for t in hero['tags'])}</div></section>
<section class="section" id="overview"><div class="wrap intro-grid"><div><p class="eyebrow">{e(bg['eyebrow'])}</p><h2>{e(bg['title'])}</h2></div><div class="intro-copy">{''.join(f'<p>{e(t)}</p>' for t in bg['paragraphs'])}</div></div><div class="wrap principles">{''.join(f'<div><span class="principle-no">0{i+1}</span><h3>{e(t["title"])}</h3><p>{e(t["text"])}</p></div>' for i,t in enumerate(bg['principles']))}</div></section>
<section class="section section-muted" id="capabilities"><div class="wrap">{heading('02','CAPABILITIES','连接业务能力，而不止于对话。','从数据准备到结果查看，每一环都由实际工具和服务承担。以下为项目能力说明，具体工具集合依部署模式而定。')}<div class="feature-grid">{cards}</div></div></section>
{ui_section}
<section class="section" id="architecture"><div class="wrap">{heading('03','ARCHITECTURE',ar['title'],ar['intro'])}<div class="architecture-switch" aria-label="选择架构说明"><button type="button" class="arch-button selected" data-arch="lan" aria-controls="arch-lan" aria-pressed="true">LAN · 远程 GPU API</button><button type="button" class="arch-button" data-arch="eci" aria-controls="arch-eci" aria-pressed="false">云端 · OSS + ECI</button><span>架构示意 / 非运行状态</span></div><div class="architecture-panels"><figure class="arch-panel selected" id="arch-lan"><div class="diagram-canvas" tabindex="0" aria-label="LAN 架构图，小屏可横向滚动"><img src="./assets/diagrams/architecture-lan.svg" width="1100" height="650" alt="LAN 架构：浏览器进入应用工作台；Agent 与 MCP 连接数据服务及 GPU API，成果经应用侧校验后进入地图预览" loading="lazy"></div><figcaption>{e(ar['lanCaption'])}</figcaption></figure><figure class="arch-panel" id="arch-eci"><div class="diagram-canvas" tabindex="0" aria-label="云端架构图，小屏可横向滚动"><img src="./assets/diagrams/architecture-eci.svg" width="1100" height="650" alt="云端架构：应用工作台通过 OSS 和 ECI 滑坡推理作业衔接成果，再返回地图预览" loading="lazy"></div><figcaption>{e(ar['eciCaption'])}<br>{e(ar['eciNote'])}</figcaption></figure></div><div class="architecture-note"><strong>共同的交付目标</strong><p>将任务、运行记录与成果来源关联，支持查看、复用与排查。两条路径的具体协议和检查范围分别说明。</p></div></div></section>
<section class="section workflow-section" id="workflow"><div class="wrap">{heading('04','FROM REQUEST TO RESULTS',wf['title'],wf['intro'])}<div class="workflow-grid"><div class="step-list" aria-label="流程步骤">{step_buttons}</div><div class="step-panels">{step_details}</div></div><div class="input-strip"><div><p class="eyebrow">INPUT / MULTITEMPORAL</p><h3>两个时相，明确的模型输入。</h3><p>{e(wf.get("inputText","前后时相分别获取，再按既定合同进行网格处理与通道组合。"))}</p></div>{figure('inputs')}</div>{channel_section}</div></section>
<section class="section" id="results"><div class="wrap">{heading('05','CASE GALLERY',rs['title'],rs['intro'])}<div class="case-grid">{results}</div><p class="section-footnote">{e(rs.get("footnote","所有候选掩膜均需专业复核。"))}</p></div></section>
<section class="section section-muted" id="engineering"><div class="wrap engineering-grid"><div>{heading('06','ENGINEERING',eng['title'])}<div class="engineering-list">{''.join(f'<article><span>0{i+1}</span><div><h3>{e(t["title"])}</h3><p>{e(t["text"])}</p></div></article>' for i,t in enumerate(eng['items']))}</div></div><div class="engineering-media">{figure('trace')}<p class="small-note">资料基准：{e(page['evidenceDate'])}。页面不以历史回归数量替代模型精度或在线稳定性证明。</p></div></div></section>
{contributions}
<section class="section demo-section" id="demo"><div class="wrap live-callout"><div><p class="eyebrow">EXPLORE / LIVE SERVICE</p><h2>{e(dm['title'])}</h2><p class="live-description">{e(dm['text'])}</p></div><div class="live-entry"><div class="demo-status"><span class="status-dot"></span><span id="demo-status">实时服务暂未开放</span></div><p class="verification" id="demo-verified" hidden></p><div class="demo-actions"><a class="button primary" id="live-link" target="_blank" rel="noopener noreferrer" hidden>打开在线交互演示 ↗</a><a class="text-link" href="#results">查看静态成果 →</a></div><p class="small-note">在线状态由管理员人工确认，本页不自动探测后端。</p></div></div></section>
<section class="section faq-section"><div class="wrap faq-grid"><div><p class="eyebrow">NOTES / SCOPE</p><h2>关于展示与使用范围。</h2><p>功能、成果和运行状态分别说明。</p></div><div class="faq-list">{faq}</div></div></section>
</main>
<footer><div class="wrap footer-main"><div><a class="footer-brand" href="#top">{e(page['brand'])}</a><p>{e(c['footer']['note'])}</p></div><div class="footer-links"><a id="repository-link" target="_blank" rel="noopener noreferrer" hidden>展示仓库 ↗</a><a id="docs-link" target="_blank" rel="noopener noreferrer" hidden>公开文档 ↗</a><a href="#top">返回顶部 ↑</a></div></div><div class="wrap footer-bottom"><span>{e(c['footer']['credits'])}</span><span>内容更新：<time datetime="{e(page['updated'])}">{e(page['updated'])}</time></span></div></footer>
<dialog id="image-dialog" aria-labelledby="image-caption"><button class="dialog-close" type="button" aria-label="关闭放大图片">关闭 ×</button><img id="expanded-image" alt=""><p id="image-caption"></p></dialog>
<noscript><div class="noscript-note">当前未启用 JavaScript。项目内容、两种架构和全部流程仍可阅读；图片放大、对比分界线拖动及实时外链配置暂不可用。</div></noscript>
</body></html>'''

def main():
    parser=argparse.ArgumentParser();parser.add_argument('--check',action='store_true');args=parser.parse_args()
    c=json.loads((ROOT/'content.json').read_text(encoding='utf-8'))
    output=render(c)
    target=ROOT/'index.html'
    if args.check:
        if not target.exists() or target.read_text(encoding='utf-8')!=output:
            raise SystemExit('index.html is out of date. Run python scripts/build.py')
        print('Content and generated HTML match.')
    else:
        target.write_text(output,encoding='utf-8');print('Generated index.html')
if __name__=='__main__':main()
