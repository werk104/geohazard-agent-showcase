# 展示网站维护说明

GitHub Pages 静态项目展示页。目标网址：
https://werk104.github.io/geohazard-agent-showcase/

本包是待上传的网站文件，不表示已有线上内容被替换。采用本地字体与资源，无 npm、CDN、地图瓦片、后端或模型依赖。已补入真实双时相影像、滑坡与裂缝预测结果，提供静态对比滑块与二值掩膜查看；已加入 P01 工作台长图、P05 工具调用片段与 P06 地图预览界面，均为脱敏公开副本。架构图已绘制。个人职责已按项目本人确认的范围公开；本版已按用户要求配置独立在线体验入口。

## 从上一版更新

v4 素材更新参考仓库根目录的 `UPDATE_FROM_V3.md`：已有仓库可直接覆盖更新文件并提交，不必重新克隆或修改 Pages 设置。保留 `.git/`；这次需要更新 `config/site.json` 的 `demo` 对象，并同步替换 `js/app.js`。不包含原始 GeoTIFF 或会话归档。

## 首次上传：推荐使用 GitHub Actions

这种方式以后只改 `content.json`，提交后 GitHub 自动生成首页并发布，不需要本机安装 Python。

1. 解压 ZIP，打开 `geohazard-agent-showcase` 目录。
2. 进入现有仓库 `werk104/geohazard-agent-showcase` 的 `Settings → Pages`，将 `Source` 从 `Deploy from a branch` 改为 **GitHub Actions**。
3. 回到 `Code → Add file → Upload files`，把目录**里面的文件与子目录**上传到仓库根目录，替换原 `index.html`。不要把外层 `geohazard-agent-showcase/` 再套进仓库。
4. 检查根目录能看到 `index.html`、`content.json`、`config/`、`assets/`、`css/`、`js/`、`scripts/`，以及 `.github/workflows/pages.yml`。
5. 如果网页上传漏掉 `.github`，使用 `Add file → Create new file` 创建 `.github/workflows/pages.yml`，复制本包对应文件内容后提交。同理可用此方式添加 `.nojekyll`，但 Actions 发布本身不依赖它。
6. 提交到 `main`。在 `Actions → Build and deploy showcase` 查看结果，成功后刷新原网址。工作流未启动时，可以在其页面点 `Run workflow` 手动运行。

默认 URL 不变。首次更新可能需要数分钟；旧缓存可强制刷新。

Actions 配置参考：
https://docs.github.com/en/pages/getting-started-with-github-pages/using-custom-workflows-with-github-pages

## 保持原来的分支发布方式

也可以继续使用 `main / (root)`：上传 `index.html`、`.nojekyll`、`assets/`、`css/`、`js/`、`config/`、`docs/`，**暂不上传 `.github/`**。本包首页已生成，可以直接显示。

这种模式下，改文案后需要先运行：

```bash
python scripts/build.py
```

再将生成的 `index.html` 一起上传。仅修改 `content.json` 不会改变网页；仅修改配置链接或替换同路径图片则无需生成首页。

## 日常维护：只记三个位置

| 想修改的内容 | 修改位置 | 后续操作 |
| --- | --- | --- |
| 标题、简介、功能、流程、结果说明、图注 | `content.json` | Actions 模式直接提交；分支模式先运行生成脚本 |
| 图片文件、路径、alt、占位标记 | `assets/images/` 与 `content.json → media` | 上传图片并修改路径，重新生成 |
| 在线演示开关、地址、仓库链接 | `config/site.json` | 直接提交，不需要重新生成首页 |
| 布局、颜色、字号 | `css/styles.css` | 直接提交 |
| LAN / ECI 架构图 | `assets/diagrams/architecture-*.svg` | 替换 SVG，保留准确图注 |

所有核心文案以 `content.json` 为唯一编辑源。`index.html` 为生成结果，不建议手动改，否则下一次生成会覆盖。JSON 使用英文双引号，末项不要加逗号；段落正文不要写 HTML 标签。`page.updated` 是内容更新日期；`page.evidenceDate` 是功能资料的基准日期，不要未经复验就同时改新。

## 替换图片

详见 [图片替换说明](IMAGE_REPLACEMENT.md)。P01—P06 均已补入真实素材，首页使用滑坡叠加成果；工作台长截图可点击后滚动查看。可以仅提供授权的 PNG/WebP，不必提供原始地理数据。

