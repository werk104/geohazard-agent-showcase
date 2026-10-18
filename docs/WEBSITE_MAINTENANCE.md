# 展示网站维护说明

本仓库维护 GeoHazard Agent 的静态展示网站。项目功能、案例和个人职责见[项目介绍](../README.md)；本文件记录当前维护方式，历史迁移说明见文末归档。

展示地址：https://werk104.github.io/geohazard-agent-showcase/

下列命令均在仓库根目录执行。

## 文件与职责

| 修改目标 | 文件或目录 | 后续操作 |
| --- | --- | --- |
| 标题、功能、工作流、案例说明、个人职责 | `content.json` | 重新生成首页，或交由现有 Actions 构建 |
| 项目介绍与个人职责 | `README.md` | 直接提交；职责表述与 `content.json` 保持一致 |
| 在线入口、GitHub 链接 | `config/site.json` | 直接提交 |
| 图片与截图 | `assets/images/`、`content.json → media / comparisons` | 同步更新路径、尺寸和说明，重新生成首页 |
| 字号、布局与配色 | `css/styles.css` | 直接提交 |
| 页面交互与配置加载 | `js/app.js` | 检查语法与交互后提交 |
| 页面结构模板 | `scripts/build.py` | 修改后生成首页 |
| 系统架构图 | `assets/diagrams/` | 修改 SVG 并核对图注 |

`content.json` 是网页文案的编辑源，`index.html` 是生成结果。不要只手改首页，否则下次构建会覆盖修改。`page.updated` 记录内容更新时间，`page.evidenceDate` 表示功能资料基准日期，不能因改文案而自动更新后者。

## 日常更新与发布

在工作区无未提交修改时，先同步现有仓库：

```bash
git status
git pull --ff-only origin main
```

修改对应文件后，本机有 Python 与 Node.js 时运行：

```bash
python scripts/build.py
python scripts/check.py
node --check js/app.js
```

检查改动后，添加本次实际变更的文件并提交、推送。提交只保存到本地；推送成功才会更新远端。失败时先解决报错，不使用强制推送或硬重置。

### GitHub Actions 发布

现有工作流是 `.github/workflows/pages.yml`，名称为 `Build and deploy showcase`。推送到 `main` 后，工作流生成并检查首页，将公开文件暂存至 `_site/`，再部署到 Pages。使用该方式时，仓库 `Settings → Pages → Source` 应为 `GitHub Actions`。

本机没有 Python 或 Node.js 时，可以将内容修改交由现有工作流构建。提交后查看 Actions 结果，部署成功后刷新展示页。

### 分支根目录发布

如果仓库仍使用 `main / (root)` 发布，应先在本机运行构建，并将生成的 `index.html` 一起提交。仅修改 `content.json` 不会更新已生成的页面。继续使用已有发布方式即可，不必因整理文档而切换 Pages 设置。

## 在线体验与仓库入口

`config/site.json` 的 `demo` 对象控制在线体验。当前提供的配置为：

```json
{
  "enabled": true,
  "url": "http://121.40.114.105:7860",
  "allowHttp": true,
  "deploymentMode": "eci",
  "statusText": "在线体验入口已配置",
  "lastVerifiedAt": null
}
```

这是 `demo` 对象，不是完整配置。修改时保留 `schemaVersion` 和 `links`。HTTP 在线入口需要明确启用 `allowHttp`；改为 HTTPS 后可将其关闭。暂停入口时，将 `enabled` 设为 `false`。

`links.githubRepositoryUrl` 同时控制顶部 GitHub 入口和页脚仓库入口，当前值为 `https://github.com/werk104/geohazard-agent-showcase`。仓库及文档外链仅接受 HTTPS。

配置由浏览器读取，链接在新窗口打开。静态网站不会自动请求模型或检查业务服务健康状态。`lastVerifiedAt: null` 表示未填写人工核实时间；只有实际检查后才填写带时区的 ISO 8601 时间。配置读取失败时，静态正文仍可阅读，动态入口按降级逻辑处理。

## 图片、截图与素材说明

- [图片替换与路径对应](IMAGE_REPLACEMENT.md)
- [26 通道组成、案例网格与导出说明](DEMO_ASSETS.md)
- [界面截图及历史会话摘要](UI_SCREENSHOTS.md)

替换案例时，输入图、叠加图与二值掩膜必须保持一致的展示范围和画布，同步更新 `comparisons` 的路径与尺寸。长截图可配置 `fullSrc` 和 `scrollFull: true`。

`assets/ASSET_CREDITS.json`、`DEMO_PROCESSING.json`、`UI_PROCESSING.json` 与 `SESSION_EVIDENCE_20261017.json` 是素材来源、显示处理及公开历史摘要，应保留。历史执行记录不表示当前服务状态，也不构成模型精度评估。

若需在保存原始 TIFF 的本机重新导图，使用：

```bash
python -m pip install -r scripts/requirements-assets.txt
python scripts/export_demo_assets.py --source "原始四份TIFF所在目录"
```

这些依赖仅用于重新制作素材，常规网站构建使用 Python 标准库。原始 TIFF、原始会话归档和模型权重不放入展示仓库。当前不展示视频或视频占位。

## 本地预览与更新后核对

```bash
python -m http.server 8088 --bind 127.0.0.1
```

打开 http://127.0.0.1:8088/ ，不要用双击 HTML 的方式检查配置加载。检查导航、GitHub 与在线体验链接、个人职责、图片放大、长图滚动、对比滑块和移动端布局。

`scripts/check.py` 检查资源、锚点和生成结果一致性，`node --check` 检查 JavaScript 语法；二者不能替代浏览器布局与实际线上访问检查。

## 定期整理

历史升级说明集中放入 `docs/archive/`，维护入口保持在本文件。新增图片前后应检查引用；已被新素材替代且未被页面、文档、素材清单或导出脚本引用的文件，可以从当前版本移除。单纯从当前版本删除文件不会清除 Git 历史中的旧文件。

`scripts/build.py`、`check.py`、`package_site.py`、`export_demo_assets.py`、`requirements-assets.txt` 和 `.github/workflows/pages.yml` 仍有维护或发布用途，不属于应删除的历史遗留文件。`_site/` 与 Python 缓存属于生成物，不提交到 Git；现有 `.gitignore` 已覆盖它们。

## 历史更新归档

以下文件保留原文，用于追溯当时的迁移过程。其中的覆盖清单、配置状态与执行命令只适用于对应历史版本；当前操作以上文为准。

| 历史迁移 | 归档 |
| --- | --- |
| v2 → v3：界面截图及移除视频占位 | [UPDATE_FROM_V2.md](archive/UPDATE_FROM_V2.md) |
| v3 → v4：新长截图、会话摘要及在线入口 | [UPDATE_FROM_V3.md](archive/UPDATE_FROM_V3.md) |

v5 将 README 改为项目介绍、公开个人职责，并增加顶部 GitHub 入口；文档整理将上述两份迁移说明移至归档目录，清除无引用的旧占位图与旧界面截图。