更换真实案例时，同时更新 `media` 与 `comparisons` 的配对路径及尺寸，不能仅替换一张图。本轮已同步更新案例、界面展示和图注。

## 维护个人职责

当前职责已启用；修改时保持 `content.json` 与 README 中的职责描述一致。所有命令均在仓库根目录执行。

在 `content.json → contribution` 中填写真实确认的职责，最后将 `enabled` 改成 `true`。例如：

```json
{
  "enabled": true,
  "title": "个人负责部分",
  "intro": "在现有工程及团队协作基础上，主要承担以下工作。",
  "items": ["填写本人确认的第一项职责", "填写本人确认的第二项职责"]
}
```

不要直接把此示例当作职责证明。

## 在线交互入口

`config/site.json` 的 `demo` 对象集中管理在线入口。本版已设为：

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

在线按钮需 `enabled` 为布尔值 `true`、地址合法且模式为 `lan` 或 `eci`。默认接受公开 HTTPS 地址；HTTP 只在 `demo.allowHttp` 明确为 `true` 时允许用于在线入口。其他文档 / 仓库外链仍只接受 HTTPS，站内媒体继续使用本地相对路径。

本机、内网、保留地址、带用户名密码、查询串或片段的 URL 会被拒绝。页面不放 API key，不嵌入服务，不自动请求模型、MCP 或健康接口。入口会在新窗口打开；配置状态不代表自动探活。

`lastVerifiedAt` 可为空，此时显示“地址由项目本人提供”。本人实际检查后，可填写带时区的 ISO 8601 时间，再显示“最近人工确认”。不能用网页加载时间伪造核实时间。

关闭入口：将 `enabled` 改回 `false`。保持 HTTPS 默认约束：将 `allowHttp` 设为 `false`。配置缺失、损坏或字段类型错误时，入口保持关闭，静态正文仍可阅读。

本版不展示视频，不保留视频占位。旧配置中的 `video` 字段会被忽略。

## 真实素材与通道说明

详细导出方法、26 通道映射、两种案例的空间配对及网格差异见 [案例素材说明](DEMO_ASSETS.md)；可复核摘要见 `assets/DEMO_PROCESSING.json`。

`content.json → inputContract` 控制通道表；`comparisons` 控制每个案例的输入图、叠加图、二值图和原始导出尺寸。比较器仅裁切显示叠放图层，不会更改数据。原始 TIFF 不随站点分发。

如需重新导图，可在自己保存原 TIFF 的环境安装 `scripts/requirements-assets.txt`，然后运行：

```bash
python -m pip install -r scripts/requirements-assets.txt
python scripts/export_demo_assets.py --source "原始四份TIFF所在目录"
```

导图脚本只在本地重新制作素材时使用。常规 Pages 发布仍只需要 Python 标准库，不需要 GDAL、Rasterio 或 Pillow。

## 本地检查

需要 Python 3.10 或更新版本；GitHub Actions 默认环境无需另装依赖。

```bash
python scripts/build.py
python scripts/check.py
node --check js/app.js
python -m http.server 8088 --bind 127.0.0.1
```

打开 http://127.0.0.1:8088/ 。不要通过双击 HTML 来测试配置读取；`file://` 通常无法读取 JSON。部署的 GitHub Pages 使用 HTTPS，不受此限制。

建议在最终站点检查手机布局、导航、两种架构切换、六个流程步骤、图片放大、长截图滚动、FAQ 和外链。可以在站点父目录起静态服务，以 `/geohazard-agent-showcase/` 前缀访问，检查项目子路径。

## 历史会话与截图

v4 已替换为 `长截图2.jpeg` 对应材料，并在界面区提供 2026-10-17 可展开摘要。资料提取范围见 [界面截图说明](UI_SCREENSHOTS.md)；原始归档不发布。新截图中的执行输入与原有 TIFF 案例区分别说明。

## 本次交付验证

交付时检查了生成文件一致性、图片 / SVG / JSON、站内资源与锚点、JavaScript 语法、URL / 配置降级逻辑，并用无浏览器的 DOM 模拟检查了流程切换、架构切换、导航、图片放大及对比分界线逻辑；导出图像已目视核查，并核对原始掩膜与显示图的像素对应。当前环境没有可用的指定浏览器测试能力，因此未完成实际浏览器截图、移动端实机和线上发布验证；请以上传后的最终页面为准。

未操作远程 GitHub 仓库、未推送、未替换已上线页面、未启动业务服务或 GPU 任务。
